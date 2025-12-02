"""
Release Radar API - FastAPI Application
"""
from fastapi import FastAPI
from app.routers import releases
from app.config import settings

# Crear aplicación
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Sistema de correlación y análisis de riesgos para despliegues",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir routers
app.include_router(releases.router, tags=["releases"])


# Event handlers
@app.on_event("startup")
async def startup_event():
    """Evento de inicio"""
    print(f"🚀 {settings.app_name} v{settings.version} started")
    print(f"📊 Storage type: {settings.storage_type}")
    print(f"⚠️  Risk thresholds:")
    print(f"   - Error rate: {settings.error_rate_threshold * 100}%")
    print(f"   - Latency P95: {settings.latency_p95_threshold}ms")
    print(f"   - Throughput min: {settings.throughput_min} req/s")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento de cierre"""
    print(f"👋 {settings.app_name} shutting down")


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Release Radar API",
        "version": settings.version,
        "docs": "/docs"
    }