# Auditoría OpenClaw — Diagnóstico y Recomendaciones

**Fecha:** 17 de agosto de 2026
**Autor:** Consultor de optimización OpenClaw (subagente)
**Alcance:** Diagnóstico de nuestra instalación + casos de uso reales de la comunidad + lista priorizada de recomendaciones.

---

## SECCIÓN 1 — Diagnóstico de nuestro sistema

### 1.1 Estado de la instalación

| Componente | Estado |
|---|---|
| Versión | OpenClaw `2026.7.1-2` (canal stable, deps OK) |
| Gateway | Local, `ws://127.0.0.1:18789`, auth token, systemd user activo |
| SO | Linux 5.15 (Ubuntu) · Node 22.22.3 |
| Dashboard | `http://127.0.0.1:18789` |
| Canal | Telegram (único, directo, SETUP OK) |
| Modelo | `deepseek-v4-flash` (main) · fallback `mimo-v2.5` |
| Sesiones | 36 activas · `~/.openclaw/agents/main/sessions/` |
| Memoria | Plugin `memory-core` activo · **dreaming DESACTIVADO** |
| Heartbeat | 30 min (main) · **HEARTBEAT.md vacío** |
| Tasks | 2 running · 40 tracked · audit clean |
| Tailscale | OFF (exposición de red no usada) |

### 1.2 Automatización actual (ya robusta)

Tenemos **9 cron jobs activos** (más que la media de usuarios):

1. `Lectura Diaria` — 6:00 AM diario (mimo)
2. `Check-in Adaptativo Mañana` — 5:55 AM
3. `Check-in Adaptativo Mediodía` — 12:30 L-V
4. `Check-in Adaptativo Tarde` — 6:00 PM L-V
5. `End-of-Day Auto-Gestión` — 11:55 PM
6. `Weekly Planning` — 8:00 PM domingo
7. `Arya — Crear Recordatorios del Día` — 12:05 AM
8. `Balancear Ingresos` — 7:00 PM viernes
9. `Reminder Ajustes End-of-Day` — **DESACTIVADO**

**Fortalezas:** rutinas diarias bien cubiertas, recordatorios Arya funcionales, lectura diaria automática, planificación semanal, balance de ingresos.

### 1.3 Skills activas vs. disponibles

**Activas (en uso):**
- `arya-reminders` (workspace) — recordatorios cron
- `humanizer` (workspace) — quitar patrones IA
- `productivity-automation-kit` (workspace) — plantillas/automatización
- `gog` (bundled) — Gmail/Calendar/Drive/Sheets/Docs
- `weather` (bundled) — clima Medellín
- `healthcheck` (bundled) — auditoría servidor
- `session-logs` (bundled) — debug de sesiones
- `browser-automation` (plugin) — control de navegador
- `canvas` (plugin) — presentar HTML en nodos

**39 skills bundled DESACTIVADAS** (inventario de infrautilizadas):
`obsidian`, `notion`, `github`, `gh-issues`, `trello`, `mcporter` (MCP), `summarize`, `spike`, `taskflow`, `taskflow-inbox-triage`, `diagram-maker`, `meme-maker`, `coding-agent`, `nano-pdf`, `model-usage`, `gemini`, `gifgrep`, `goplaces`, `himalaya` (email), `1password`, `openai-whisper`, `sherpa-onnx-tts`, `spotify-player`, `sonoscli`, `voice-call`, `xurl`, `oracle`, `sag`, `peekaboo`, `camsnap`, `blucli`, `eightctl`, `ordercli`, `blogwatcher`, `things-mac`, `apple-*`, `bear-notes`, `slack`, `discord`, `wacli`, `imsg`, `qqbot`.

### 1.4 Capacidades de OpenClaw que NO aprovechamos

Con `tools.profile: "coding"`, YA tenemos disponibles (pero no usamos):
- **`image_generate`** — generación/edición de imágenes (configurado: `gemini-3.1-flash-image-preview` + fallbacks)
- **`music_generate`** — generación de música
- **`video_generate`** — generación de video (16 backends)
- **`skill_workshop`** — crear/actualizar skills desde el chat con gobernanza
- **`subagents` / `sessions_spawn`** — subagentes en background (paralelizar investigación)
- **`taskflow`** — orquestación durable multi-paso
- **`browser`** — automatización de navegador (login, scraping, flujos web)
- **`canvas`** — mostrar HTML/dashboards en nodos
- **`create_goal` / `update_goal`** — objetivos con presupuesto de tokens
- **`update_plan`** — planes de tareas multi-paso
- **`video-frames`** — extraer frames/clips de video (bundled)

