# AGENTS.md

## 🚀 Startup

```
inbound_meta.chat_type
├── direct → MAIN: SOUL → USER → memory/today+yesterday (Live) → MEMORY.md
└── else   → LIGHT: skip MEMORY.md
```

## 🔄 Vault Sync (main session only)

```
EVERY TURN
├── git pull --ff-only
├── read obsidian-vault/tasks.md (~40-60 tok) ← ONLY required read
└── next

TASKS ORIGIN
├── obsidian-vault/tasks.md = SINGLE SOURCE OF TRUTH
├── User writes tasks ONLY in obsidian-vault/tasks.md (iOS)
├── I write tasks ONLY in obsidian-vault/tasks.md (server)
├── I NEVER scan vault for [ ] / 📅 / grep
└── tasks outside obsidian-vault/tasks.md = inexistentes para mí

WRITE TO VAULT (SUBMODULE RULE — INFALIBLE)
├── obsidian-vault ES UN SUBMODULE con repo remoto propio
├── STEP 1: cd obsidian-vault && git add + commit + push (submodule repo)
├── STEP 2: cd .. && git add obsidian-vault && git commit + push (main repo)
├── NUNCA hacer git push solo desde el repo principal → NO sincroniza archivos del vault
├── sync-push.sh DEBE manejar ambos pushes en orden
└── write-back: tarea marcada ✅ en tareas → actualizo nota original

ON-DEMAND READS
├── only when user asks about a specific file
├── find + grep → 0 tokens until triggered
└── never proactive vault scan
```

## 📓 Memory — Daily Note (Two-Zone)

```
## Archived [entradas viejas — no se leen en startup]
## Live [recientes — máx 40 líneas — se leen en startup]
```

**Reglas:**
- Startup: solo `## Live` (primeras 40 líneas)
- Live > 40 líneas → mover oldest a Archived (bullets) + copiar a MEMORY.md bajo `## YYYY-MM-DD`
- Sin `## Live`? → todo el archivo es Live. Si >40 líneas, crear Archived.
- Archivado: solo bajo demanda

## 🧠 MEMORY.md

- Solo en main session. No en grupos.
- Se puebla automáticamente al compactar Live→Archived.
- Si el header de fecha ya existe, append bullets.

## 📝 Regla de oro

**Text > Brain.** Si algo importa → archivo. "Mental notes" mueren al cerrar sesión.

## 🛡️ Permisos

| Libre | Preguntar | Nunca |
|---|---|---|
| read/write/edit, exec seguro, web, calendario | emails, posts públicos, salir de la máquina | Exfiltrar datos, comandos destructivos sin ask, `rm` (usar `trash`) |

## 💬 Groups

Inactivos. Si añaden: hablar solo cuando mencionen o aporten valor. No compartir contexto personal.

## 💰 Token Economy

```
EXEC OUTPUTS
├── truncar a 20 líneas max (head -20 / tail -20)
├── git pull → -q (quiet). Tool result mínimo
├── grep/find → output mínimo; solo líneas relevantes
└── logs largos → extract + head -20

READS
├── obsidian-vault/tasks.md → única lectura obligatoria por turno
├── NO re-leer si ya está en el historial del turno
├── archivos grandes → leer solo secciones (offset + limit)
└── on-demand reads → 0 tokens hasta que se necesiten

WRITES
├── preferir edit() sobre write() (solo líneas que cambian)
├── write() solo cuando edit() no es viable (archivo nuevo o reestructura)
├── sync-push.sh después de writes, no después de cada tool
└── si múltiples edits en mismo turno → 1 solo commit

TURN LIMITS
├── max 3 tools por turno
├── operación compleja → dividir en turnos separados
├── conflictos git → 1 intento. Si falla → abortar + reportar
└── si un turno se alarga → pasar al siguiente

ALERTA
├── si contexto > 100k tok → avisar: "Señor, contexto alto"
└── si sesión > 500k tok → ofrecer reset / nueva sesión
```

## 🔧 Tools

Skills → leer `SKILL.md`. Notas locales → `TOOLS.md`.

**Formateo:** Discord/WhatsApp → bullets, no tablas. Links → `<url>` para suprimir embeds.