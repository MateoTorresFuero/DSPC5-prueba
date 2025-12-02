"""
Release Radar API - Sprint 1 MVP Simple
"""
from fastapi import FastAPI, HTTPException
from app.classifier import classify_risk
from app.models import create_release

app = FastAPI(
    title="Release Radar API",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Release Radar API está en funcionamiento. Visita /docs para la documentación."}

# Almacenamiento en memoria (dict simple)
releases_db = {}


@app.get("/health")
def health_check():
    """Health check endpoint"""
    from datetime import datetime
    return {
        "status": "healthy",
        "version": "0.1.0",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/releases")
def create_release_endpoint(release: dict):
    """
    Crea un nuevo release
    
    Ejemplo de body:
    {
        "version": "v1.0.0",
        "commit": "abc123",
        "metrics": {
            "error_rate": 0.005,
            "latency_p95": 220,
            "throughput": 1200
        }
    }
    """
    version = release.get("version")
    
    if not version:
        raise HTTPException(status_code=400, detail="version is required")
    
    if version in releases_db:
        raise HTTPException(status_code=409, detail=f"Release {version} already exists")
    
    # Crear release usando models.py
    new_release = create_release(
        version=version,
        commit=release.get("commit", "unknown"),
        metrics=release.get("metrics")
    )
    
    # Si hay métricas, clasificar
    if new_release["metrics"]:
        status, _ = classify_risk(new_release["metrics"])
        new_release["status"] = status
    
    releases_db[version] = new_release
    return new_release


@app.get("/releases")
def list_releases():
    """Lista todos los releases"""
    releases = list(releases_db.values())
    # Ordenar por timestamp (más reciente primero)
    releases.sort(key=lambda r: r["timestamp"], reverse=True)
    return releases


@app.get("/releases/{version}")
def get_release(version: str):
    """Obtiene un release específico"""
    if version not in releases_db:
        raise HTTPException(status_code=404, detail=f"Release {version} not found")
    return releases_db[version]


@app.get("/analysis/{version}")
def analyze_release(version: str):
    """
    Analiza el riesgo de un release
    
    Devuelve:
    {
        "version": "v1.0.0",
        "status": "OK" o "RIESGOSO",
        "metrics": {...},
        "reasons": ["razón 1", "razón 2"]
    }
    """
    if version not in releases_db:
        raise HTTPException(status_code=404, detail=f"Release {version} not found")
    
    release = releases_db[version]
    
    if not release["metrics"]:
        return {
            "version": version,
            "status": "DESCONOCIDO",
            "metrics": None,
            "reasons": ["No hay métricas disponibles"]
        }
    
    # Clasificar riesgo
    status, reasons = classify_risk(release["metrics"])
    
    return {
        "version": version,
        "status": status,
        "metrics": release["metrics"],
        "reasons": reasons
    }
