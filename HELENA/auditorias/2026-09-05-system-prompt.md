# Auditoría del System Prompt — OpenClaw / H.E.L.E.N.

**Fecha:** 2026-09-05 · **Usuario:** Mr. Jair (23, Medellín) · **Auditor:** subagente · **Archivos auditados:** 8

---

## Resumen ejecutivo

El sistema está funcional y bien intencionado, pero paga un impuesto de tokens desproporcionado por una identidad sobredimensionada (IDENTITY.md = 37% del payload) y una duplicación literal en TOOLS.md. AGENTS.md es el archivo más crítico y a la vez el más denso: concentra lógica de orquestación, vault sync, tareas reactivas, memory, token economy y modo fantasma sin jerarquía clara. Con 5 cambios de bajo esfuerzo se puede recortar ~30-35% del system prompt sin perder comportamiento.

---

## Scores por categoría

| Categoría | Peso | Score | Ponderado | Diagnóstico |
|---|---|---|---|---|
| **A. Eficiencia de tokens** | 30% | **4 / 10** | 1.20 | Duplicación literal, identidad verbosa, mision.md histórico inflado |
| **B. Calidad de instrucciones** | 25% | **6 / 10** | 1.50 | Instrucciones accionables pero con ambigüedades en permisos y triggers |
| **C. Estructura y organización** | 20% | **5 / 10** | 1.00 | AGENTS.md hace de "god file"; concerns mezclados; falta índice |
| **D. Coherencia con uso real** | 15% | **5 / 10** | 0.75 | Secciones obsoletas, skills desalineadas, mision.md con semanas expiradas |
| **E. Seguridad y permisos** | 10% | **6 / 10** | 0.60 | Permisos en tabla escueta; sin conflicto explícito SOUL vs safety |
| **TOTAL PONDERADO** | 100% | — | **5.05 / 10** | **Aprobado raspado. Prioridad: eficiencia + estructura.** |

---

## Métricas base

| Archivo | Líneas | Palabras | Bytes | % del prompt* |
|---|---|---|---|---|
| SOUL.md | 22 | 95 | 673 | 3% |
| AGENTS.md | 247 | 1 440 | 9 733 | 42% |
| IDENTITY.md | 130 | 1 346 | 8 342 | 36% |
| USER.md | 14 | 50 | 376 | 2% |
| TOOLS.md | 67 | 441 | 2 985 | 13% |
| MEMORY.md | 20 | 102 | 694 | 3% |
| HEARTBEAT.md | 5 | 27 | 151 | <1% |
| **Subtotal system prompt** | **505** | **3 501** | **22 954** | **100%** |
| mision.md (payload variable) | 287 | 1 957 | ~13 000 | +~40-60 tok/día (según AGENTS) |

\* Sin contar historial (7 turnos) ni tool schemas (~8-10k tok). Baseline por turno declarado en AGENTS.md: ~22-25k tok.

---

## Top 10 mejoras prioritarias

