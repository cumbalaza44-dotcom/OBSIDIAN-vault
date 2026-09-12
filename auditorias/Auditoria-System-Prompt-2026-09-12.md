# Auditoría System Prompt — OpenClaw / H.E.L.E.N.

**Fecha:** 2026-09-12 18:53 GMT-5 · **Auditor:** subagente · **Alcance:** solo lectura, sin modificar configs ni crons
**Auditoría previa:** `workspace/auditoria-system-prompt.md` (2026-09-05, score 5.05/10, 10 hallazgos)

---

## (a) Estado actual

### Archivos del system prompt (medido hoy)

| Archivo | Líneas | Palabras | Estado vs 05/09 |
|---|---|---|---|
| SOUL.md | 30 | 152 | estable (95→152w, crece leve) |
| IDENTITY.md | 50 | 296 | ✅ recortado (1346→296w) |
| USER.md | 27 | 120 | ✅ completado (50→120w) |
| AGENTS.md | 147 | 856 | ✅ desdoblado (247→147l, PROTOCOLS.md extraído) |
| PROTOCOLS.md | 86 | 571 | ✅ nuevo (memory two-zone + token economy + skills) |
| TOOLS.md | 55 | 329 | ✅ deduplicado (bloque LLM duplicado eliminado) |
| MEMORY.md | 14 | 76 | ⚠️ delgado, nota Gym pendiente desde hace semanas |
| HEARTBEAT.md | 3 | 26 | ❌ sigue placeholder inactivo |
| **Total prompt** | **412** | **~2400** | ✅ −30% aprox. vs 05/09 (~3500w) |
| mision.md | 195 | 1137 | ✅ purgado (287→195l, 1957→1137w) |

### Config (`/root/.openclaw/openclaw.json`, 600 perms)

- Modelo principal: `spark` (muse-spark-1.3) + fallbacks `openrouter/free`. Aliases mimo/spark/dsv4 coherentes con TOOLS.md.
- Gateway local + loopback, controlUi `allowInsecureAuth:true` (aceptable en local), Tailscale off.
- `denyCommands`: cámara, SMS, calendar/reminders/contacts add — bien.
- Plugins: google, memory-core (dreaming off), openrouter, telegram. Skills mayormente deshabilitadas; solo `humanizer` + `productivity-automation-kit` locales — coherente con PROTOCOLS.md.
- ⚠️ Secretos en plaintext (bot token Telegram + API key OpenRouter). Permisos 600 mitigan; sin backup automático verificado de este archivo (`backup-openclaw.sh` es de abril).

### Cron jobs (6 total, todos `ok` + `delivered`)

| Job | Schedule (Bogotá) | Estado |
|---|---|---|
| Mañana | 5:00 diario | ok |
| Mediodía | 12:30 L-V | ok |
| Tarde (checkpoint + gastos) | 18:00 L-V | ok |
| Cierre nocturno | 21:00 diario | ok |
| Weekly Planning | Dom 20:00 | ok (última corrida 100s, ok) |
| One-shot: Organizar habitación | Dom 13, 06:00 COT | programado, correcto (11:00Z = 06:00 COT) |

### Vault sync

- `md5sum mision.md` = `55ee0785…` == `vault-index.json.misionHash` ✅ **en sync**.
- Estructura HOY (Sáb 12, 2 tareas) / MAÑANA (Dom 13, 7 tareas con horas) / SEMANA 07–13 tabla completa / HÁBITOS / PROYECTOS / HOGAR / HABILIDADES — bien formada.
- Último commit vault `8e74869` (12/09 18:47), push dual funcionando.

### Progreso desde auditoría 05/09 (7 de 10 aplicados)

Aplicados: #1 TOOLS dedup, #2 IDENTITY recorte, #3 mision purga, #4 desdoble AGENTS→PROTOCOLS, #5 frontera SOUL/IDENTITY (nota "no duplicar"), #6 skills alineadas, #7 regla desempate `safety > SOUL > AGENTS > USER`, #8 USER completado.
Pendientes: #9 HEARTBEAT (sigue placeholder), #10 vault-index gitignore/volatilidad (sigue versionado, ver nuevo hallazgo H1).

**Score estimado hoy: ~7.0/10** (era 5.05). Sube por eficiencia y estructura; pierde puntos por los hallazgos nuevos abajo.

---

## (b) Incoherencias / fricciones detectadas

### 🔴 Críticos

