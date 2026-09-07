---
title: "OpenClaw — Capacidades Completas"
date: 2026-09-07
tags: [openclaw, sistema, referencia, automatizacion]
aliases: [OpenClaw Capacidades]
---

# 🦞 OpenClaw — Capacidades Completas

> **Versión documentada:** `2026.7.1-2` (0790d9f) · Fecha: 2026-09-07 · Fuente: docs, `openclaw --help`, `package.json`, config viva del host.

## Qué es OpenClaw

OpenClaw es un **gateway auto-hospedado** (self-hosted) que conecta tus apps de mensajería — Telegram, WhatsApp, Discord, Slack, Signal, iMessage, WebChat y 20+ más vía plugins — con agentes de IA con uso de herramientas (tool use), sesiones, memoria y automatización. Corre como un único proceso Gateway en tu máquina o servidor y actúa como puente entre cualquier canal y un asistente siempre disponible que puedes contactar desde el bolsillo. Es open source (MIT), multi-agente y extensible vía plugins y skills.

---

## 1. Gateway — Núcleo del sistema

- **Proceso único** (`openclaw gateway run`) que centraliza sesiones, ruteo, conexiones de canal y scheduling. Persiste estado en SQLite (`~/.openclaw/openclaw.json` + `openclaw-agent.sqlite`).
- **Modos:** `local` (por defecto), remoto, trusted-proxy; auth por token/password/none.
- **Bind:** loopback / lan / tailnet / auto / custom; soporte Tailscale serve/funnel.
- **Control UI** en `http://127.0.0.1:18789` (dashboard, config, sesiones, nodos).
- **Hot reload** de config + validación estricta (rechaza claves desconocidas).
- **CLI:** `openclaw gateway {run,status,health,discover,call,install,start,stop,restart}`, `openclaw health`, `openclaw status`, `openclaw logs`, `openclaw doctor --fix`.
- **APIs HTTP:** OpenAI-compatible y OpenResponses, tools-invoke, discovery/Bonjour.
- **Seguridad:** sandboxing, tool policy, exec approvals, secrets, operator scopes, sandbox-vs-policy-vs-elevated bien documentado.

> **Uso para Mr. Jair:** Gateway en el VPS actual (`port 18789`, `bind loopback`, auth token). Control UI para monitorear sesiones y cron sin tocar SSH.

---

## 2. Mensajería — Canales

**Core (sin plugin):** WebChat, Telegram (grammY Bot API), iMessage (bridge `imsg` en Mac).

**Plugins oficiales** (`openclaw plugins install @openclaw/<id>` + restart):
Discord, Feishu, Google Chat, IRC, LINE, Matrix, Mattermost, MS Teams, Nextcloud Talk, Nostr, QQ Bot, Raft, Signal (signal-cli), Slack (Bolt), SMS (Twilio), Synology Chat, Tlon, Twitch, Voice Call (Plivo/Telnyx/Twilio), WhatsApp (Baileys + QR), Zalo, Zalo Personal.

**Externos:** WeChat, Yuanbao, Zalo ClawBot.

**Features:** grupos con activación por mención, DMs con allowlist/pairing, bot-loop protection, ambient room events, soporte media/reacciones (varía por canal), broadcast, polls, threads, pins.

**CLI:** `openclaw channels {list,status,add,login,logout,resolve}`, `openclaw message {send,read,react,poll,thread,delete,edit,pin}`.

> **Uso para Mr. Jair:** Telegram ya operativo como canal principal. WhatsApp disponible vía QR si quiere segundo canal. `openclaw message send --target <id> --message "..." --media foto.jpg` para envíos programáticos.

---

## 3. Automatización

### 3.1 Cron — Scheduled Tasks (`openclaw cron`)
Scheduler dentro del Gateway. Persiste jobs y run history en SQLite; sobrevive reinicios.

