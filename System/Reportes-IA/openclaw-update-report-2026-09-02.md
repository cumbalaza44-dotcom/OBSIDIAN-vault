# Reporte de Actualización OpenClaw
**Fecha:** 2026-09-02  
**Analista:** H.E.L.E.N. (subagent)

---

## 📊 Estado Actual

| Campo | Valor |
|-------|-------|
| Versión instalada | `2026.7.1-2` (0790d9f) |
| Última disponible (npm) | `2026.8.2` |
| Gateway | ✅ Activo (PID 3247383, puerto 18789) |
| Bind | Loopback (127.0.0.1) |
| Modelo activo | `openrouter/xiaomi/mimo-v2.5` (mimo) |
| Otros modelos | spark (Muse Spark), dsv4 (DeepSeek V4 Flash) |

---

## 🆕 Novedades en 2026.8.2

### Highlights principales

1. **Home Panel (Cmd/Ctrl+Shift+H)** — Abrir tu agente Home en un dock lateral/derecho sin cambiar de página. Permite previsualizar el contexto de trabajo adjunto o adjuntar texto seleccionado al mensaje.

2. **Desktop Companion para Linux** — Instalable vía `.deb` o AppImage en x86-64. Quick Chat desde system tray o atajo de teclado X11. AppImage con actualizaciones verificadas por firma.

3. **Background Sessions mejoradas** — Crear y ejecutar sesiones en segundo plano desde "New Session" sin salir de la página. Seleccionar ubicación (local, cloud, paired-device). Abrir desde aviso de completado.

4. **Upgrades más seguros** — Preserva configuración más nueva, detiene migraciones incompletas de sesión, y recupera Gateway detenido tras actualización fallida si el paquete es seguro.

5. **Replies que terminan el trabajo** — Retorna respuesta final después de tool work asentado, y superficia fallos después de un turno aceptado. Corrige conversaciones que se deten en output de tool.

6. **Voz más confiable** — Mantiene razonamiento interno fuera del audio, preserva audio generado por tools, y mantiene turnos de Browser Talk funcionales después de setup de llamada.

7. **Browser control sin Gateway corriendo** — Extensiones Chrome en macOS/Linux pueden despertar el relay local pareado para clientes CDP autenticados.

8. **4 nuevos temas UI** — CRT, Manuscript, Rosé, Miami. Persisten offline y se aplican sin flash durante recarga.

### Cambios técnicos

- **Visibilidad de sesiones por defecto** — Sesiones unsandboxed ahora trabajan con otras sesiones del mismo agente por defecto. Para acceso más restrictivo, configurar `tools.sessions.visibility` a `tree` o `self`.
- **Conversaciones cross-session** — Mensajes reenviados se renderizan como bubbles distintos con links de sesión y identidad del agente remitente.
- **Organización de sesiones** — Menús más claros, copiar transcripts como Markdown, abrir en tabs/ventanas/splits, editar iconos y colores, ocultar grupos vacíos.
- **Beam links legibles** — URLs `/beam/` con nombres legibles basados en la sesión.
- **Plugin SDK types** — `botToken` de Telegram tipado como `SecretInput (string | SecretRef)`.
- **iOS composer** — Controles inline de modelo, thinking, permisos, adjuntos y contexto más cercanos a web.

### Fixes relevantes

- **Sharp actualizado a 0.35.4** con libheif 1.23.2 — corrige vulnerabilidades de decodificación de imágenes.
- **Permisos de workspace** — Cambios de permisos se aplican a runs activos.
- **Diagnósticos privados** — Valores marcados como privados se redactan en logs de macOS.
- **Límites de MCP** — Rechaza respuestas HTTP y eventos SSE oversized antes de parsear.
- **Fidelidad de source files** — Preserva UTF-8 BOMs, line endings, contexto fuzzy-match y estado end-of-file.
- **Seguridad de migración** — Coordinación de mantenimiento agent-database, verificación de readiness.
- **Configuración más nueva preservada** — Migración lee configuración activa antes de intentar recuperación last-known-good.

---

## ⚠️ Problemas Detectados en el Sistema Actual

