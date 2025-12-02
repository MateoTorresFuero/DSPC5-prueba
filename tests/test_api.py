"""
Tests de los endpoints de la API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app, releases_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_db():
    """Limpia la base de datos antes de cada test"""
    releases_db.clear()
    yield
    releases_db.clear()


def test_health_check():
    """Test: /health devuelve status healthy"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_create_release_ok():
    """Test: crear release con métricas OK"""
    payload = {
        "version": "v1.0.0",
        "commit": "abc123",
        "metrics": {
            "error_rate": 0.005,
            "latency_p95": 220,
            "throughput": 1200
        }
    }
    
    response = client.post("/releases", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "v1.0.0"
    assert data["status"] == "OK"


def test_create_release_risky():
    """Test: crear release con métricas riesgosas"""
    payload = {
        "version": "v1.0.1",
        "commit": "def456",
        "metrics": {
            "error_rate": 0.05,  # Alto
            "latency_p95": 500,  # Alta
            "throughput": 500    # Bajo
        }
    }
    
    response = client.post("/releases", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "v1.0.1"
    assert data["status"] == "RIESGOSO"


def test_create_release_duplicate():
    """Test: crear release duplicado -> error 409"""
    payload = {
        "version": "v1.0.0",
        "commit": "abc123"
    }
    
    # Primera vez OK
    response1 = client.post("/releases", json=payload)
    assert response1.status_code == 200
    
    # Segunda vez error
    response2 = client.post("/releases", json=payload)
    assert response2.status_code == 409


def test_list_releases():
    """Test: listar releases"""
    # Crear 2 releases
    client.post("/releases", json={"version": "v1.0.0", "commit": "abc"})
    client.post("/releases", json={"version": "v1.0.1", "commit": "def"})
    
    response = client.get("/releases")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_release():
    """Test: obtener release específico"""
    # Crear release
    client.post("/releases", json={"version": "v1.0.0", "commit": "abc"})
    
    response = client.get("/releases/v1.0.0")
    
    assert response.status_code == 200
    data = response.json()
    assert data["version"] == "v1.0.0"


def test_get_release_not_found():
    """Test: obtener release inexistente -> 404"""
    response = client.get("/releases/v99.99.99")
    
    assert response.status_code == 404


def test_analyze_release():
    """Test: analizar release con métricas"""
    # Crear release riesgoso
    client.post("/releases", json={
        "version": "v1.0.0",
        "commit": "abc",
        "metrics": {
            "error_rate": 0.05,
            "latency_p95": 500,
            "throughput": 500
        }
    })
    
    response = client.get("/analysis/v1.0.0")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "RIESGOSO"
    assert len(data["reasons"]) > 0


def test_analyze_release_no_metrics():
    """Test: analizar release sin métricas"""
    # Crear release sin métricas
    client.post("/releases", json={
        "version": "v1.0.0",
        "commit": "abc"
    })
    
    response = client.get("/analysis/v1.0.0")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "DESCONOCIDO"