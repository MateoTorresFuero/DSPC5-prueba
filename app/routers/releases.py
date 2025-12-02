"""
Endpoints relacionados con releases
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime

from app.schemas import (
    ReleaseCreateSchema,
    ReleaseResponseSchema,
    AnalysisResponseSchema,
    HealthResponseSchema
)
from app.models import Release, Metrics, RiskStatus
from app.services.storage import storage
from app.services.classifier import classify_risk
from app.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponseSchema)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.version,
        "timestamp": datetime.now()
    }


@router.post(
    "/releases",
    response_model=ReleaseResponseSchema,
    status_code=status.HTTP_201_CREATED
)
async def create_release(release_data: ReleaseCreateSchema):
    """
    Crea un nuevo release
    
    - **version**: Versión del release (ej: v1.2.3)
    - **commit**: Hash del commit
    - **metrics**: Métricas opcionales del release
    """
    # Verificar si ya existe
    existing = storage.get_release(release_data.version)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Release {release_data.version} already exists"
        )
    
    # Crear release
    release = Release(
        version=release_data.version,
        commit=release_data.commit
    )
    
    # Si hay métricas, clasificar riesgo
    if release_data.metrics:
        metrics = Metrics(
            error_rate=release_data.metrics.error_rate,
            latency_p95=release_data.metrics.latency_p95,
            throughput=release_data.metrics.throughput,
            errors_5xx=release_data.metrics.errors_5xx
        )
        release.metrics = metrics
        risk_status, _ = classify_risk(metrics)
        release.status = risk_status
    
    # Guardar
    storage.save_release(release)
    
    return release.to_dict()


@router.get("/releases", response_model=list[ReleaseResponseSchema])
async def list_releases():
    """
    Lista todos los releases ordenados por fecha (más reciente primero)
    """
    releases = storage.list_releases()
    return [r.to_dict() for r in releases]


@router.get("/releases/{version}", response_model=ReleaseResponseSchema)
async def get_release(version: str):
    """
    Obtiene un release específico por versión
    """
    release = storage.get_release(version)
    if not release:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Release {version} not found"
        )
    return release.to_dict()


@router.get("/analysis/{version}", response_model=AnalysisResponseSchema)
async def analyze_release(version: str):
    """
    Analiza el riesgo de un release específico
    
    Devuelve el estado (OK/RIESGOSO) y las razones de la clasificación
    """
    release = storage.get_release(version)
    if not release:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Release {version} not found"
        )
    
    if not release.metrics:
        return {
            "version": release.version,
            "status": RiskStatus.UNKNOWN.value,
            "metrics": None,
            "reasons": ["No metrics available for analysis"]
        }
    
    # Clasificar riesgo
    risk_status, reasons = classify_risk(release.metrics)
    
    return {
        "version": release.version,
        "status": risk_status.value,
        "metrics": release.metrics.to_dict(),
        "reasons": reasons
    }