### 1. Catalog Schema Error (doctor)
```
model catalog load issue: Invalid models.json schema:
providers.openrouter.models.1.input.2/3: must be equal to constant / must match a schema in anyOf
```
**Archivo:** `/root/.openclaw/agents/main/agent/plugins/openrouter/catalog.json`  
**Impacto:** Puede causar que ciertos modelos no se carguen correctamente en el catálogo. No bloquea el funcionamiento actual pero genera warnings.

### 2. Agent "main" sin tool "message" (doctor warning)
```
Agent "main" is routed from channel "telegram", but the message tool 
is unavailable for that agent; explicit channel actions such as 
sendAttachment, upload-file, thread-reply, or reply can fail.
```
**Impacto:** Las acciones de mensajería explícitas (enviar archivos, respuestas en threads) pueden fallar. Se recomienda agregar `"message"` al allowlist del agente o usar un profile con herramientas de mensajería.

### 3. Gateway Service PATH (gateway status)
```
Service config issue: Gateway service PATH includes version managers; 
recommend a minimal PATH.
Service config issue: Gateway service uses Node from a version manager; 
it can break after upgrades.
```
**Impacto:** El servicio usa Node desde nvm (`~/.nvm/versions/node/v22.22.3/bin/node`). Si se actualiza Node o nvm, el Gateway puede dejar de funcionar. Se recomienda un path mínimo para el servicio.

### 4. Startup optimization (doctor)
- `NODE_COMPILE_CACHE` no configurado — CLI runs más lentos en hosts pequeños.
- `OPENCLAW_NO_RESPAWN` no establecido — restarts rutinarios se dan al supervisor en vez de manejarse in-process.

---

## 🔍 Impacto en la Configuración Actual

| Aspecto | Estado | Impacto |
|---------|--------|---------|
| Modelos (mimo, spark, dsv4) | ✅ Funcional | Ninguno deprecated en 2026.8.2 |
| Gateway loopback | ✅ Funcional | Sin cambios relevantes |
| Telegram channel | ⚠️ Parcial | Falta tool "message" en allowlist — afecta sendAttachment/reply |
| OpenRouter plugin | ⚠️ Warning | Catalog schema issue — revisar catalog.json |
| Skills (humanizer, gog, weather, etc.) | ✅ Funcional | Sin breaking changes reportados |
| Obsidian vault submodule | ✅ Funcional | Sin cambios en manejo de submodules |
| Cron jobs | ✅ Funcional | Sin cambios en sistema de cron |
| Session visibility | ⚠️ Cambio default | Nuevo default: unsandboxed sessions comparten visibility. Configurar `tools.sessions.visibility: "tree"` si se necesita aislamiento |

---

## 🎯 Recomendación

### **Actualizar: SÍ, pero con precaución**

**Razones a favor:**
1. Salto de **2 versiones** (7.1 → 8.2) — corrige vulnerabilidades de imágenes (Sharp/libheif) y múltiples bugs de migración.
2. Mejoras significativas en **voice, browser control, y sessions** que impactan positivamente el uso diario.
3. **Upgrades más seguros** — el propio update proceso es más robusto en 8.2, así que el camino de actualización es más confiable.

**Precauciones antes de actualizar:**
1. **Resolver el warning de "message" tool** — agregar `"message"` al allowlist del agente `main` para Telegram antes de actualizar.
2. **Revisar `catalog.json`** — el schema error de OpenRouter puede causar problemas con modelos; verificar después de la actualización.
3. **Backup de configuración** — `cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-20260902`.
4. **El servicio usa nvm** — considerar migrar a un path estático del binario de Node para mayor estabilidad.

**Proceso de actualización:**
```bash
# 1. Backup
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-20260902

# 2. Actualizar
npm update -g openclaw

# 3. Verificar
openclaw --version
openclaw doctor
openclaw gateway status

# 4. Si hay problemas
openclaw doctor --repair
```

**¿Esperar?** No es urgente (no hay CVEs críticos reportados), pero el salto acumulado justifica la actualización. Los fixes de seguridad de Sharp y la robustez del proceso de upgrade hacen que valga la pena.

---

*Reporte generado automáticamente por H.E.L.E.N. — 2026-09-02 18:34 COT*