**H1. `vault-sync.sh` (raíz) destruye el schema de `vault-index.json` si alguien lo ejecuta.**
El script regenera `vault-index.json` como `{updated, totalNotes, notes[]}`, pero el archivo real usa `{misionHash, misionSnapshot, lastChecked}` (sistema reactivo de AGENTS.md). Ejecutarlo borraría el tracking de tareas. Está obsoleto y es peligroso. No se tocó (solo auditoría).

**H2. Triple especificación de tono contradictoria.**
- SOUL.md: "español neutro, preciso, sin adjetivos redundantes".
- IDENTITY.md: "español neutro, colombiano cuando aporta cercanía".
- USER.md: "español neutro, formal, toque británico".
"Tocar británico" vs "colombiano cercano" vs "sin adjetivos" no son el mismo registro. Hoy depende del archivo que pese más en el turno.

**H3. Snapshot de `vault-index.json` incluye TODAS las secciones, AGENTS.md dice "solo HOY".**
El snapshot actual mezcla HOY + MAÑANA + HÁBITOS + PROYECTOS. Cualquier edición en PROYECTOS dispara "TASKS CHANGED" y el diff por línea puede confundir arrastres con tareas nuevas. Además el separador `|` es frágil si una tarea contiene `|`.

### 🟡 Medios

**H4. Carrera de escritura cron→main sin marcador de origen.**
Weekly Planning (y cualquier cron futuro con permiso de escritura) edita `mision.md` desde sesión aislada. El siguiente turno main ve hash distinto y lo atribuye al usuario ("Señor, detecté que agregó…"). No hay marcador de origen de escritura ni refresh de snapshot post-cron.

**H5. Cierre nocturno se contradice a sí mismo.**
Su payload ordena "Marcar tareas pendientes que se carry-forward a mañana" y en la misma instrucción "No crear archivos, solo enviar mensaje". No puede hacer carry-forward sin editar `mision.md`.

**H6. Índice qmd obsoleto (95 días).**
`qmd status`: 119 archivos indexados, actualizado hace 95 días. AGENTS.md obliga `qmd search` antes que grep, pero el índice no ve nada creado desde ~junio. Búsquedas con misses silenciosos.

**H7. Pipeline de memoria diaria inactivo.**
`memory/` no tiene daily notes de septiembre (último: 2026-08-23). "registro de progreso diario" del vault solo llega a mayo. El sistema two-zone de PROTOCOLS.md existe en papel pero no corre; la continuidad entre sesiones recae solo en MEMORY.md (76 palabras) + mision.md.

**H8. Hábito de lectura diaria muerto pero vivo en el prompt.**
`LECTURAS-DIARIAS/` último archivo 2026-08-12 (un mes). Tabla HÁBITOS: "Lectura diaria | Último registro Sáb 8/08" (5 semanas). Gym: "❌ semana 24-28 Ago" (3 semanas). mision.md sigue listando "📚 Lectura" cada día y MAÑANA trae "Revisar y ajustar cron lecturas diarias" — el cron de lecturas no existe en `cron list`. Decisión pendiente: restaurar o retirar.

### 🟢 Menores

**H9.** HEARTBEAT.md placeholder se inyecta cada turno (~26 palabras de ruido). Excluirlo o eliminarlo.
**H10.** `sync-push.sh` aún dice "JARVIS" (nombre legacy), usa `--force-with-lease` y loguea a `/var/log` (puede fallar por permisos). Funciona, pero deuda nominal.
**H11.** Weekly Planning referencia `TASKS.MD` (nombre legacy; el archivo es `mision.md`). Los crons aislados sin historial pueden confundirse.
**H12.** Job Tarde usa `channel: "telegram:7310779816" + accountId`, los demás `channel: "telegram" + to`. Deriva de schema; funciona, normalizar cuando se toque.
**H13.** TOOLS.md dice mimo = "Default", pero el default real es spark. Una línea stale.
**H14.** Repo raíz sucio: `skills/arya-reminders/*` eliminados sin commitear, `media/inbound/openclaw-staged-*` y `reports/*` sin trackear. Higiene de commits pendiente (no bloquea el vault).
**H15.** Job Mañana asume "Fitness: rutina del día (5:30-8:00)" también fines de semana; HOY Sáb 12 no trae gym y MEMORY.md dice que la rutina Gym está "a redefinir". Riesgo de alucinación fitness en check-ins de fin de semana.

---

## (c) Mejoras propuestas (priorizadas por impacto)

