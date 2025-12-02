"""
Schemas Pydantic para validación de request/response
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MetricsSchema(BaseModel):
    """Schema de métricas"""
    error_rate: float = Field(..., ge=0, le=1, description="Tasa de errores (0-1)")
    latency_p95: float = Field(..., ge=0, description="Latencia P95 en ms")
    throughput: int = Field(..., ge=0, description="Requests por segundo")
    errors_5xx: int = Field(default=0, ge=0, description="Número de errores 5xx")

    class Config:
        json_schema_extra = {
            "example": {
                "error_rate": 0.015,
                "latency_p95": 245.5,
                "throughput": 1200,
                "errors_5xx": 5
            }
        }


class ReleaseCreateSchema(BaseModel):
    """Schema para crear un release"""
    version: str = Field(..., min_length=1, description="Versión del release")
    commit: str = Field(..., min_length=7, max_length=40, description="Hash del commit")
    metrics: Optional[MetricsSchema] = Field(None, description="Métricas del release")

    class Config:
        json_schema_extra = {
            "example": {
                "version": "v1.2.3",
                "commit": "abc123def456",
                "metrics": {
                    "error_rate": 0.005,
                    "latency_p95": 220.0,
                    "throughput": 1150,
                    "errors_5xx": 2
                }
            }
        }


class ReleaseResponseSchema(BaseModel):
    """Schema de respuesta de un release"""
    version: str
    commit: str
    timestamp: datetime
    status: str
    metrics: Optional[MetricsSchema]

    class Config:
        json_schema_extra = {
            "example": {
                "version": "v1.2.3",
                "commit": "abc123def456",
                "timestamp": "2024-12-01T15:30:00",
                "status": "OK",
                "metrics": {
                    "error_rate": 0.005,
                    "latency_p95": 220.0,
                    "throughput": 1150,
                    "errors_5xx": 2
                }
            }
        }


class AnalysisResponseSchema(BaseModel):
    """Schema de análisis de riesgo"""
    version: str
    status: str
    metrics: Optional[MetricsSchema]
    reasons: list[str] = Field(default_factory=list, description="Razones de la clasificación")

    class Config:
        json_schema_extra = {
            "example": {
                "version": "v1.2.3",
                "status": "RIESGOSO",
                "metrics": {
                    "error_rate": 0.035,
                    "latency_p95": 450.0,
                    "throughput": 800,
                    "errors_5xx": 120
                },
                "reasons": [
                    "Error rate increased by 600% (baseline: 0.5%)",
                    "Latency P95 exceeds threshold (450ms > 300ms)",
                    "Throughput below minimum (800 < 1000)"
                ]
            }
        }


class HealthResponseSchema(BaseModel):
    """Schema de respuesta de health check"""
    status: str
    version: str
    timestamp: datetime

    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "0.1.0",
                "timestamp": "2024-12-01T15:30:00"
            }
        }