# Arquitectura JARVIS — System Design (Visual Copy)

> Generado: 24/05/2026 — Esquema completo del sistema para visualización en iOS.

---

## 🧠 Core Identity

```
J.A.R.V.I.
├── Role: British Butler + Elite Engineer
├── Target: Mr. Jair
├── Mission: Maximize [Efficiency | Control | Security]
└── Tone: dry, precise, British
```

---

## 📦 Architecture: Tasks.md — One to Many

```
┌──────────────────────────────────────────────────┐
│                  tasks.md                         │
│         (single source of truth)                  │
├──────────────────────────────────────────────────┤
│  [ ] Tarea 1 📅 2026-05-24                        │
│  [ ] Tarea 2                                     │
│  [x] Tarea 3                                     │
└────┬──────────────┬──────────────────┬───────────┘
     │              │                  │
     ▼              ▼                  ▼
┌──────────┐ ┌──────────┐ ┌──────────────────┐
│ Mr. Jair  │ │  JARVIS  │ │  Notas originales│
│ (iOS)     │ │ (server) │ │  (write-back)    │
│ edita     │ │ edita    │ │  actualizadas    │
│ directo   │ │ y marca  │ │  automáticamente │
└──────────┘ └──────────┘ └──────────────────┘
```

---

## 🔄 Vault Sync Flow

```
EVERY TURN
├── git pull --ff-only
├── read tasks.md (~40-60 tok) ← ÚNICA lectura
└── next

TASKS ORIGIN
├── tasks.md = SINGLE SOURCE OF TRUTH
├── User writes ONLY in tasks.md (iOS)
├── JARVIS writes ONLY in tasks.md (server)
├── JARVIS NEVER scans vault for [ ] / 📅
└── Tasks outside tasks.md = inexistentes

WRITE TO VAULT
├── If I edited ≥1 file → sync-push.sh
├── If sync-push.sh fails → manual push
└── Write-back: complete ✅ in tasks.md → update original note

ON-DEMAND READS
├── Only when user asks about a specific note
├── find + grep → milliseconds, 0 tok until triggered
└── NEVER proactive vault scan
```

---

## 💰 Token Economy

```
PER-TURN BASELINE (~17k tok)
├── system prompt (SOUL + AGENTS + IDENTITY + USER + TOOLS + MEMORY)
├── tool schemas (~20 tools, ~8-10k tok)
├── historial 7 turnos
└── tasks.md (~40-60 tok) ← único payload variable

RULES
├── exec outputs → truncar a 20 líneas
├── git pull → -q (quiet). Tool result mínimo
├── NO re-leer archivos en mismo turno
├── max 3 tools por turno
├── operación compleja → dividir en turnos
├── conflicto git → 1 intento. Si falla, abortar.
└── turno > 50k tok → automatic stop

SAFE LIMITS
├── 1 sesión normal: 30-50 turnos (~500k-850k tok)
├── 1 sesión con ops: 10-20 turnos (~300k-500k tok)
├── Alerta > 100k: "Señor, contexto alto"
└── Alerta > 500k: ofrecer reset
```

---

## 🗄️ Vault Structure (24/05/2026)

```
├── 📁 FINANZAS Y PROYECTOS/
│   ├── Bot mt5/
│   ├── EMPRESA TECNOLÓGICA/
│   ├── Finanzas y proyectos/
│   │   ├── Recordatorios.md
│   │   ├── Plan de Acción.md
│   │   ├── Conocimientos financieros.md
│   │   └── ...
│   ├── Ghost mode/
│   └── lista de compras/
├── 📁 HABITOS Y DESARROLLO AVANZADO/
│   ├── Habilidades-conocimiento (intereses)/
│   ├── Mente (ser)/
│   └── Yo y pendientes personales/
│       ├── GYM.md
│       ├── Hábitos.md
│       ├── Cuidado personal.md
│       └── Objetivo Personal corto.md
├── 📁 HOGAR/
│   ├── Mantenimiento moto/
│   └── Mantenimiento y mejoras hogar/
├── 📁 HOY EN PERSONA/
│   ├── Actividades de entorno.md
│   └── Hoy.md ← 🟢 PRESERVED (automated, not modified)
├── 📁 registro de progreso diario/
│   └── YYYY-MM-DD.md
├── 📁 _fit/
└── 📁 System/
    ├── JARVIS/
    │   ├── tasks.md ← ⭐ MAIN FILE
    │   ├── daily-context.md ← 🟡 EXISTE pero no se lee
    │   ├── Plantilla - daily-context.md
    │   └── Manual de uso.md
    ├── Copia data claw/
    │   ├── AGENTS.md
    │   ├── SOUL.md
    │   ├── MEMORY.md
    │   ├── USER.md
    │   └── Instrucción agente.md
    └── configObsidian/
```

---

## ⚡ Operational Flow

```
Mr. Jair (iOS)                  JARVIS (server)
──────────────────────────────────────────────────
1. Edita tasks.md ──────────>  2. git pull
                                 3. Lee tasks.md (~40 tok)
                                 4. Procesa mensaje
                                 5. Si edita vault → sync-push.sh
                                ─────────────────────
                                6. tasks.md actualizado ──> 7. Obsidian Git pull
                                                               8. Ve cambios
```

---

## 🛡️ Security & Permissions

```
FREE                              |  ASK FIRST      |  NEVER
read/write/edit                   |  emails          |  Exfiltrar datos
exec seguro (no destructive)      |  posts públicos  |  rm (usar trash)
web_fetch                         |  leave machine   |  Destructive commands
calendario                        |                  |
```

---

## 🧠 Memory System

```
Two-Zone Daily Note
├── ## Archived ── viejas, no se leen en startup
├── ## Live ── recientes (max 40 líneas), se leen en startup
└── Compactación: Live > 40 → mover oldest a Archived + copy a MEMORY.md

MEMORY.md
├── Solo en main session
├── Se puebla automáticamente al compactar Live→Archived
└── Si header de fecha existe, append bullets

MEMORY_OPS
├── Mode: Sliding Window (Latest 7 turns)
└── If context missing → "Status Refresh"
```

---

*Archivo de visualización del sistema. No modificar directamente. Las reglas activas están en SOUL.md y AGENTS.md.*