- **Tipos de schedule:** `at` (one-shot ISO/relativo), `every` (intervalo `10m/1h/1d`), `cron` (expr 5-6 campos + `--tz`), `on-exit` (al salir un comando).
- **Payloads:** `--system-event` (encola en main session), `--message` (turn con modelo), `--command`/`--command-argv` (shell en el host, sin modelo).
- **Opciones agent-turn:** `--model`, `--fallbacks`, `--session {isolated,main,custom}`, `--timeout-seconds`, `--delete-after-run`, `--exact`/`--stagger`.
- **Triggers condicionales:** script JS headless que retorna `{fire, message?, state?}` evaluado en cada tick; útil para watchers (ej: estado de PR).
- **Comandos:** `cron {add,list,get,show,runs,status,enable,disable,edit,rm,run}`.

### 3.2 Heartbeat
Turn periódico en la sesión principal (default `30m`, `1h` con Anthropic OAuth). No crea tasks. Ideal para batch de checks (inbox, calendario, notificaciones) con contexto completo. Configurable vía `HEARTBEAT.md` y `agents.defaults.heartbeat`.

### 3.3 Tasks — Background Task Ledger (`openclaw tasks`)
Registro de trabajo desacoplado: ACP runs, sub-agentes, cron aislados, CLI. Estados `queued → running → terminal (succeeded/failed/timed_out/cancelled/lost)`. Retención 7 días (lost: 24h). Comandos: `tasks {list,show,cancel,audit,flow}`.

### 3.4 TaskFlow
Orquestación durable multi-paso sobre tasks, con revision tracking y modos managed/mirrored. Para flujos tipo "investigar → resumir → notificar".

### 3.5 Hooks y Standing Orders
- **Hooks:** scripts disparados por eventos de ciclo de vida (`/new`, `/reset`, `/stop`, compaction, startup, message flow). Gestión: `openclaw hooks`.
- **Standing Orders:** instrucciones permanentes inyectadas cada sesión (viven en `AGENTS.md` u otros workspace files). Combinables con cron.

### 3.6 Commitments (Inferred)
Follow-ups cortos inferidos de la conversación (ej: "preguntar cómo salió la entrevista mañana"), scoped por agente+canal, entregados vía heartbeat. Para recordatorios exactos usar cron.

> **Uso para Mr. Jair:** Ya usa cron para tareas de `mision.md` con hora (`— HH:MM`). Heartbeat para chequeos diarios. TaskFlow si quiere orquestar "Ghost Trader: backtest → reporte → alerta Telegram".

---

## 4. Memoria y Búsqueda

### Modelo de memoria
Archivos Markdown en el workspace (`~/.openclaw/workspace`):
- `MEMORY.md` — memoria largo plazo (hechos durables, preferencias, decisiones). Inyectada al inicio de cada sesión.
- `memory/YYYY-MM-DD.md` — notas diarias (contexto operativo). Indexadas para búsqueda, no inyectadas por defecto.
- `DREAMS.md` — diario de sueños / resúmenes REM (opcional).

### Memory Search (`memory_search` / `memory_get`)
Búsqueda híbrida: similitud vectorial + keywords (BM25). Chunking automático.

- **Providers soportados:** OpenAI (default), Gemini, Voyage, Mistral, Bedrock, DeepInfra, local GGUF (llama.cpp), Ollama, LM Studio, GitHub Copilot, OpenAI-compatible. Config: `agents.defaults.memorySearch.provider`.
- **QMD local (host actual):** `@tobilu/qmd` v2.5.3 con `embeddinggemma-300M-Q8_0.gguf` (CPU, sin API key). Índice en `/root/.cache/qmd/index.sqlite`. Colecciones `vault` (obsidian-vault) y `memory` (MEMORY.md + memory/). Comandos: `qmd search/vsearch/query/get/ls/status/update+embed`.
- **CLI:** `openclaw memory {search,status,index,promote,promote-explain,rem-harness,rem-backfill}`.

> **Uso para Mr. Jair:** `qmd search "Ghost Trader" --json -n 5` antes de cualquier grep en el vault. `memory_search` para que el agente recuerde preferencias/decisiones entre sesiones.

---

## 5. Skills — Paquetes de instrucciones

Archivos `SKILL.md` (frontmatter YAML + markdown) que enseñan al agente **cómo** usar sus tools con workflows repetibles.

