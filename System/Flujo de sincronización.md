# Flujo de Sincronización — Obsidian Vault → OpenClaw

## 📡 Visión general

Pipeline automatizado de 0 costos en tokens. Conecta ediciones en iOS (Mr. Jair) con lecturas reactivas en OpenClaw (JARVIS), y viceversa.

```
┌──────────────┐     ┌────────────┐     ┌──────────────┐
│  Mr. Jair    │────→│  GitHub    │────→│  Servidor    │
│  (iOS)       │     │  Repo      │     │  (VPS)       │
└──────────────┘     └────────────┘     └──────┬───────┘
                                                │
                          ┌─────────────────────┘
                          ▼
              ┌──────────────────────────┐
              │  sync-pull.sh            │
              │  (cron cada 5 min)       │
              └──────────┬───────────────┘
                         │ ¿Cambios?
                         ▼
              ┌──────────────────────────┐
              │  sync-snapshot.sh        │
              │  → _VAULT-SNAPSHOT.md    │
              │       ├── 📁 Estructura  │
              │       ├── 🆕 Recientes   │
              │       ├── 📝 Tareas      │
              │       ├── 📋 Tareas hoy  │ ← Fecha actual
              │       └── 📄 Vacías      │
              │  → /tmp/obsidian-        │
              │    vault-flag            │
              └──────────┬───────────────┘
                         │ Señal reactiva
                         ▼
              ┌──────────────────────────┐
              │  JARVIS (OpenClaw)       │
              │  Lee snapshot en cada    │
              │  sesión — ya trae todo   │
              └──────────────────────────┘
```

## 🔄 Flujo completo

### 📥 Mr. Jair edita → JARVIS se entera

1. **Mr. Jair** edita/crea/checkea tareas en Obsidian (iOS)
   - Las tareas con `📅 YYYY-MM-DD` aparecen automáticamente en `Hoy.md` vía **Dataview + Tasks** nativos en Obsidian
   - Sin esperar al servidor — se renderiza al abrir la nota
2. Plugin **Obsidian Git** sincroniza a GitHub cada ~3 min
3. **sync-pull.sh** (cron del VPS cada 5 min) hace `git pull --ff-only`
4. Si hay cambios → ejecuta **sync-snapshot.sh**:
   - Genera `_VAULT-SNAPSHOT.md` (~30 líneas)
   - **Nuevo:** Incluye sección `📋 Tareas de hoy` con las tareas del día actual (date-filtered)
   - Escribe `/tmp/obsidian-vault-flag` (señal reactiva)
5. **JARVIS** en su próxima sesión detecta la flag, lee el snapshot y borra la flag
6. Costo: **0 tokens** en idle. Una lectura (~200 tokens) solo cuando hay cambios.

### 📤 JARVIS edita → Mr. Jair lo ve

1. **JARVIS** modifica archivos en `obsidian-vault/`
2. Al terminar, ejecuta **sync-push.sh**:
   - `git add -A` → `git commit` → `git push --force-with-lease`
3. También ejecuta **sync-snapshot.sh** para refresh inmediato del snapshot
   - El snapshot regenerado ya incluye las tareas del día actualizadas
4. **Mr. Jair** recibe los cambios vía plugin Obsidian Git en iOS
5. Costo: **0 tokens**. Sin esperar al cron.

### 🏠 Hoy.md — Nativo en Obsidian (sin servidor)

El archivo `Hoy.md` dejó de generarse desde el servidor. Ahora es una nota 100% nativa de Obsidian que usa **Dataview** y **Tasks** para renderizar las tareas del día automáticamente.

**Antes:**
```
iOS crea tarea → push GitHub → espera 5 min → sync-today.sh la escribe en Hoy.md → push devuelta a GitHub → iOS sincroniza
```

**Ahora:**
```
[Dentro de Obsidian iOS] Abres Hoy.md → Tasks query muestra tareas con 📅 hoy → instantáneo ✨
```

Esto fue posible gracias a que el snapshot del servidor (`_VAULT-SNAPSHOT.md`) ahora incluye su propia sección `📋 Tareas de hoy`, eliminando la dependencia del servidor para generar `Hoy.md`.

### 🚦 Señal reactiva (flag)

El archivo `/tmp/obsidian-vault-flag` contiene:
- `changed_at` — timestamp de detección
- `new_commits` — cantidad de commits nuevos
- `files_changed` — archivos modificados

Se borra automáticamente después de leerlo. Sin limpieza manual.

## 🧩 Scripts involucrados

| Script | Trigger | Función |
|--------|---------|---------|
| `sync-pull.sh` | Cron cada 5 min | Git pull + detección de cambios + snapshot |
| `sync-push.sh` | Manual (JARVIS) | Commit + push forzado de ediciones locales |
| `sync-snapshot.sh` | Pull (cambio) o Push | Genera `_VAULT-SNAPSHOT.md` con tareas del día |
| `check-flag.sh` | Startup de JARVIS | Detecta flag, inicia cadena de lectura |
| ~~`sync-today.sh`~~ | ~~Cron+Push~~ | ✅ **Eliminado** — reemplazado por Dataview + snapshot |

### sync-snapshot.sh — Ahora con tareas del día

Además de las secciones clásicas (estructura, archivos recientes, tareas pendientes globales), el snapshot escanea todas las notas buscando tareas con `📅 YYYY-MM-DD` igual a la fecha actual, separando pendientes `[ ]` de completadas `[x]`, y las incluye en una sección dedicada:

```markdown
## 📋 Tareas de hoy — 2026-05-12
**⏳ 1 pendientes | ✅ 0 completadas**

### ⏳ Pendientes
- [ ] 📅 2026-05-12 — Crear rutina de ejercicio  — *GYM.md*
```

Esto permite a JARVIS conocer las tareas del día en **una sola lectura del snapshot** (sin leer Hoy.md aparte).

## 📊 Costos

- **Idle:** 0 tokens — solo corre cron bash
- **Lectura en startup:** ~200 tokens (snapshot de ~30 líneas con tareas del día incluidas)
- **Escritura (JARVIS):** 0 tokens — solo git operations
- ~~**sync-today.sh:**~~ Eliminado — ahorra ejecución y push innecesarios

---

*Documentación del pipeline — Cero overhead, máximo control. Actualizado 2026-05-12.*