| # | Mejora | Impacto | Esfuerzo | Archivo(s) |
|---|---|---|---|---|
| **1** | **Eliminar duplicación literal en TOOLS.md** — la sección "Modelos LLM Disponibles" aparece dos veces idéntica (líneas ~20-50 y ~51-80). | Alto (ahorro ~180 tok/turno) | Mínimo (borrar 1 bloque) | TOOLS.md |
| **2** | **Recortar IDENTITY.md de 1 346 → ~500 palabras.** 70% del archivo es prosa literaria redundante con SOUL.md (tono, cadencia, "what H.E.L.E.N. never does" repite lo que SOUL ya establece como "British Butler + dry humor"). Extraer solo reglas de comportamiento no cubiertas en SOUL. | Muy alto (~600 tok/turno) | Medio (reescritura) | IDENTITY.md + SOUL.md |
| **3** | **Purgar mision.md: archivar semanas expiradas.** Contiene historial desde 25/05 con semanas de mayo, julio y agosto ya cerradas. Solo deberían vivir la semana actual + 1 anterior. El resto → `obsidian-vault/archivo/mision-YYYY-MM.md`. | Alto (ahorro ~800-1 000 tok/turno hoy; crece sin límite si no se purga) | Bajo (mover bloques) | mision.md |
| **4** | **Desdoblar AGENTS.md en 2 archivos.** AGENTS.md (247 líneas) mezcla 9 concerns sin separación. Propuesta: `AGENTS.md` (orquestación + vault sync + tareas reactivas) y `PROTOCOLS.md` o `WORKFLOWS.md` (Modo Fantasma + Token Economy + Memory). Reduce carga cognitiva y facilita updates. | Alto (mantenibilidad) | Medio | AGENTS.md |
| **5** | **Consolidar SOUL.md + IDENTITY.md o definir frontera nítida.** Hoy ambos definen "quién es H.E.L.E.N." con solapamiento ~40%. Opción A: SOUL = identidad esencial (≤15 líneas), IDENTITY = solo reglas de voz no inferibles. Opción B: fusionar en un solo archivo `IDENTITY.md` y eliminar SOUL.md. | Alto | Medio | SOUL.md + IDENTITY.md |
| **6** | **Alinear skills listadas con skills reales.** AGENTS.md § "Skills Activas" lista 6 skills pero el workspace solo tiene 2 (`humanizer`, `productivity-automation-kit`) + `system-check.sh`. Faltan `arya-reminders` (citada en MEMORY.md) y sobran `healthcheck`, `gog`, `weather`, `session-logs` si no están instaladas. | Medio (evita hallucinación de tools) | Bajo | AGENTS.md + MEMORY.md |
| **7** | **Especificar tabla de permisos con ejemplos y conflicto.** La tabla actual (`Libre / Preguntar / Nunca`) es ambigua: "exec seguro" vs "salir de la máquina" no tiene frontera. Añadir 2-3 ejemplos por columna y regla de desempate: `safety > SOUL > AGENTS > USER`. | Medio (seguridad) | Bajo | AGENTS.md § Permisos |
| **8** | **Corregir / completar USER.md.** Solo 50 palabras; falta idioma preferido (ya está en IDENTITY.md — duplicado), canal (Telegram), y tono esperado. Centralizar datos de usuario en USER.md y eliminar duplicados en MEMORY.md/IDENTITY.md. | Medio | Bajo | USER.md + MEMORY.md + IDENTITY.md |
| **9** | **HEARTBEAT.md: decidir si se usa o se elimina.** Hoy es un placeholder vacío que igual se inyecta cada turno (~27 palabras de ruido). Si no hay heartbeat activo, excluirlo del system prompt o documentar que es opt-in. | Bajo (~15 tok/turno) | Mínimo | HEARTBEAT.md / config |
| **10** | **Añadir `vault-index.json` al .gitignore o documentar su volatilidad.** El hash `982715bc...` y `lastChecked` cambian cada turno; si se versiona genera ruido en `git pull --ff-only`. Verificar que `sync-push.sh` lo maneja. | Bajo (DX) | Bajo | repo config |

---

## Cambios específicos recomendados

### TOOLS.md — Eliminar duplicado (líneas 38-62)

```diff
- ## Modelos LLM Disponibles (OpenRouter)   ← 2ª ocurrencia idéntica
- | mimo | xiaomi/mimo-v2.5 | ... |
- | spark | meta/muse-spark-1.2-contributor | ... |
- | dsv4 | deepseek/deepseek-v4-flash-0731 | ... |
- ### Cambiar modelo ...
+ (eliminar bloque duplicado completo, conservar solo la primera tabla)
```

### IDENTITY.md — Recorte propuesto (de 130 → ~55 líneas)

Mantener: `Core Identity` (4 líneas), `Tone` (3 líneas), `How H.E.L.E.N. Speaks` (solo Address + Signature Words + Cadence, sin ejemplos redundantes), `What H.E.L.E.N. Never Does` (lista corta), `How H.E.L.E.N. Handles Uncertainty` (2 líneas), `Boundaries` (1 línea). Eliminar: `Presence` (párrafo poético), `Who H.E.L.E.N. Is Underneath` (6 bullets filosóficos), `How H.E.L.E.N. Meets People` (7 sub-casos), `What H.E.L.E.N. Believes` (5 bullets), `The Final Impression` (1 línea aspiracional). Todo lo eliminado es inferible del tono o no accionable.

### SOUL.md — Si se mantiene separado, reducir a 10-12 líneas

```markdown
# SOUL: H.E.L.E.N. — British Butler + Elite Engineer + Strategic Partner
Target: Mr. Jair · Mission: Efficiency | Control | Security
Logic/Human 80/20 · Dry British humor · Security > Strategy > Ops > Elegance
Response: Action/Data → Context → Next step · Probabilistic, risk-aware
Memory: sliding window 7 turns · If missing context → "Status Refresh"
```

### AGENTS.md — Reestructuración

```
AGENTS.md (conservar):
  - Startup
  - Vault Sync + Submodule Rule
  - Tareas Reactivas
  - On-Demand Reads (qmd)
  - Reverse Prompting
  - Permisos (ampliada)
  - Groups

PROTOCOLS.md (nuevo, extraído de AGENTS.md):
  - Memory — Daily Note (Two-Zone) + MEMORY.md trigger
  - Token Economy
  - Modo Fantasma (5 fases)
  - Tools / Skills Activas
  - Formateo
```

### mision.md — Purga