- **Orden de carga (precedencia):** workspace/skills > .agents/skills > ~/.agents/skills > ~/.openclaw/skills > bundled > extraDirs + plugin skills.
- **Allowlist por agente:** `agents.defaults.skills` y `agents.list[].skills`.
- **Gestión:** `openclaw skills {list,info,check,install,search,update,verify,workshop}`. ClawHub como catálogo.
- **Skills activos en este host (21/55 ready):** `browser-automation`, `canvas`, `clawhub`, `diagram-maker`, `gog` (Google Workspace), `healthcheck`, `humanizer`, `meme-maker`, `node-connect`, `node-inspect-debugger`, `notion`, `productivity-automation-kit`, `python-debugpy`, `session-logs`, `skill-creator`, `spike`, `taskflow`, `taskflow-inbox-triage`, `tmux`, `video-frames`, `weather` (+ `clawhub`, `diagram-maker`, etc.).
- **Skills bundled deshabilitados (requieren credenciales/plataforma):** 1password, apple-notes/reminders, bear-notes, github, coding-agent, gemini, etc. — habilitables a demanda.

> **Uso para Mr. Jair:** `gog` para Gmail/Calendar/Drive/Sheets, `notion` para Notion, `productivity-automation-kit` para workflows de eficiencia, `skill-creator` para crear skills propias (ej: "Ghost Trader ops").

---

## 6. Plugins — Extensibilidad

Añaden channels, providers, tools, skills, speech/TTS/STT, media generation, web search/fetch, hooks.

- **Instalación:** `openclaw plugins {search,install,enable,disable,list}` desde ClawHub / npm / git / local. Requiere restart del Gateway.
- **Bundled plugins:** browser, y decenas de providers/channels empaquetados.
- **Catálogo:** `openclaw plugins search "calendar"` → ClawHub.
- **SDK:** `openclaw/plugin-sdk` para autores (contracts, tools, hooks, manifest).

> **Uso para Mr. Jair:** Instalar solo lo necesario (ej: `@openclaw/github` si quiere gestión de repos, `@openclaw/llama-cpp-provider` para embeddings 100% locales).

---

## 7. Tools — Superficie de herramientas del agente

Categorías (visibles según `tools.profile`, `tools.allow/deny`, provider, sandbox, canal):

| Categoría | Para qué | Tools representativos |
|-----------|----------|-----------------------|
| Runtime | Comandos y procesos | `exec`, `process`, `code_execution` |
| Files | Leer/escribir workspace | `read`, `write`, `edit`, `apply_patch` |
| Web | Buscar y fetchear | `web_search`, `web_fetch`, `x_search` |
| Browser | Automatizar navegador | `browser` (Chrome dedicado) |
| Messaging | Responder en el canal | `message` |
| Sessions/Agents | Sesiones y delegación | `sessions_*`, `subagents`, `get_goal`, `create_goal`, `update_goal`, `session_status` |
| Automation | Scheduling | `cron`, `heartbeat_respond` |
| Gateway/Nodes | Estado del gateway/nodos | `gateway`, `nodes` |
| Media | Generar/entender media | `image`, `image_generate`, `music_generate`, `video_generate`, `tts` |
| Tool Search | Catálogos grandes | `tool_search`, `tool_describe` |

**Perfiles:** `tools.profile: "coding"` (actual en este host) incluye `web_search`/`web_fetch` pero no `browser` por defecto — añadir con `alsoAllow: ["browser"]` si se necesita.

---

## 8. Browser Automation

Navegador dedicado (perfil `openclaw`, Chromium/Chrome/Brave/Edge) aislado del navegador personal, controlado vía Gateway (loopback).

- **Acciones:** `open/navigate`, `snapshot` (AI/aria), `click/type/fill/select/drag/hover`, `screenshot`, `pdf`, `evaluate`, `tabs/focus/close`, `cookies/storage`, `download/waitfordownload`, `trace`.
- **CLI:** `openclaw browser {status,start,stop,open,snapshot,screenshot,tabs,click,type, ...}` con `--browser-profile`.
- **Skill:** `browser-automation` enseña el loop snapshot → stable-tab → stale-ref recovery.

> **Uso para Mr. Jair:** Automatizar consultas web que requieren login/interacción (ej: dashboards de trading, Meta Ads) sin exponer su perfil personal.

---

## 9. Canvas y Nodes

