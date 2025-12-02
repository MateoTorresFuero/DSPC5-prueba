# Release Radar - Sprint 1

Sistema simple de análisis de riesgo para despliegues.

## 📁 Estructura

```
app/
├── __init__.py       # 3 líneas
├── main.py           # 115 líneas - FastAPI + endpoints
├── models.py         # 40 líneas - Funciones para crear dicts
└── classifier.py     # 50 líneas - Función classify_risk()
```

**Total: ~210 líneas de código**

---

## 🚀 Instalación y Ejecución

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Correr la API

```bash
uvicorn app.main:app --reload
```

API disponible en: http://localhost:8000

Docs interactiva: http://localhost:8000/docs

---

## 🧪 Probar la API

### Health check
```bash
curl http://localhost:8000/health
```

### Crear release OK
```bash
curl -X POST http://localhost:8000/releases \
  -H "Content-Type: application/json" \
  -d '{
    "version": "v1.0.0",
    "commit": "abc123",
    "metrics": {
      "error_rate": 0.005,
      "latency_p95": 220,
      "throughput": 1200
    }
  }'
```

### Crear release RIESGOSO
```bash
curl -X POST http://localhost:8000/releases \
  -H "Content-Type: application/json" \
  -d '{
    "version": "v1.0.1",
    "commit": "def456",
    "metrics": {
      "error_rate": 0.05,
      "latency_p95": 500,
      "throughput": 500
    }
  }'
```

### Listar releases
```bash
curl http://localhost:8000/releases
```

### Analizar un release
```bash
curl http://localhost:8000/analysis/v1.0.1
```

---

## 🧪 Correr Tests

```bash
# Todos los tests
pytest -v

# Solo tests del clasificador
pytest tests/test_classifier.py -v

# Solo tests de la API
pytest tests/test_api.py -v
```

---

## ⚙️ Umbrales de Riesgo

Un release es **RIESGOSO** si:
- Error rate > 2%
- Latencia P95 > 300ms
- Throughput < 1000 req/s

(Puedes cambiarlos en `app/classifier.py`)

---

## 📊 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/releases` | Crear release |
| GET | `/releases` | Listar todos |
| GET | `/releases/{version}` | Obtener uno |
| GET | `/analysis/{version}` | Analizar riesgo |

---

## 💾 Almacenamiento

**Sprint 1**: Dict en memoria (`releases_db = {}`)
- Los datos se pierden al reiniciar
- Perfecto para MVP

**Sprint 2**: Se puede cambiar a archivo JSON o SQLite

---

## ✅ Checklist Sprint 1

- [x] Estructura del proyecto
- [x] API con FastAPI
- [x] `app/models.py` - Funciones para crear releases
- [x] `app/classifier.py` - Función classify_risk()
- [x] Endpoints: /health, /releases, /analysis
- [x] Tests unitarios (test_classifier.py)
- [x] Tests de API (test_api.py)
- [ ] CI workflow (próximo paso)
- [ ] Video demo

---

## 🎯 Cumple Issue #2

✅ **Issue #2: Modelo Release y función clasificadora**
- ✅ Crear `app/models.py` con función `create_release()`
- ✅ Crear `app/classifier.py` con función `classify_risk()`
- ✅ Lógica: si error_rate > umbral → RIESGOSO

---

## 🔄 Diferencias con versión compleja

| Aspecto | Versión compleja | Esta versión |
|---------|-----------------|--------------|
| Archivos | 10 archivos | 4 archivos |
| Líneas | ~350 líneas | ~210 líneas |
| Pydantic schemas | Sí | No (dicts) |
| Config separado | Sí | No (hardcoded) |
| Modelos | Clases OOP | Funciones simples |
| Capa servicios | Sí | No |

---

## 📝 Notas

- **Storage**: Dict en memoria. Los datos se pierden al reiniciar.
- **Métricas**: Se proporcionan al crear el release.
- **Clasificación**: Basada en umbrales estáticos simples.
- **Simplicidad**: Diseñado para estudiantes, fácil de entender y extender.

---

## 🚀 Próximos pasos (Sprint 2)

- Añadir Docker y docker-compose
- Script `generate_metrics.py`
- Pipeline `release_analysis.yml`
- Evidencias en `.evidence/`