| # | Mejora | Impacto | Esfuerzo | Origen |
|---|---|---|---|---|
| **P0** | **Retirar o corregir `vault-sync.sh`**: o se elimina (el sync real lo hace el agente + `sync-push.sh`), o se reescribe para preservar `{misionHash, misionSnapshot, lastChecked}`. Hoy es una trampa de pérdida de datos. | Evita destrucción del tracking reactivo | Bajo (borrar o 20 líneas) | H1 |
| **P1** | **`qmd update && qmd embed` + cron mensual de reindexado.** Sin índice vigente, la regla "qmd antes que grep" es teatro. | Restaura la búsqueda del vault | Bajo (un comando + 1 cron) | H6 |
| **P2** | **Tono single-source: USER.md manda.** Fijar `USER.md = registro británico formal` como única fuente de tono usuario; SOUL conserva "preciso, sin adjetivos" como estilo de razonamiento interno; IDENTITY elimina su línea de idioma o la deja como "cercanía solo si el usuario la pide". | Elimina registro inconsistente | Bajo (3 ediciones) | H2 |
| **P3** | **Scopar snapshot a HOY (+ MAÑANA) y cambiar separador a `\n` o JSON array.** Cumple lo que AGENTS.md ya promete y elimina falsos positivos de PROYECTOS. | Menos notificaciones fantasma | Medio (ajustar detección + 1 migración de formato) | H3 |
| **P4** | **Marcador de origen de escritura + refresh post-cron.** Ej.: línea `<!-- updated-by: weekly-planning 2026-09-13 -->` o que los crons con escritura refresquen `misionHash/snapshot` al terminar. | Cierra la carrera cron→main | Medio | H4 |
| **P5** | **Decidir lectura diaria: restaurar cron o retirar hábito.** Si se restaura, recrear cron diario; si no, quitar "📚 Lectura" de la tabla SEMANA y archivar `LECTURAS-DIARIAS/`. Lo mismo para Gym: actualizar tabla o pausar hábito hasta redefinir rutina. | Coherencia mision ↔ crons ↔ hábitos | Bajo (decisión de Mr. Jair + edición) | H8, H15 |
| **P6** | **Resolver contradicción del Cierre:** o se le permite editar `mision.md` (carry-forward real), o se cambia la instrucción a "proponer carry-forward en el mensaje". | Cierre funcional | Mínimo (1 línea del payload) | H5 |
| **P7** | **Reactivar daily notes o declararlas obsoletas.** Si two-zone sigue vigente, crear la nota de hoy y el hábito de compactación; si no, mover la sección de PROTOCOLS.md a "legacy". | Continuidad entre sesiones | Medio (hábito operativo) | H7 |
| **P8** | **Excluir HEARTBEAT.md del prompt** hasta que exista un heartbeat real. | −26 tok/turno de ruido | Mínimo | H9 |
| **P9** | **Higiene raíz:** commitear deletions `arya-reminders`, ignorar `media/inbound/openclaw-staged-*`, decidir destino de `reports/*.md`. Renombrar JARVIS→H.E.L.E.N. en `sync-push.sh`, quitar `--force-with-lease`, log local. | Repos limpios, menos confusión | Bajo | H10, H14 |
| **P10** | **Micro-correcciones:** `TASKS.MD`→`mision.md` en Weekly Planning, normalizar delivery del job Tarde, "Default" mimo→spark en TOOLS.md, acotar fitness de fin de semana en job Mañana. | Pulido | Mínimo | H11–H13, H15 |

### Orden de ejecución sugerido

1. **Hoy (15 min, cero riesgo):** P0 (retirar `vault-sync.sh` del camino) + P1 (reindexar qmd) + P8 (excluir heartbeat).
2. **Con Mr. Jair (decisiones):** P2 (tono), P5 (lectura/gym), P7 (daily notes sí/no).
3. **Siguiente ventana (30-45 min):** P3 + P4 (snapshot + origen de escritura) + P6 (cierre) en una sola pasada, probar un turno.
4. **Fondo:** P9 + P10 cuando se toquen esos archivos por otro motivo.

---

## Verificación de sync

- Hash `mision.md` (`55ee0785…`) == `vault-index.json.misionHash` al cierre de esta auditoría ✅
- Este reporte vive en `obsidian-vault/auditorias/Auditoria-System-Prompt-2026-09-12.md`, pusheado dual (submódulo + raíz).
- No se modificó ningún config, prompt ni cron. Solo lectura + este reporte.

*Subagente — 2026-09-12 18:53 GMT-5 — OpenClaw / H.E.L.E.N. 🦾*
