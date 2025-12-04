# 📋 TARJETAS SIMPLES - Sprint 2 (Release Radar)

**Issues #11 - #16**

---

## 🟦 **Issue #11: Script generate_metrics.py**

**Descripción:**
Script que simula métricas realistas para releases.

**Tareas:**

- Crear `scripts/generate_metrics.py`
- Generar error_rate, latency_p95, throughput con aleatoriedad
- Argumentos: `--version`, `--quality` (normal/risky/random)
- Guardar en `app/data/metrics/metrics-{version}.json`

**Criterio:** Script ejecuta y genera JSON válido con métricas simuladas.

---

## 🟦 **Issue #12: Dockerfile**

**Descripción:**
Contenerizar la API con buenas prácticas de seguridad.

**Tareas:**

- Crear `Dockerfile` con imagen `python:3.10-slim`
- Usuario no-root (appuser)
- HEALTHCHECK configurado
- Crear `.dockerignore`

**Criterio:** `docker build` ejecuta sin errores, imagen < 250MB, corre como non-root.

**PR:** (link cuando se cree)

---

## 🟦 **Issue #13: docker-compose.yml**

**Descripción:**
Orquestar la API con Docker Compose.

**Tareas:**

- Crear `docker-compose.yml` con servicio `api`
- Exponer puerto 8000
- Volumen para `app/data/` (persistencia)
- Healthcheck habilitado

**Criterio:** `docker compose up` levanta API y responde en localhost:8000.

**PR:** (link cuando se cree)

---

## 🟦 **Issue #14: Workflow release_analysis.yml**

**Descripción:**
Pipeline que registra release, genera métricas y clasifica riesgo.

**Tareas:**

- Crear `.github/workflows/release_analysis.yml`
- Job 1: Registrar release (POST /releases con curl)
- Job 2: Generar métricas con `generate_metrics.py`
- Job 3: Clasificar y obtener análisis
- Job 4: Guardar `.evidence/release-risk-report.json`
- Trigger: `workflow_dispatch` (manual)

**Criterio:** Workflow ejecuta manualmente y genera evidencia en `.evidence/`.

**PR:** (link cuando se cree)

---

## 🟦 **Issue #15: Workflow build_scan_sbom.yml**

**Descripción:**
Build de imagen Docker, scan de seguridad y generación de SBOM.

**Tareas:**

- Crear `.github/workflows/build_scan_sbom.yml`
- Docker build de la imagen
- Scan con Trivy → `.evidence/trivy-report.json`
- SBOM con Syft → `.evidence/sbom.json`
- Usar **self-hosted runner** (documentar en README)

**Criterio:** Workflow genera SBOM y reporte de vulnerabilidades en `.evidence/`.

**Nota:** Requiere self-hosted runner configurado por el dueño del repo.

**PR:** (link cuando se cree)

---

## 🟦 **Issue #16: Video Sprint 2**

**Descripción:**
Grabar demo mostrando Docker, workflows y evidencias.

**Tareas:**

- Mostrar tablero Kanban actualizado
- Demo: `docker compose up` y probar API
- Ejecutar `generate_metrics.py` y ver JSON generado
- Ejecutar workflows `release_analysis.yml` y `build_scan_sbom.yml`
- Mostrar archivos en `.evidence/`

**Criterio:** Video de 5-7 minutos subido y compartido.

---

## 📊 Resumen Sprint 2

**Total:** 6 issues (#11 - #16)  
**WIP Limit:** Máximo 2 tareas en "Doing" por persona

**Distribución sugerida:**

- Persona 1: #11, #12 (script + Docker)
- Persona 2: #13, #14 (Compose + workflow análisis)
- Persona 3: #15, #16 (workflow SBOM + video)

**Dependencias:**

- Issue #14 depende de #11 (necesita el script)
- Issue #15 depende de #12 (necesita Dockerfile)
- Issue #16 depende de todos

---

## 📝 Notas importantes:

1. **Self-hosted runner**: Solo el dueño del repo puede configurarlo (Settings → Actions → Runners). Los demás pueden escribir el workflow.

2. **`.evidence/` al final del Sprint 2:**

   ```
   .evidence/
   ├── README.md
   ├── release-risk-report.json  # Issue #14
   ├── sbom.json                 # Issue #15
   └── trivy-report.json         # Issue #15
   ```

3. **Estructura final:**
   ```
   release-radar/
   ├── .github/workflows/
   │   ├── ci.yml              (Sprint 1)
   │   ├── release_analysis.yml   (Sprint 2, #14)
   │   └── build_scan_sbom.yml    (Sprint 2, #15)
   ├── scripts/
   │   └── generate_metrics.py    (Sprint 2, #11)
   ├── Dockerfile                 (Sprint 2, #12)
   └── docker-compose.yml         (Sprint 2, #13)
   ```

---

**¿Necesitas el contenido del `docker-compose.yml` o de los workflows ahora?**
