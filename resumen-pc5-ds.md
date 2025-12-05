# Análisis del Proyecto 14 - "Release Radar"

## ¿De qué trata?

**Release Radar** es un sistema de correlación y análisis de riesgos para despliegues de software. Básicamente, es una herramienta que te ayuda a **responder la pregunta crítica**: _"¿Este último despliegue rompió algo?"_

El proyecto construye:

1. **Una API (FastAPI)** que registra cada release/despliegue que haces
2. **Un sistema de análisis** que recolecta métricas de comportamiento del sistema
3. **Un clasificador de riesgo** que determina si un release es "OK" o "Riesgoso" basándose en datos reales

La idea es que después de cada despliegue, el sistema automáticamente:

- Registra el evento (commit, tag, timestamp)
- Recolecta métricas (tasa de errores, latencia, códigos 5xx)
- Compara contra baseline o releases previos
- Marca el release como seguro o problemático
- Genera reportes para auditoría

---

## ¿Por qué es útil en el mundo real?

### Problema que resuelve:

En producción real, uno de los mayores dolores de cabeza es el **"debugging temporal"**:

- Haces un despliegue a las 3pm
- A las 4pm empiezan a llegar quejas de usuarios
- A las 5pm te das cuenta que la tasa de errores subió 300%
- **¿Fue tu despliegue? ¿Fue otro? ¿Fue tráfico externo?**

**Release Radar automatiza la detección de estos problemas.**

### Casos de uso reales:

1. **Post-deployment validation automática**

   - Evita que un deploy malo permanezca en producción horas sin detección
   - En empresas grandes (Netflix, Amazon, Google) esto es crítico

2. **Decisiones de rollback informadas**

   - En vez de adivinar si hacer rollback, tienes datos objetivos
   - "El release v2.3.1 tiene 45% más errores 500 que v2.3.0" → rollback inmediato

3. **Auditoría y post-mortems**

   - Cuando algo falla en producción, puedes rastrear exactamente qué release lo causó
   - Timeline visual de releases y su impacto

4. **CI/CD con gates inteligentes**

   - Puedes bloquear deploys subsecuentes si detectas un release riesgoso
   - "No despliegues staging si dev está marcado como riesgoso"

5. **Cultura de ownership**
   - Los equipos ven objetivamente el impacto de sus cambios
   - Incentiva mejor testing antes de desplegar

### Empresas que usan sistemas similares:

- **Datadog APM**: Tiene "Deployment Tracking" que hace exactamente esto
- **New Relic**: "Deployment Markers" con análisis de impacto
- **Honeycomb**: Correlación automática de deploys con anomalías
- **LaunchDarkly**: Para feature flags, pero con análisis de impacto similar

---

## Retos principales del proyecto

### 1. **Reto de Integración: Fuentes de Métricas**

**El problema**: Necesitas métricas reales o simuladas convincentes.

**Complejidad**:

- En el proyecto se pide simular métricas (fichero JSON o script `generate_metrics.py`)
- Pero tienes que hacerlo de forma **realista**: no puedes solo poner números random
- Debes simular:
  - Tasa de errores baseline (ej: 0.5%) y spikes (ej: 5% en release malo)
  - Latencia P50, P95, P99
  - Throughput (requests/segundo)
  - Errores 4xx vs 5xx

**Tip**: El video menciona que podrías conectar con Prometheus conceptualmente. Si quieres impresionar, podrías levantar un Prometheus local dummy con métricas mockeadas.

---

### 2. **Reto de Lógica: Clasificación de Riesgo**

**El problema**: ¿Qué hace que un release sea "riesgoso"?

**Complejidad**:

- No es solo "error_rate > X"
- Necesitas considerar:
  - **Comparación relativa**: 2% de errores puede ser normal para un servicio, catastrófico para otro
  - **Ventanas de tiempo**: ¿Cuánto tiempo esperas después del deploy para medir? (5 min, 30 min, 1 hora)
  - **Múltiples métricas**: Un release puede tener más errores pero menos latencia, ¿es riesgoso?
  - **Falsos positivos**: Un spike de tráfico externo no debería marcar el release como malo

