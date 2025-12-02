"""
Lógica de clasificación de riesgo de releases
"""
from app.models import Metrics, RiskStatus
from app.config import settings


def classify_risk(metrics: Metrics) -> tuple[RiskStatus, list[str]]:
    """
    Clasifica el riesgo de un release basándose en sus métricas
    
    Args:
        metrics: Métricas del release
    
    Returns:
        Tupla con (estado de riesgo, lista de razones)
    """
    reasons = []
    
    # Verificar tasa de errores
    if metrics.error_rate > settings.error_rate_threshold:
        percentage = metrics.error_rate * 100
        threshold_pct = settings.error_rate_threshold * 100
        reasons.append(
            f"Error rate too high ({percentage:.2f}% > {threshold_pct:.2f}%)"
        )
    
    # Verificar latencia P95
    if metrics.latency_p95 > settings.latency_p95_threshold:
        reasons.append(
            f"Latency P95 exceeds threshold ({metrics.latency_p95:.1f}ms > {settings.latency_p95_threshold}ms)"
        )
    
    # Verificar throughput mínimo
    if metrics.throughput < settings.throughput_min:
        reasons.append(
            f"Throughput below minimum ({metrics.throughput} < {settings.throughput_min} req/s)"
        )
    
    # Verificar errores 5xx (criterio adicional)
    if metrics.errors_5xx > 50:
        reasons.append(
            f"High number of 5xx errors ({metrics.errors_5xx} errors)"
        )
    
    # Determinar estado
    if len(reasons) == 0:
        return RiskStatus.OK, ["All metrics within acceptable thresholds"]
    else:
        return RiskStatus.RISKY, reasons


def calculate_risk_score(metrics: Metrics) -> float:
    """
    Calcula un score de riesgo (0-100)
    
    Args:
        metrics: Métricas del release
    
    Returns:
        Score de 0 (sin riesgo) a 100 (alto riesgo)
    """
    score = 0.0
    
    # Error rate (40% del score)
    error_ratio = metrics.error_rate / settings.error_rate_threshold
    score += min(error_ratio * 40, 40)
    
    # Latency (30% del score)
    latency_ratio = metrics.latency_p95 / settings.latency_p95_threshold
    score += min(latency_ratio * 30, 30)
    
    # Throughput (30% del score) - inverso porque bajo throughput = más riesgo
    throughput_ratio = settings.throughput_min / max(metrics.throughput, 1)
    score += min(throughput_ratio * 30, 30)
    
    return min(score, 100.0)