**Infrautilizado específicamente:**
- **Dreaming (memory-core) DESACTIVADO** — consolida memoria automáticamente en background. Tenemos `memory/.dreams/` y `DREAMS.md` (89KB) pero el sweep no corre.
- **HEARTBEAT.md vacío** — el heartbeat (30 min) no hace NADA útil; se desperdicia un ciclo de contexto completo.
- **QMD** — motor de búsqueda semántica del vault instalado y documentado en TOOLS.md, pero solo se usa bajo demanda.
- **gog** — configurado con Google pero sin evidencia de automatización de calendario/email/Sheets activa (solo lectura puntual).
- **39 skills bundled** desactivadas — incluyendo `obsidian` y `notion` que son directamente relevantes a nuestro vault.
- **`browser`** — skill instalada pero sin flujos activos (scraping de Meta Ads, verificación de productos, etc.).
- **`image_generate` / `video_generate` / `music_generate`** — configurados pero sin uso para el contenido del MODO FANTASMA (fase Crear/Capturar).
- **`skill_workshop`** — sin propuestas; no creamos skills nuevas desde el chat.
- **`subagents`** — no usamos paralelización para investigación larga.

### 1.5 Vault Obsidian (sistema de tareas)

- `obsidian-vault/tasks.md` = fuente única de verdad de tareas (sync dual-push submodule).
- `vault-index.json` con `tasksHash`/`tasksSnapshot` para detección reactiva de cambios.
- QMD indexa `vault` y `memory` colecciones.
- **Brecha:** la skill bundled `obsidian` está desactivada (usa el CLI oficial `obsidian`), y `notion` también.

---

## SECCIÓN 2 — Casos de uso de otros usuarios (con fuentes)

> Nota: `web_search` estaba deshabilitado en esta sesión; verifiqué todo vía `web_fetch` directo a docs oficiales (docs.openclaw.ai), el repo GitHub, el showcase oficial y ClawHub. Todo lo citado es real y verificado.

### 2.1 Patrones de automatización documentados (docs oficiales)

