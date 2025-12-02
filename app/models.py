"""
Modelos de datos internos
"""
from datetime import datetime
from typing import Optional
from enum import Enum


class RiskStatus(str, Enum):
    """Estados de riesgo de un release"""
    OK = "OK"
    RISKY = "RIESGOSO"
    UNKNOWN = "DESCONOCIDO"


class Release:
    """Modelo de un release/despliegue"""
    
    def __init__(
        self,
        version: str,
        commit: str,
        timestamp: Optional[datetime] = None,
        status: RiskStatus = RiskStatus.UNKNOWN
    ):
        self.version = version
        self.commit = commit
        self.timestamp = timestamp or datetime.now()
        self.status = status
        self.metrics: Optional['Metrics'] = None
    
    def to_dict(self) -> dict:
        """Convierte el release a diccionario"""
        return {
            "version": self.version,
            "commit": self.commit,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status.value,
            "metrics": self.metrics.to_dict() if self.metrics else None
        }


class Metrics:
    """Métricas de un release"""
    
    def __init__(
        self,
        error_rate: float,
        latency_p95: float,
        throughput: int,
        errors_5xx: int = 0
    ):
        self.error_rate = error_rate
        self.latency_p95 = latency_p95
        self.throughput = throughput
        self.errors_5xx = errors_5xx
    
    def to_dict(self) -> dict:
        """Convierte las métricas a diccionario"""
        return {
            "error_rate": self.error_rate,
            "latency_p95": self.latency_p95,
            "throughput": self.throughput,
            "errors_5xx": self.errors_5xx
        }