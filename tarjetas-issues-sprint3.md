# 📋 TARJETAS SIMPLES - Sprint 3 (Release Radar)

**Issues #20 - #25**

---

## 🟦 **Issue #20: Endpoint /timeline**

**Descripción:**
Implementar endpoint que devuelve releases ordenados cronológicamente con sus estados.

**Tareas:**

- Añadir `GET /timeline` en `app/main.py`
- Devolver releases ordenados por timestamp (más reciente primero)
- Incluir version, status, metrics y timestamp de cada release

**Criterio:** `/timeline` devuelve JSON con lista de releases ordenada correctamente.

---

## 🟦 **Issue #21: Workflow deploy_dummy.yml**

**Descripción:**
Simular un despliegue para demostrar flujo completo de CI/CD.

**Tareas:**

- Crear `.github/workflows/deploy_dummy.yml`
- Job que simula deploy (echo "Deploying v{version}...")
- Guardar log en `.evidence/deploy-log.txt`
- Trigger: `workflow_dispatch` con input de version

**Criterio:** Workflow ejecuta y genera log de despliegue en `.evidence/`.

**PR:** (link cuando se cree)

---

## 🟦 **Issue #22: Encadenar workflows (deploy → análisis)**

**Descripción:**
Configurar que `release_analysis.yml` se ejecute automáticamente después de `deploy_dummy.yml`.

**Tareas:**

- Modificar `release_analysis.yml`
- Añadir trigger `workflow_run` para ejecutar después de deploy
- Pasar version entre workflows
- Probar flujo completo

**Criterio:** Push a main → deploy_dummy ejecuta → release_analysis ejecuta automáticamente.

**PR:** (link cuando se cree)

---

## 🟦 **Issue #23: Generar timeline.json en evidencias**

**Descripción:**
Script o paso en workflow que guarde snapshot del timeline en `.evidence/`.

**Tareas:**

- Crear script o añadir step en `release_analysis.yml`
- Llamar a `/timeline` y guardar respuesta
- Guardar en `.evidence/timeline.json`

**Criterio:** `.evidence/timeline.json` se genera con releases actuales.

**PR:** (link cuando se cree)

---

## 🟦 **Issue #24: Despliegue K8s (OPCIONAL)**

**Descripción:**
Si da tiempo, desplegar la API en Minikube o kind.

**Tareas:**

- Crear `k8s/deployment.yaml` y `k8s/service.yaml`
- ConfigMap con configuración
- Desplegar con `kubectl apply -f k8s/`
- Probar API desde cluster

**Criterio:** Pods corriendo y API accesible desde el cluster.

**Nota:** Opcional - solo si el equipo tiene tiempo.

**PR:** (link cuando se cree)

---

## 🟦 **Issue #25: Video Sprint 3 y Demo Final**

**Descripción:**
Grabar demo mostrando flujo completo y video final del proyecto.

**Tareas:**

- Video Sprint 3 (5-7 min):
  - Mostrar `/timeline`
  - Ejecutar flujo: commit → deploy → análisis
  - Mostrar release riesgoso detectado
  - (Opcional) Mostrar K8s si se implementó
- Video Final (12-15 min):
  - Recorrido completo de los 3 sprints
  - Demo end-to-end
  - Tablero Kanban
  - Explicación técnica

**Criterio:** Ambos videos subidos y compartidos.

---

## 📊 Resumen Sprint 3

**Total:** 6 issues (#20 - #25)  
**WIP Limit:** Máximo 2 tareas en "Doing" por persona

**Distribución sugerida:**

- Persona 1: #20, #21 (endpoint + workflow deploy)
- Persona 2: #22, #23 (encadenamiento + timeline.json)
- Persona 3: #24, #25 (K8s opcional + videos)

**Dependencias:**

- Issue #22 depende de #21 (necesita deploy_dummy.yml)
- Issue #23 depende de #20 (necesita /timeline)
- Issue #25 depende de todos

---

## 📝 Notas importantes:

1. **Issue #24 (K8s) es OPCIONAL:** Solo si tienen tiempo y ganas. NO es crítico para aprobar.

2. **`.evidence/` al final del Sprint 3:**

   ```
   .evidence/
   ├── README.md
   ├── release-risk-report.json  (Sprint 2)
   ├── sbom.json                 (Sprint 2)
   ├── trivy-report.json         (Sprint 2)
   ├── deploy-log.txt            (Sprint 3, #21)
   └── timeline.json             (Sprint 3, #23)
   ```

3. **Estructura final del proyecto:**
   ```
   release-radar/
   ├── .github/workflows/
   │   ├── ci.yml
   │   ├── release_analysis.yml   (mejorado en #22)
   │   ├── build_scan_sbom.yml
   │   └── deploy_dummy.yml       (#21)
   ├── k8s/                       (opcional, #24)
   │   ├── deployment.yaml
   │   └── service.yaml
   ├── app/
   │   └── main.py                (con /timeline, #20)
   └── .evidence/                 (completo)
   ```

---

## 🎬 Contenido del Video Final (Issue #25):

**Duración:** 12-15 minutos

1. **Introducción** (2 min)

   - Problema que resuelve Release Radar
   - Stack técnico

2. **Tablero Kanban** (2 min)

   - Mostrar evolución de 3 sprints
   - ~17 historias completadas
   - WIP respetado

3. **Demo End-to-End** (5 min)

   - API local con `/timeline`
   - Docker Compose
   - Flujo completo: commit → deploy → análisis automático
   - Release OK vs RIESGOSO

4. **Explicación Técnica** (4 min)

   - **Kanban:** Gestión del trabajo
   - **GitHub Actions:** 4 workflows (ci, release_analysis, build_scan_sbom, deploy_dummy)
   - **Docker/Compose:** Arquitectura
   - **Seguridad:** SBOM, Trivy, evidencias
   - **(Opcional) K8s:** Si implementaron

5. **Evidencias** (1 min)

   - Mostrar carpeta `.evidence/` con 5 archivos
   - Explicar qué genera cada workflow

6. **Conclusión** (1 min)
   - Valor de negocio
   - Extensiones futuras

---

**¿Necesitas el contenido de algún archivo del Sprint 3 ahora o prefieres esperar a avanzar?**