### Canvas
Renderiza HTML en nodos conectados (iOS/Android/macOS) vía `canvas.*`. Útil para dashboards, diagramas, UIs interactivas. Skill `canvas` + CLI `openclaw nodes`.

### Nodes (dispositivos compañeros)
- **Tipos:** iOS, Android, macOS (menubar app), headless (`openclaw node run`).
- **Conexión:** WebSocket al Gateway con `role: node`; pairing por `openclaw devices {list,approve,reject}` + `openclaw nodes {status,describe,remove}`.
- **Comandos expuestos:** `canvas.*`, `camera.*` (snap/clip), `device.*`, `notifications.*`, `system.*` (`system.run`/`system.which` para exec remoto), `screen.record`, etc.
- **Node host remoto:** Gateway recibe el mensaje, reenvía `exec` al node host si `host=node`. Approvals se enforcean en el host del nodo.

> **Uso para Mr. Jair:** Nodo iOS ya vinculado para Obsidian + Telegram. Canvas para presentar reportes visuales; `system.run` si quiere que el Gateway delegue cómputo a otro host.

---

## 10. Sub-agentes y Sesiones

- **Sub-agentes:** runs en background en sesión `agent:<id>:subagent:<uuid>`, no bloquean el main. Cada uno es un background task. Spawn vía `sessions_spawn`; resultados hacen push al requester. Soporta `sessions_yield` para esperar. Anidados con depth configurable. Sin `message` tool por defecto (devuelven texto al padre).
- **Sesiones:** chats directos colapsan en `main`; grupos aislados. Scopes: `per-channel-peer` (actual). Comandos: `/subagents`, `/focus`, `/unfocus`, `/agents`, `openclaw sessions`, `openclaw transcripts`.
- **Goals:** `create_goal`/`get_goal`/`update_goal` para objetivos durables con presupuesto de tokens.

> **Uso para Mr. Jair:** Delegar investigación paralela (ej: comparar modelos LLM, scrapear 3 fuentes a la vez) sin bloquear la conversación principal.

---

## 11. Media — Generación y Comprensión

| Capacidad | Tool | Modo | Providers (ejemplos) |
|-----------|------|------|----------------------|
| Imagen | `image_generate` | async (background task) | OpenAI, Google, fal, DeepInfra, ComfyUI, OpenRouter |
| Video | `video_generate` | async | fal, Google (Veo), Runway, PixVerse, Alibaba, BytePlus |
| Música/Audio | `music_generate` | async | fal, MiniMax, ComfyUI, Google |
| TTS | `tts` | sync | ElevenLabs, OpenAI, Google, Azure Speech, DeepInfra |
| STT | (inbound voice) | batch/streaming | Deepgram (nova-3/es activo), Whisper, Google |
| Media understanding | `image` (análisis) | sync | Vision models (Anthropic, OpenAI, Google, etc.) |
| Realtime voice | Talk sessions | realtime | Google (Gemini Live), OpenAI Realtime |

> **Uso para Mr. Jair:** `image_generate` para creativos de Meta Ads, `video_generate` para prototipos, `tts` para respuestas por voz, `image` para analizar screenshots de dashboards.

---

## 12. Modelos y Providers

- **35+ providers:** Anthropic, OpenAI, Google, DeepSeek, OpenRouter, Groq, Cerebras, Mistral, xAI, Bedrock, Ollama, LM Studio, llama.cpp, vLLM, SGLang, etc. + self-hosted OpenAI/Anthropic-compatible.
- **Auth:** API keys, OAuth (ej: OpenAI Codex), tokens. Store en `openclaw-agent.sqlite` + env.
- **Este host:** `openrouter/meta/muse-spark-1.2-contributor` (primary, reasoning high), aliases `mimo` (xiaomi/mimo-v2.5) y `dsv4` (deepseek-v4-flash), fallbacks `openrouter/free`. Deepgram + DeepSeek + Google + OpenRouter autenticados.
- **CLI:** `openclaw models {list,status,scan,set,aliases,fallbacks}`, `openclaw infer {model,image,video,tts,web,audio,embedding}`.

> **Uso para Mr. Jair:** Cambiar modelo con `/model mimo|spark|dsv4`. Cron y sub-agentes heredan el modelo activo. Usar `dsv4` para tareas baratas de alto contexto, `spark` para reasoning.