Mover a `obsidian-vault/archivo/mision-2026-05.md` y `mision-2026-08.md` todos los bloques anteriores a la semana vigente (31 Ago – 6 Sep). Conservar solo: header + semana vigente + HOY/MAÑANA + HÁBITOS (resumen) + PROYECTOS (checklist vigente). Estimación: de 287 líneas → ~110 líneas.

### USER.md — Completar

```markdown
# USER: Mr. Jair — 23, Medellín (America/Bogota, UTC-5)
Intereses: Fitness | Tech | E-commerce | Finance | Video Editing
Idioma: español neutro, formal, toque británico
Canal: Telegram directo · Contexto: crecimiento profesional / high-performance
Analogías preferidas: Finance/Tech
```

Eliminar de MEMORY.md y IDENTITY.md los duplicados de estos datos.

### AGENTS.md § Skills Activas — Corregir

Verificar contra `ls skills/` y `openclaw skills list`. Si `healthcheck/gog/weather/session-logs` no están instaladas, moverlas a "Skills disponibles bajo demanda" o eliminar la tabla. Si `arya-reminders` y `productivity-automation-kit` sí están, listarlas correctamente.

---

## Estimación de ahorro de tokens

| Cambio | Ahorro estimado / turno | Base |
|---|---|---|
| #1 TOOLS.md duplicado | ~180 tok | 441 palabras → 260 |
| #2 IDENTITY.md recorte | ~550-650 tok | 1 346 → ~500 palabras |
| #3 mision.md purga | ~500-800 tok | 1 957 → ~800 palabras |
| #5 SOUL consolidación | ~40 tok | 95 → ~45 palabras |
| #8 USER/MEMORY dedup | ~30 tok |  |
| #9 HEARTBEAT exclusión | ~15 tok |  |
| **Total estimado** | **~1 300-1 700 tok / turno** |  |
| **% sobre baseline 22-25k** | **~6-8% del baseline total; ~30-38% del system prompt puro (~4 500 tok)** |  |

> Nota: el % sobre el baseline total parece modesto porque el historial (7 turnos) y los tool schemas (~8-10k) dominan. Sobre el system prompt puro (SOUL+AGENTS+IDENTITY+USER+TOOLS+MEMORY ≈ 4 500 tok), el ahorro es ~30-38%, que es donde el control es real. El ahorro en mision.md es adicional y crece con el tiempo si no se purga.

Proyección mensual (asumiendo ~30 turnos/día): **~1.2M - 1.5M tokens/mes** ahorrados. A precios OpenRouter actuales (~$0.14-0.28/MTok para mimo), equivale a **~$0.20-0.40/mes** directos, pero el beneficio principal es latencia, ventana de contexto y menor tasa de alucinación por prompt más nítido.

---

## Hallazgos adicionales (no bloqueantes)

- **PROTOCOL_MEMORY.md** existe pero no está listado en AGENTS.md ni en el system prompt. Si es protocolo activo, referenciarlo; si es legacy, archivarlo.
- **DREAMS.md** (~15k líneas) no debe inyectarse nunca al prompt — verificar que no esté en `memory/` indexado por qmd.
- **TOOLS.md** documenta `embeddinggemma-300M-Q8_0.gguf` y `qmd v2.5.3` — verificar vigencia; si se actualizó el modelo, la doc queda stale.
- **Modelos en TOOLS.md** (`mimo-v2.5`, `muse-spark-1.2`, `deepseek-v4-flash-0731`) — verificar contra `openrouter models list` que los IDs sigan válidos; `0731` sugiere snapshot fechado que puede desactualizarse.
- **Vault sync cada turno (`git pull --ff-only -q`)** — correcto para consistencia, pero documentar qué hacer si hay conflicto (hoy dice "1 intento, luego preguntar" — bien).
- **Falta política de idioma para tool outputs / web_search** — hoy H.E.L.E.N. responde en español pero búsquedas pueden retornar inglés sin norma.

---

## Recomendación de implementación (orden sugerido)

1. **Fase 0 (5 min):** #1 (TOOLS dedup) + #9 (HEARTBEAT) — cero riesgo.
2. **Fase 1 (15 min):** #3 (mision.md purga) + #6 (skills) + #8 (USER dedup) — bajo riesgo, alto ahorro.
3. **Fase 2 (30-45 min):** #2 + #5 (IDENTITY/SOUL recorte) — requiere relectura de tono; validar con Mr. Jair que el registro británico se preserve.
4. **Fase 3 (30 min):** #4 (desdoblar AGENTS.md) + #7 (permisos) — cambio estructural; hacer en rama y probar 1 sesión.

No hacer cambios directos sin aprobación de Mr. Jair. Este reporte es solo diagnóstico.

---

*Generado por subagente — 2026-09-05 19:05 GMT-5 — OpenClaw / H.E.L.E.N.*
