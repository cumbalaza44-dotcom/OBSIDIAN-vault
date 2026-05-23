# Flujo de Sincronización — Obsidian Vault ↔ OpenClaw (v2)

> **Modelo: Bajo Demanda — Sin cron. Sin heartbeat. Sin snapshot.**

## 📡 Visión general

Pipeline 100% reactivo a la conversación. JARVIS sincroniza el vault automáticamente al inicio de cada sesión directa. No hay procesos en segundo plano, no hay archivos intermedios, no hay flags.

```
┌──────────────────┐
│  Mr. Jair (iOS)  │
└───────┬──────────┘
        │
        ├── 1. Edita tareas en cualquier nota
        │    (con 📅 YYYY-MM-DD)
        │
        ├── 2. Ejecuta plantilla Templater
        │    → genera System/JARVIS/daily-context.md
        │    → markdown 100% plano (tareas + estructura)
        │
        ├── 3. Obsidian Git → push a GitHub (~3 min)
        │
        ▼
  ┌───────────┐     ┌──────────────────────────────┐
  │  GitHub   │────→│  JARVIS inicia sesión directa │
  └───────────┘     └──────────┬───────────────────┘
                               │
                    ┌──────────────────────┴──┐
                    │ git pull --ff-only      │
                    │ (sin dry-run, directo) │
                    └──────────┬──────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  ¿Hubo cambios?      │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             ┌──────────┐      ┌──────────────────┐
             │ No → leer│      │ Sí → ya están   │
             │ daily-   │      │ descargados y   │
             │ context  │      │ mergeados       │
             └──────────┘      └──────────────────┘
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌──────────────────────┐
                    │  JARVIS tiene        │
                    │  contexto completo   │
                    │  del vault           │
                    └──────────────────────┘
```

## 🔄 Flujo completo

### 📥 Mr. Jair edita → JARVIS se entera

1. **Mr. Jair** edita/crea/checkea tareas en Obsidian (iOS)
   - Usa `📅 YYYY-MM-DD` para fechar tareas (Tasks + Dataview lo reconocen)
   - `Hoy.md` se renderiza automáticamente en iOS para visualización
2. **Mr. Jair ejecuta la plantilla Templater** (`Cmd+P` → Templater: Insert Template)
   - Escanea todo el vault
   - Extrae tareas del día, estructura de carpetas, archivos recientes
   - Escribe `System/JARVIS/daily-context.md` en **markdown 100% plano**
3. Plugin **Obsidian Git** sincroniza a GitHub (~3 min)
4. **JARVIS** inicia una sesión directa → automáticamente:
   - `git pull --ff-only` (~0.5s, directo, sin lógica condicional)
   - Lee `System/JARVIS/daily-context.md` (~50-200 tokens)
5. **No se lee Hoy.md** — contiene código Dataview no legible en texto plano
6. **Cada turno:** `git pull --ff-only` antes de procesar cualquier mensaje
7. Costo en idle: **0**. Costo por interacción: **~150 tokens**.

### 📤 JARVIS edita → Mr. Jair lo ve

1. **JARVIS** modifica archivos en `obsidian-vault/`
2. Al terminar, ejecuta **sync-push.sh**:
   - `git add -A` → `git commit` → `git push --force-with-lease`
3. **Mr. Jair** recibe los cambios vía plugin Obsidian Git en iOS
4. Costo: **0 tokens**.

## 📁 Archivos clave

### `System/JARVIS/daily-context.md` — El archivo que lee JARVIS

Generado por Templater desde iOS. Contiene:

```markdown
# 📋 Contexto Diario — 13/05/2026

> 📊 33 notas — 12 carpetas — 2 pendientes hoy

## 🏋️ Tareas de hoy
### ⏳ Pendientes
- [ ] Crear rutina de ejercicio — *GYM.md*

## 📁 Estructura del vault
├── 📄 Hoy.md
├── 📁 FINANZAS/
│   └── Bot MT5.md
...

## 🆕 Modificados recientemente
- GYM.md — *2026-05-13*
```

### `System/JARVIS/Plantilla - daily-context.md` — El generador

Script Templater que escanea el vault y escribe `daily-context.md`.
**Debe ejecutarse manualmente** (o vía atajo de teclado) después de editar tareas.

### `Hoy.md` — Solo para visualización en iOS

Usa Dataview + Tasks queries. **No es legible en texto plano**, por eso JARVIS no lo lee.

## 🧩 Scripts involucrados (servidor)

| Script | Trigger | Función |
|--------|---------|---------|
| `sync-push.sh` | Manual (JARVIS al editar) | Commit + push forzado de ediciones locales |

## 🧩 Plantillas involucradas (iOS)

| Plantilla | Trigger | Función |
|-----------|---------|---------|
| `System/JARVIS/Plantilla - daily-context.md` | Manual (Templater) | Genera daily-context.md con tareas, estructura, recientes |

**Eliminados (v1 → v2 → v2.1):**

| ~~Script/Archivo~~ | ~~Razón~~ |
|-------------------|-----------|
| ~~sync-pull.sh~~ | Reemplazado por `git pull --ff-only` en startup y cada turno |
| ~~sync-snapshot.sh~~ | Reemplazado por `daily-context.md` generado en iOS |
| ~~sync-today.sh~~ | Reemplazado por Templater + `daily-context.md` |
| ~~check-flag.sh~~ | Eliminado |
| ~~_VAULT-SNAPSHOT.md~~ | Eliminado |
| ~~/tmp/obsidian-vault-flag~~ | Eliminado |
| ~~Cron cada 5 min~~ | Eliminado |
| ~~Lectura de Hoy.md~~ | Reemplazado por `daily-context.md` (texto plano legible) |

## 📊 Costos

| Concepto | Costo |
|----------|-------|
| Idle | **0 tokens + 0 procesos** |
| Startup (cambios) | ~150 tok (daily-context.md) |
| Startup (sin cambios) | ~150 tok (daily-context.md, mismo contexto) |
| Escritura | 0 tokens |
| Latencia iOS→JARVIS | ~3 min (push GitHub) + tu próximo mensaje |

## 📖 Uso diario

```
1. Editas tareas en iOS (con 📅 fecha)
2. Cmd+P → Templater: Insert Template → "Plantilla - daily-context"
3. [Opcional: atajo Cmd+Shift+D]
4. Obsidian Git sincroniza solo
5. Hablas con JARVIS → ya tiene el contexto
```

---

*Documentación del pipeline v2.2 — Pull directo cada turno, sin dry-run ni condicionales. Actualizado 2026-05-16.*