---

## 13. Web Search y Fetch

**Search providers (plugins):** Brave, DuckDuckGo, Exa, Firecrawl, Gemini Search, Grok, Kimi, MiniMax, Ollama Web Search, Perplexity, SearXNG, Tavily. Tools: `web_search`, `x_search`, `brave-search`, `tavily`, etc.

**Fetch:** `web_fetch` (markdown/text, `maxChars`), `web` tools, Firecrawl.

> **Uso para Mr. Jair:** Research de mercado, validación de estrategias de trading, monitoreo de noticias.

---

## 14. Seguridad, Sandbox y Aprobaciones

- **Sandbox:** per-agent, con `workspaceRoot` para sesiones no-main.
- **Tool policy:** `tools.allow/deny`, `tools.profile`, `alsoAllow`, restricciones por provider/canal.
- **Exec approvals:** `openclaw approvals` / `exec-approvals` — bind de contexto exacto, re-validación de cwd/archivo antes de ejecutar.
- **Elevated exec:** ejecución controlada fuera del sandbox.
- **Secrets:** `openclaw secrets`, `secretref` conventions, placeholders `***`.
- **Healthcheck skill:** audita SSH, firewall, updates, exposición, backups, cifrado, gateway security.

---

## 15. CLI de Referencia (comandos top-level)

`agent`, `agents`, `approvals`, `attach`, `audit`, `backup`, `channels`, `config`, `configure`, `cron`, `devices`, `docs`, `doctor`, `gateway`, `health`, `hooks`, `infer/capability`, `logs`, `mcp`, `memory`, `message`, `models`, `node`, `nodes`, `onboard/setup`, `pairing/qr`, `plugins`, `proxy`, `sandbox`, `sessions`, `skills`, `status`, `tasks`, `transcripts`, `tui/chat`, `webhooks`, `worktrees` + `browser`, `exec` (vía tools).

---

## Tabla Resumen — Capacidades vs. Uso para Mr. Jair

| Capacidad | Qué hace | Ejemplo concreto |
|-----------|----------|------------------|
| **Gateway** | Orquesta todo | Ya corre en VPS; Control UI en :18789 |
| **Telegram** | Canal principal | Recibir tareas de `mision.md` y responder desde el móvil |
| **Cron** | Recordatorios exactos | Tarea `— 07:00` → `openclaw cron add --at ... --message ...` |
| **Heartbeat** | Checks periódicos | Revisar inbox/calendario cada 30m |
| **Tasks/TaskFlow** | Ledger + orquestación | Ghost Trader: backtest → reporte → alerta |
| **Memory + QMD** | Recuerdo entre sesiones | `qmd search "Meta Ads"` antes de grep |
| **Skills** | Workflows reusables | `gog` para Gmail/Calendar, `notion` para docs |
| **Plugins** | Extender sin forkar | Instalar `@openclaw/github` si necesita repos |
| **Browser** | Automatizar web con login | Scrapear dashboard de broker/Meta Ads |
| **Canvas/Nodes** | UI en móvil + comandos device | Dashboard visual en iOS |
| **Sub-agentes** | Paralelizar sin bloquear | 3 investigaciones concurrentes |
| **Media Gen** | Imagen/video/música/TTS | Creativos para ads, voz, análisis de screenshots |
| **Modelos** | 35+ providers + aliases | `/model dsv4` para barato, `spark` para reasoning |
| **Web Search** | 12+ motores | Research trading/noticias |
| **Seguridad** | Sandbox + approvals | `healthcheck` para auditar el VPS |

---

## Notas finales

- Esta nota se generó por exploración directa de `openclaw/docs`, `openclaw --help` (gateway/cron/skills/memory/browser/tasks), `skills list`, `package.json` y `~/.openclaw/openclaw.json` del host. No se inventaron capacidades.
- Para profundizar: `openclaw docs "query"` (docs vivas) o leer `docs/<area>/*.md` en `/root/.nvm/versions/node/v22.22.3/lib/node_modules/openclaw/docs`.
- Mantener actualizada: re-ejecutar esta investigación tras cada `openclaw update`.

*Generado automáticamente por sub-agente OpenClaw — 2026-09-07.*
