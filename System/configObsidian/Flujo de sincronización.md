# Flujo de Sincronización — Obsidian Vault ↔ H.E.L.E.N. (v3)

> **Modelo: Reactivo por turno + tasks.md como fuente única + QMD para búsqueda.**

## 📡 Visión general

Pipeline reactivo. H.E.L.E.N. sincroniza en cada turno directo. No hay cron ni heartbeat — la detección de cambios ocurre al leer tasks.md.

```
┌──────────────────┐
│  Mr. Jair (iOS)  │
└───────┬──────────┘
        │
        ├── 1. Edita tasks.md o cualquier nota
        │    (Obsidian en iOS)
        │
        ├── 2. Obsidian Git → push a GitHub (~3 min)
        │
        ▼
  ┌───────────┐     ┌──────────────────────────────┐
  │  GitHub   │────→│  H.E.L.E.N. recibe mensaje   │
  └───────────┘     └──────────┬───────────────────┘
                               │
                    ┌──────────────────────┴──┐
                    │ git pull --ff-only      │
                    │ read vault-index.json   │
                    │ read tasks.md           │
                    │ calcular hash           │
                    │ ¿cambió? → detectar     │
                    └──────────┬──────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ▼                     ▼
             ┌──────────┐      ┌──────────────────┐
             │ No → sin │      │ Sí → comparar    │
             │ acción   │      │ snapshot previo  │
             └──────────┘      └──────────────────┘
                                      │
                             ┌────────┴────────┐
                             │ Tarea nueva ⏰  │→ crear recordatorio
                             │ Tarea nueva sin │→ reverse prompting
                             │ Tarea ✅        │→ registrar progreso
                             │ Prioridad ↑     │→ reordenar MIT
                             └─────────────────┘
```

## 🔄 Flujo completo

### 📥 Mr. Jair edita → H.E.L.E.N. lo detecta

1. **Mr. Jair** edita `tasks.md` en Obsidian iOS
2. Plugin **Obsidian Git** sincroniza a GitHub (~3 min)
3. **H.E.L.E.N.** recibe un mensaje → automáticamente:
   - `git pull --ff-only` (~0.5s)
   - Lee `vault-index.json` (hash + snapshot anterior)
   - Lee `obsidian-vault/tasks.md` (~40-60 tokens)
   - Calcula hash de tasks.md (`md5sum`)
   - Si el hash cambió → detecta qué cambió y actúa
4. **No se lee `daily-context.md`** — reemplazado por lectura directa de tasks.md + QMD
5. **No se lee `Hoy.md`** — contiene Dataview no legible en texto plano
6. Costo en idle: **0**. Costo por interacción: **~100 tokens**.

### 📤 H.E.L.E.N. edita → Mr. Jair lo ve

1. **H.E.L.E.N.** modifica `tasks.md` u otros archivos en `obsidian-vault/`
2. Al terminar, ejecuta **sync-push.sh**:
   - `cd obsidian-vault && git add + commit + push` (submodule)
   - `cd .. && git add obsidian-vault && git commit + push` (main repo)
3. **Mr. Jair** recibe los cambios vía plugin Obsidian Git en iOS
4. Costo: **0 tokens**.

## 🗂️ Archivos clave

### `tasks.md` — La única fuente de verdad para tareas

Archivo central. Todo lo que está aquí existe; lo que no está aquí, no existe para H.E.L.E.N.
- Se lee **cada turno** (~40-60 tokens)
- Se compara contra `vault-index.json` para detectar cambios

### `vault-index.json` — Snapshot para detección de cambios

```json
{
  "tasksHash": "md5sum de tasks.md",
  "lastChecked": "timestamp",
  "tasksSnapshot": ["lista de tareas del HOY"]
}
```

### `System/JARVIS/daily-context.md` — Obsoleto

Ya no se usa. Reemplazado por lectura directa de tasks.md + búsqueda QMD.

## 🔍 QMD — Motor de búsqueda del vault

Indexa todo el vault para búsqueda semántica rápida:
- `qmd search "consulta" --json -n 5` — búsqueda por keywords
- `qmd get "qmd://vault/ruta"` — leer documento completo
- Dos colecciones: `vault` (notas) y `memory` (memoria a largo plazo)

## 🧩 Scripts involucrados (servidor)

| Script | Trigger | Función |
|--------|---------|---------|
| `sync-push.sh` | H.E.L.E.N. al editar | Commit + push del submodule + repo principal |
| `skills/arya-reminders/create-reminder.sh` | Tarea nueva con hora | Crear recordatorio vía cron |

## 🧩 Archivos de identidad

| Archivo | Propósito |
|---------|-----------|
| `SOUL.md` | Identidad, principios, tono |
| `IDENTITY.md` | Personalidad detallada de H.E.L.E.N. |
| `USER.md` | Perfil de Mr. Jair (preferencias, datos) |
| `AGENTS.md` | Reglas operativas, startup, vault sync, token economy |
| `TOOLS.md` | Configuración de herramientas locales (QMD, etc.) |
| `MEMORY.md` | Memoria a largo plazo (curada desde daily notes) |

## 📊 Costos actualizados

| Concepto | Costo |
|----------|-------|
| Idle | **0 tokens + 0 procesos** |
| Startup / turno | ~100 tok (tasks.md + vault-index.json) |
| Búsqueda QMD | ~50 tok por consulta (vs 500+ con grep/read) |
| Escritura | 0 tokens |
| Latencia iOS→H.E.L.E.N. | ~3 min (push GitHub) + tu próximo mensaje |

## 📖 Uso diario

```
1. Editas tasks.md en iOS (agregas, marcas, priorizas)
2. Obsidian Git sincroniza solo (~3 min)
3. Me escribes algo → detecto cambios automáticamente
4. Si agregaste tarea con hora → creo recordatorio al instante
5. Si marcaste ✅ → registro en progreso diario
6. Si es ambigua → reverse prompting para detalles
```

---

*Documentación del pipeline v3 — tasks.md + vault-index + QMD. Actualizado 2026-06-09.*