**Decisión de diseño**:

- Podrías implementar un sistema de **scoring** (errores: 40%, latencia: 30%, 5xx: 30%)
- O un sistema de **umbrales múltiples** (si error_rate > 2x baseline AND latencia > 1.5x → riesgoso)
- O **machine learning simple** (regresión logística), pero eso es overkill para el proyecto

---

### 3. **Reto de Temporalidad: Estado y Timeline**

**El problema**: Un release no es un evento puntual, evoluciona en el tiempo.

**Complejidad**:

- Un release puede ser "OK" en los primeros 10 minutos y volverse "Riesgoso" después
- Necesitas **actualizar el estado** de releases conforme pasa el tiempo
- El endpoint `/timeline` debe mostrar la evolución histórica

**Implementación**:

```
Release v1.2.3 registrado a las 14:00
├─ 14:05: Análisis inicial → OK (error_rate: 0.5%)
├─ 14:15: Análisis actualizado → OK (error_rate: 0.6%)
├─ 14:30: Análisis actualizado → RIESGOSO (error_rate: 3.2%)
└─ 14:45: Estado final → RIESGOSO
```

**Reto técnico**: Cómo modelar esto en tu base de datos (SQLite/PostgreSQL). ¿Un registro por release? ¿Múltiples análisis por release con timestamps?

---

### 4. **Reto de Pipeline: `release_analysis.yml`**

**El problema**: Automatizar todo el flujo en GitHub Actions.

**Complejidad del workflow**:

```
Trigger: push a main o workflow_dispatch
│
├─ Job 1: Registrar Release
│   └─ Calcular versión (ej: timestamp, commit SHA, o leer de tag)
│   └─ POST /releases con metadata
│
├─ Job 2: Generar/Consultar Métricas
│   └─ Ejecutar generate_metrics.py (simulado)
│   └─ O curl a un /metrics endpoint de otro servicio
│
├─ Job 3: Análisis de Riesgo
│   └─ Obtener métricas del Job 2
│   └─ Comparar contra baseline o release anterior
│   └─ PUT /analysis/{release} con clasificación
│
└─ Job 4: Generar Evidencias
    └─ Guardar .evidence/release-risk-report.json
    └─ Upload como artifact de GitHub Actions
```

**Dependencias entre jobs**: Necesitas usar `needs: [job1, job2]` y pasar datos entre jobs (via artifacts o variables de entorno).

---

### 5. **Reto de Evidencias: `.evidence/release-risk-report.json`**

**El problema**: Generar reportes útiles y completos en cada sprint.

**Contenido esperado**:

```json
{
  "timestamp": "2024-12-01T15:30:00Z",
  "release": "v1.2.3",
  "commit": "abc123def",
  "metrics": {
    "error_rate": 0.008,
    "latency_p95": 245,
    "throughput": 1200
  },
  "baseline": {
    "error_rate": 0.005,
    "latency_p95": 220,
    "throughput": 1150
  },
  "risk_score": 65,
  "classification": "RIESGOSO",
  "reasons": ["Error rate increased by 60%", "Latency P95 increased by 11%"]
}
```

**Sprint 1**: reporte básico con clasificación simple
**Sprint 2**: añadir métricas simuladas y comparación
**Sprint 3**: timeline completo con múltiples releases

---

### 6. **Reto de Visualización: Timeline de Releases**

**El problema**: `/timeline` debe ser informativo, no solo una lista.

**Expectativa**:

- Mostrar releases en orden cronológico
- Código de colores: verde (OK), rojo (Riesgoso)
- Métricas resumidas por release
- Idealmente, un gráfico simple (podrías usar una biblioteca como `matplotlib` para generar imagen, o devolver datos para un frontend)

**Consideración**: El proyecto es backend-focused, pero si añades un frontend mínimo (HTML + Chart.js) en un artifact, sumarías muchos puntos en la demo.

