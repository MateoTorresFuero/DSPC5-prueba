"""
Tests de la función clasificadora
"""
from app.classifier import classify_risk


def test_classify_risk_ok():
    """Test: métricas normales -> OK"""
    metrics = {
        "error_rate": 0.005,  # 0.5%
        "latency_p95": 220,
        "throughput": 1200
    }
    
    status, reasons = classify_risk(metrics)
    
    assert status == "OK"
    assert len(reasons) == 1
    assert "aceptables" in reasons[0].lower()


def test_classify_risk_high_error_rate():
    """Test: error rate alto -> RIESGOSO"""
    metrics = {
        "error_rate": 0.05,  # 5% (umbral: 2%)
        "latency_p95": 220,
        "throughput": 1200
    }
    
    status, reasons = classify_risk(metrics)
    
    assert status == "RIESGOSO"
    assert len(reasons) == 1
    assert "error rate" in reasons[0].lower()


def test_classify_risk_high_latency():
    """Test: latencia alta -> RIESGOSO"""
    metrics = {
        "error_rate": 0.005,
        "latency_p95": 500,  # 500ms (umbral: 300ms)
        "throughput": 1200
    }
    
    status, reasons = classify_risk(metrics)
    
    assert status == "RIESGOSO"
    assert len(reasons) == 1
    assert "latencia" in reasons[0].lower()


def test_classify_risk_low_throughput():
    """Test: throughput bajo -> RIESGOSO"""
    metrics = {
        "error_rate": 0.005,
        "latency_p95": 220,
        "throughput": 500  # 500 req/s (mínimo: 1000)
    }
    
    status, reasons = classify_risk(metrics)
    
    assert status == "RIESGOSO"
    assert len(reasons) == 1
    assert "throughput" in reasons[0].lower()


def test_classify_risk_multiple_problems():
    """Test: múltiples problemas -> RIESGOSO con varias razones"""
    metrics = {
        "error_rate": 0.05,   # Alto
        "latency_p95": 500,   # Alta
        "throughput": 500     # Bajo
    }
    
    status, reasons = classify_risk(metrics)
    
    assert status == "RIESGOSO"
    assert len(reasons) == 3  # 3 problemas