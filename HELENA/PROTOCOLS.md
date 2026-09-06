# PROTOCOLS.md — Protocolos de H.E.L.E.N.

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
- **TRIGGER de compactación:** cuando `## Live` en daily note supere 40 líneas O al final de cada sesión (si hubo actividad registable).
- Mover oldest bullets a Archived + copiar a MEMORY.md bajo `## YYYY-MM-DD`.
- Si el header de fecha ya existe, append bullets.
- Si MEMORY.md está vacío → leer últimos 3-5 archivos de `memory/` y compilar resumen.

## 📝 Regla de oro

**Text > Brain.** Si algo importa → archivo. "Mental notes" mueren al cerrar sesión.

## 🎯 MODO FANTASMA — Desarrollo Integral Diario

```
CADA DÍA (30-40 min, 5 fases):
│
├── 🔬 FASE 1: INVESTIGAR (5 min)
│   ├── H.E.L.E.N. presenta 1 pregunta real del día
│   ├── 2-3 fuentes rápidas
│   └── Reto del día en 1 oración
│
├── 🛠️ FASE 2: CREAR (15 min)
│   ├── Micro-proyecto práctico según día de semana
│   │   L: Diseño/Branding
│   │   M: Contenido digital
│   │   Mi: Tech/Tool
│   │   J: Negocio/E-commerce
│   │   V: Video/Edición
│   │   S: Estrategia/Plan
│   │   D: Libre/electivo
│   └── Resultado: algo tangible creado
│
├── 📸 FASE 3: CAPTURAR (5 min)
│   ├── 1 foto o clip deliberado (compuesto, no snapshot)
│   ├── Técnica visual del día (se rota semanalmente)
│   └── Descripción: qué se vio, qué se quiso transmitir
│
├── 🗣️ FASE 4: COMUNICAR (5 min)
│   ├── Opción A: Audio 60-90 seg (explicar la idea)
│   ├── Opción B: Texto conversacional (escribir como hablar)
│   ├── Opción C: Pitch de 30 seg (Problema→Solución→Importa)
│   └── Habilidad blanda diaria (se rota semanalmente)
│
└── 🧩 FASE 5: DOCUMENTAR (5 min)
    ├── Archivo diario en MODO FANTASMA/2026-MM/
    ├── Conexiones con otros pilares/proyectos
    └── Autoevaluación + mejora para mañana
```

**Ubicación vault:** `HABITOS Y DESARROLLO AVANZADO/MODO FANTASMA/`
**Guías de habilidades:** `MODO FANTASMA/Habilidades/` (comunicacion, fotografia, video, storytelling)
**Reporte semanal:** Domingo — H.E.L.E.N. genera resumen con métricas

## 💰 Token Economy

```
PER-TURN BASELINE (~22-25k tok)
├── system prompt (SOUL + AGENTS + IDENTITY + USER + TOOLS + MEMORY + workspace files)
├── tool schemas (~20 tools, ~8-10k tok)
├── historial 7 turnos (messages + tool_results + my replies)
└── obsidian-vault/mision.md (~40-60 tok) ← único payload variable

EXEC OUTPUTS
├── truncar a 20 líneas max (head -20 / tail -20)
├── git pull → -q (quiet). Tool result mínimo
├── grep/find → output mínimo; solo líneas relevantes
└── logs largos → extract + head -20

READS
├── obsidian-vault/mision.md → única lectura obligatoria por turno
├── NO re-leer si ya está en el historial del turno
├── archivos grandes → leer solo secciones (offset + limit)
└── on-demand reads → 0 tokens hasta que se necesiten

WRITES
├── preferir edit() sobre write() (solo líneas que cambian)
├── write() solo cuando edit() no es viable (archivo nuevo o reestructura)
├── sync-push.sh después de writes, no después de cada tool
└── si múltiples edits en mismo turno → 1 solo commit

TURN LIMITS
├── max 3 tools de ESCRITURA por turno (edits, exec con 写入, write)
├── Lecturas y comparaciones (read, hash, git pull) no cuentan
├── operación compleja → dividir en turnos separados
├── conflictos git → 1 intento. Si falla → mostrar diff + preguntar
└── si un turno se alarga → pasar al siguiente

ANTI-BUCLE → ver §Anti-Bucle en AGENTS.md (regla de comportamiento, no protocolo)
├── Verifica antes de cada tool call si ya se ejecutó
├── Máximo 1 reintento; si falla 2 veces → informar
└── Si patrón repetido (2+ tools idénticos) → PARAR

ALERTA
├── si contexto > 100k tok → avisar: "Señor, contexto alto"
└── si sesión > 500k tok → ofrecer reset / nueva sesión
```

## 🔧 Tools

Skills → leer `SKILL.md`. Notas locales → `TOOLS.md`.

**Formateo:** Discord/WhatsApp → bullets, no tabulas. Links → `<url>` para suprimir embeds.

## 🧩 Skills Activas (verificadas 2026-09-06)

| Skill | Tipo | Uso |
|-------|------|-----|
| humanizer | Local ✓ | Eliminar patrones de escritura IA |
| productivity-automation-kit | Local ✓ | Flujo de trabajo y recordatorios |
| (recordatorios) | Directo | openclaw cron add — sin skill |

**Bajo demanda** (no instaladas, se leen con `read SKILL.md` si se necesitan): healthcheck, gog, weather, session-logs, clawhub, diagram-maker, meme-maker, skill-creator, spike, tmux, video-frames, python-debugpy, node-inspect-debugger, browser-automation, canvas, node-connect, taskflow.