---

### 7. **Reto de Integración con Deploy Real**

**El problema**: En Sprint 3 se pide que `release_analysis.yml` se encadene con un pipeline de deploy.

**Flujo esperado**:

```
1. Developer hace push a main
2. CI/CD corre tests (ci.yml)
3. Si pasa, deploy a "staging" (deploy.yml)
4. Después del deploy, dispara release_analysis.yml
5. Release Analysis marca como OK o Riesgoso
6. Si Riesgoso:
   - Notificar al equipo
   - Bloquear deploy a producción
   - Sugerir rollback
```

**Implementación GitHub Actions**:

- Usar `workflow_run` para disparar `release_analysis.yml` después de `deploy.yml`
- O usar `repository_dispatch` para comunicación entre workflows

---

## Componentes clave del stack

### Backend (FastAPI):

- **Endpoints**:
  - `GET /health` → healthcheck estándar
  - `GET /releases` → lista todos los releases
  - `POST /releases` → registra nuevo release
  - `GET /analysis/{release}` → métricas y clasificación de un release específico
  - `GET /timeline` → evolución histórica de releases

### Scripts Python:

- **`generate_metrics.py`**: Simula métricas por release (puede leer de un config o generar algorítmicamente)
- **`classify_risk.py`**: Lógica de clasificación (puede ser parte de la API o script separado)

### Storage:

- **SQLite o PostgreSQL**:
  - Tabla `releases`: id, version, commit, timestamp, status
  - Tabla `metrics`: id, release_id, error_rate, latency, throughput, timestamp
  - Tabla `analysis`: id, release_id, risk_score, classification, reasons, timestamp

### Docker/K8s (opcional pero recomendado):

- Contenerizar la API para Sprint 2/3
- En K8s, podrías tener un CronJob que ejecute análisis periódico

---

## Mi opinión sobre el proyecto

### Aspectos positivos:

✅ **Relevancia práctica**: Es un problema real que las empresas enfrentan diariamente

✅ **Complejidad balanceada**: No es trivial (como el Proyecto 1), pero tampoco extremadamente complejo (como el 11)

✅ **Flexible**: Puedes hacerlo simple (umbrales fijos) o sofisticado (scoring multi-dimensional)

✅ **Buen storytelling para la demo**: Es fácil explicar el valor de negocio en el video final

✅ **Integración DevSecOps clara**: Pipelines, evidencias, automatización

### Aspectos desafiantes:

⚠️ **Simulación de métricas realistas**: No es difícil técnicamente, pero requiere pensamiento para que sea convincente

⚠️ **Lógica de clasificación**: Puedes caer en hacer algo muy simplista ("if error > 1% → riesgo") que no impresione

⚠️ **Orquestación de workflows**: Encadenar `deploy.yml` → `release_analysis.yml` requiere entender bien GitHub Actions

⚠️ **Evidencias evolutivas**: Cada sprint debe añadir algo nuevo y visible a `.evidence/`, no repetir lo mismo

---

## Recomendaciones para destacar

1. **Añade un dashboard mínimo**: Aunque sea HTML estático que lea el JSON de timeline y lo muestre con colores

2. **Implementa notificaciones simuladas**: En el workflow, si detectas un release riesgoso, haz un `echo` grande y visible en los logs, o genera un issue automáticamente en GitHub

3. **Usa datos semi-realistas**: En vez de métricas completamente random, podrías basarte en distribuciones conocidas (errores siguen Poisson, latencia sigue normal, etc.)

4. **Documenta tu criterio de riesgo**: En el README, explica **por qué** elegiste tus umbrales y cómo se podrían tunear

5. **Conecta con rollback**: En Sprint 3, cuando detectes un release riesgoso, podrías tener un endpoint `/rollback/{release}` que simule el proceso (aunque sea fake)

---

¿Qué te parece el proyecto ahora que lo entiendes mejor? ¿Tienes dudas sobre algún aspecto específico antes de empezar a implementar?
