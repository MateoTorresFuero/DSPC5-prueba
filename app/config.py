"""
Configuración y umbrales para clasificación de riesgos
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    app_name: str = "Release Radar API"
    version: str = "0.1.0"
    
    # Umbrales de clasificación de riesgo
    error_rate_threshold: float = 0.02  # 2% de errores
    latency_p95_threshold: float = 300  # 300ms
    throughput_min: int = 100  # requests/segundo mínimo
    
    # Configuración de almacenamiento
    storage_type: str = "memory"  # memory, sqlite (futuro)
    
    class Config:
        env_prefix = "RELEASE_RADAR_"


settings = Settings()