La [guía de Automatización](https://docs.openclaw.ai/automation) define el árbol de decisión que la comunidad usa:
- **Automations (cron)** para timing exacto → ya lo usamos bien.
- **Heartbeat** para checks periódicos flexibles (inbox, calendario) → **no lo usamos**.
- **Task Flow** para orquestación durable multi-paso → no lo usamos.
- **Hooks** para reaccionar a eventos de ciclo de vida (`/new`, `/reset`, `/stop`) → no lo usamos.
- **Standing Orders** (en `AGENTS.md`) para autoridad operativa permanente → parcial (nuestro AGENTS.md tiene reglas, pero no "programas" de standing orders formales).

### 2.2 Showcase oficial (proyectos reales de la comunidad) — [docs.openclaw.ai/start/showcase](https://docs.openclaw.ai/start/showcase)

| Proyecto | Autor | Patrón que ilustra | Relevancia para nosotros |
|---|---|---|---|
| **Tesco Shop Autopilot** | @marchattonhere | Automatización de compras vía **browser control** sin APIs | Compras/entrega automatizadas |
| **PR Review → Telegram** | @bangnokia | OpenCode + OpenClaw revisa diffs y responde en Telegram | Revisión de código en canal |
| **Wine Cellar Skill** | @prades_maxime | Le pidió al agente **crear una skill local desde CSV** en minutos | Crear skills desde chat (skill_workshop) |
| **Mailbox broker para sub-agentes** | @albzhu | Callback async para que sub-agentes no bloqueen al orquestador | Subagentes orquestados |
| **GA4 analytics skill** | @jdrhyne | OpenClaw **construyó su propia skill** y la publicó en ClawHub | Skills auto-generadas |
| **Music Craft** | @luischarro | Generación de música provider-agnostic | `music_generate` para contenido |
| **Dropage deploy** | @jiantoucn | "Deploy este HTML" → URL pública en 1s | Deploy rápido de prototipos |
| **Anti-scam URL checker** | @phishguard-niki | Verificación de URLs (2.5M dominios) | Seguridad |
| **tokenomics cost tracker** | @ncz-os | Rastreo de costo por modelo/sesión | Control de gasto de tokens |
| **Excalidraw diagram generator** | @swiftlysingh | Diagramas desde chat | `diagram-maker` |
| **lite-mode** | @mirajmahmudul | Mantener OpenClaw en máquinas de 2-4GB | Relevante (nuestro VPS 8GB) |
| **Self Improving Agent** | @xiucheng | Analiza calidad de conversación y se auto-mejora | Mejora continua |

### 2.3 ClawHub — skills de la comunidad (fuente: [clawhub.ai](https://clawhub.ai))

Skills populares y sus categorías (verificadas en el hub):
- **Finance**: `finance@anton-roos` (13.6k instalaciones — stocks/ETF/crypto/FX), `finance-lite` (daily macro brief FRED), `candor-finance` (finanzas personales), `koompi-finance` (AP/AR, facturación), `quickbooks-finance`.
- **Video/Imagen**: `ai-video-generation`, `video-edit` (RunComfy), `ai-image-generation`, `dreamina-image-generation-editing`.
- **Productividad/Dev**: `find-skills`, `superpowers` (spec-first/TDD/subagent-driven), `ocr-local` (Tesseract, sin API), `grill-me` (interrogar planes).
- **Automatización**: `reddit-automation`, `agent-browser` (headless browser CLI).
- **Proactividad**: `proactive-agent-lite` (de task-follower a proactivo con memoria).

### 2.4 Patrones de alto valor que otros maximizan

1. **Memory consolidation automática** — la comunidad habilita `dreaming` para que la memoria se consolide sola en background (nosotros lo tenemos OFF).
2. **Heartbeat productivo** — en vez de vacío, otros lo usan para revisar inbox/calendario/notificaciones cada 30 min.
3. **Skills auto-generadas** — pedir al agente que cree skills nuevas desde el chat (skill_workshop), no esperar a que existan.
4. **Subagentes paralelos** — para investigación larga, el agente lanza sub-agentes aislados que anuncian resultados al canal.
5. **Browser automation** — automatizar sitios web sin API (compras, scraping, bookings) — el patrón "Tesco Autopilot".
6. **Generación de medios** — usar image/video/music_generate para contenido, no solo texto.
7. **Modelos baratos para subagentes/cron** — la comunidad asigna modelos más baratos a tareas de background y mantiene el modelo caro solo para el main (nosotros ya usamos mimo para cron — buen patrón).
8. **Standing Orders** — autoridad operativa permanente en AGENTS.md para que el agente actúe solo en dominios definidos.

---

## SECCIÓN 3 — Lista priorizada de recomendaciones

Criterio: **Impacto alto + esfuerzo bajo primero.** Cada recomendación: qué, por qué, cómo, impacto.

### 🥇 PRIORIDAD ALTA — Impacto alto, esfuerzo bajo

#### R1. Activar Dreaming (memory-core)
- **Qué:** Habilitar el sweep de consolidación de memoria en background (light → REM → deep).
- **Por qué:** Ya tenemos `memory/.dreams/` y `DREAMS.md` (89KB) pero el sweep está OFF. La memoria se consolida solo y promueve lo importante a `MEMORY.md` sin intervención.
- **Cómo:**
  ```bash
  openclaw config set plugins.entries.memory-core.config.dreaming.enabled true
  ```
  (o vía Control UI → Config). Ajustar `memory-core` dreaming schedule si existe.
- **Impacto:** Memoria a largo plazo más rica y automática; menos trabajo manual de compactación en AGENTS.md.

#### R2. Hacer productivo el Heartbeat (30 min)
- **Qué:** Poblar `HEARTBEAT.md` con checks periódicos flexibles en vez de dejarlo vacío.
- **Por qué:** El heartbeat ya corre cada 30 min con contexto completo del main; hoy no hace nada. Es capacidad desperdiciada.
- **Cómo:** Añadir a `HEARTBEAT.md` tareas ligeras como: "Si hay correos nuevos no leídos de X, resumir"; "Revisar si tasks.md tiene tareas vencidas y avisar"; "Si el clima cambió drásticamente en Medellín, avisar". Mantenerlo corto (2-4 checks).
- **Impacto:** Proactividad real sin cron extra; el agente "vigila" cosas por ti.

#### R3. Activar la skill bundled `obsidian`
- **Qué:** Habilitar la skill oficial de Obsidian (CLI `obsidian`) para trabajar el vault de forma nativa.
- **Por qué:** Tenemos un vault Obsidian como submodule y hoy lo manejamos con edición de archivos + QMD. El CLI oficial da búsqueda/creación/edición de notas, tareas, links y propiedades de forma estructurada.
- **Cómo:**
  ```bash
  openclaw config set skills.entries.obsidian.enabled true
  ```
  Requiere `obsidian` CLI instalado y app corriendo (en servidor headless puede no aplicar — **verificar**; si no hay GUI, la skill no es viable). Alternativa: mantener QMD + edición directa.
- **Impacto:** Integración más profunda con el vault si el CLI está disponible; si no, descartar sin pérdida.

#### R4. Usar `image_generate` en el MODO FANTASMA (fase Crear/Capturar)
- **Qué:** Aprovechar la generación de imágenes ya configurada (`gemini-3.1-flash-image-preview` + fallbacks) para el micro-proyecto diario.
- **Por qué:** Está configurado pero sin uso. La fase "Crear" (L: Diseño/Branding, V: Video, etc.) se beneficia de assets visuales generados.
- **Cómo:** En el cron del MODO FANTASMA, añadir paso opcional de "generar 1 imagen de apoyo" usando `image_generate`. También para thumbnails de contenido e-commerce.
- **Impacto:** Contenido visual real para e-commerce/branding sin herramientas externas.

#### R5. Activar `summarize` y `nano-pdf` (skills bundled)
- **Qué:** Habilitar resumen de documentos y manejo de PDFs.
- **Por qué:** Mr. Jair lee contenido diario y trabaja con documentos (finanzas, e-commerce). Resumir PDFs/artículos ahorra tiempo.
- **Cómo:**
  ```bash
  openclaw config set skills.entries.summarize.enabled true
  openclaw config set skills.entries.nano-pdf.enabled true
  ```
- **Impacto:** Lectura diaria más eficiente; análisis de documentos financieros.

### 🥈 PRIORIDAD MEDIA — Impacto medio-alto, esfuerzo medio

#### R6. Usar subagentes para investigación paralela
- **Qué:** Lanzar sub-agentes (`sessions_spawn`) para tareas largas de investigación (ej: "10 productos ganadores Meta Ads").
- **Por qué:** La investigación de productos/mercado es lenta y bloqueante en el main. Los sub-agentes corren en background y anuncian resultados al canal.
- **Cómo:** En cron o a petición, que el agente lance 2-3 sub-agentes con modelo barato (`mimo` o `deepseek-v4-flash`) para investigar nichos/productos en paralelo. Ver `docs/tools/subagents.md`.
- **Impacto:** Investigación de e-commerce mucho más rápida y paralela.

#### R7. Crear skills propias vía `skill_workshop`
- **Qué:** Usar el Skill Workshop para que el agente cree skills reutilizables desde el chat (patrón "Wine Cellar Skill").
- **Por qué:** Tenemos la herramienta pero 0 propuestas. Ej: una skill "Análisis de productos ganadores" o "Registro de gastos diarios" que encapsule el flujo.
- **Cómo:** Pedir en el chat: "Crea una skill que haga X". El agente genera una propuesta; se revisa y aplica. Gobernanza incluida (scanner, rollback).
- **Impacto:** Automatización reutilizable sin escribir código manual.

#### R8. Activar `taskflow` para flujos multi-paso durables
- **Qué:** Usar Task Flow para pipelines de varios pasos (ej: recopilar datos → generar reporte → entregar).
- **Por qué:** Nuestros cron jobs son de un solo turno. Para flujos que sobreviven reinicios y tienen estado, Task Flow es superior.
- **Cómo:** Para el reporte semanal o el balance de ingresos, estructurarlo como flow de 3 pasos. Ver `docs/automation/taskflow.md`.
- **Impacto:** Flujos robustos y auditables.

#### R9. Usar `browser` para automatizar sitios web sin API
- **Qué:** Automatizar flujos web (patrón "Tesco Autopilot") — ej: verificar precios de productos, chequear disponibilidad, scraping de nichos.
- **Por qué:** La skill `browser-automation` está instalada. Para e-commerce, automatizar búsquedas de productos ganadores o seguimiento de precios.
- **Cómo:** Configurar un perfil de navegador y pedir al agente que haga flujos multi-paso (login, búsqueda, extracción). Ver `docs/tools/browser.md`.
- **Impacto:** Datos de mercado reales sin APIs de pago.

#### R10. Activar `model-usage` para control de gasto
- **Qué:** Habilitar la skill que rastrea uso/costo de modelos.
- **Por qué:** Con 9 cron jobs + heartbeat + subagentes, el gasto de tokens crece. Controlarlo evita sorpresas.
- **Cómo:**
  ```bash
  openclaw config set skills.entries.model-usage.enabled true
  ```
- **Impacto:** Visibilidad del gasto por modelo/sesión.

### 🥉 PRIORIDAD BAJA — Impacto medio, esfuerzo alto / opcional

#### R11. Activar `notion` o `trello` para proyectos
- **Qué:** Integrar Notion o Trello si Mr. Jair quiere gestión de proyectos fuera del vault.
- **Por qué:** Solo si hay necesidad. El vault ya cubre tareas. Opcional.
- **Cómo:** Configurar token de Notion (`NOTION_API_TOKEN`) o cuenta Trello.
- **Impacto:** Gestión de proyectos alternativa si se desea.

#### R12. Activar `video_generate` para contenido de video
- **Qué:** Generar videos cortos (16 backends) para el pilar de edición de video / e-commerce.
- **Por qué:** Mr. Jair tiene interés en edición de video. Generar clips B-roll o promos.
- **Cómo:** Configurar un provider de video (requiere API key de un backend soportado). Ver `docs/tools/video-generation.md`.
- **Impacto:** Contenido de video generado para redes/e-commerce.

#### R13. Activar `meme-maker` y `diagram-maker` para contenido
- **Qué:** Generar memes y diagramas desde el chat.
- **Por qué:** Rápido contenido social y diagramas de arquitectura (ej: Prototipo X, Ghost Trader).
- **Cómo:** Habilitar skills bundled.
- **Impacto:** Contenido social y documentación visual.

#### R14. Configurar hooks para eventos de ciclo de vida
- **Qué:** Usar hooks para loguear/limpiar en `/new`, `/reset`, `/stop`.
- **Por qué:** Buenas prácticas de higiene de sesión. Opcional.
- **Cómo:** `openclaw hooks enable session-memory` y revisar `openclaw hooks list`.
- **Impacto:** Sesiones más limpias, memoria de sesión persistida.

#### R15. Exponer Tailscale para acceso remoto seguro
- **Qué:** Activar Tailscale para acceder al dashboard/control desde fuera.
- **Por qué:** Solo si Mr. Jair quiere gestionar el servidor remotamente. Es una mejora de conveniencia, no de capacidad.
- **Cómo:** `openclaw config set gateway.tailscale.mode on` (requiere cuenta Tailscale).
- **Impacto:** Acceso remoto seguro al control UI.

---

## 🎯 CONCLUSIÓN — Las 5 acciones de mayor impacto a implementar primero

1. **Activar Dreaming** (`memory-core`) → memoria auto-consolidada, menos trabajo manual. *(Impacto alto, esfuerzo mínimo)*
2. **Poblar `HEARTBEAT.md`** con checks periódicos → el heartbeat de 30 min deja de desperdiciarse y el agente se vuelve proactivo. *(Impacto alto, esfuerzo mínimo)*
3. **Activar `image_generate` en MODO FANTASMA** → contenido visual real ya configurado pero sin usar; potencia e-commerce/branding. *(Impacto alto, esfuerzo bajo)*
4. **Usar subagentes para investigación paralela** (productos ganadores Meta Ads, nichos) → e-commerce más rápido. *(Impacto alto, esfuerzo medio)*
5. **Activar `summarize` + `nano-pdf`** → lectura diaria y análisis de documentos más eficientes. *(Impacto medio-alto, esfuerzo bajo)*

**Orden de ejecución sugerido:** R1 → R2 → R5 → R4 → R6 (todas de bajo riesgo, reversibles vía `openclaw config`).

---

### Fuentes verificadas
- Docs oficiales: `docs.openclaw.ai/automation`, `/start/showcase`, `/help/faq`, `/concepts/memory`, `/concepts/dreaming`, `/tools/subagents`, `/tools/skill-workshop`, `/tools/image-generation`, `/tools/video-generation`, `/gateway/configuration`
- Repo: `github.com/openclaw/openclaw` (README, 346k+ stars)
- Hub de skills: `clawhub.ai` (finance, video, imagen, productividad)
- Docs locales: `/root/.nvm/versions/node/v22.22.3/lib/node_modules/openclaw/docs/`
- Config local: `/root/.openclaw/openclaw.json`, `openclaw status`

*Nota: `web_search` no estaba disponible en esta sesión; toda la investigación de la FASE 2 se hizo por `web_fetch` directo a fuentes oficiales y el hub de la comunidad. Las capacidades citadas (dreaming, taskflow, subagents, skill_workshop, image/video/music_generate, browser, hooks, standing orders) están confirmadas en la documentación oficial y en la configuración local.*
