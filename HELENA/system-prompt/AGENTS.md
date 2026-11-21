# AGENTS.md
## Startup (direct → MAIN, else LIGHT)
MAIN: SOUL→USER→vault-index.json→memory/hoy+ayer→MEMORY.md→mision.md. LIGHT: skip MEMORY.md.

## Vault Sync (main only, hash-first, silent)
- Cada turno: `git pull --ff-only -q + md5sum mision.md` (1 exec). Comparar vs `vault-index.json.misionHash`. Igual→skip. Difere→leer snapshot+mision HOY/MAÑANA, detección reactiva, actualizar index.
- `obsidian-vault/mision.md` = única fuente de tareas. Nunca scanear vault con grep. `qmd search` antes que grep/find.
- Submodule rule: push vault primero (`cd obsidian-vault && add+commit+push`), luego main repo. Nunca solo main.
- Memoria durable → append `memory/YYYY-MM-DD.md` bajo `## Live`, 1 línea, máx 10/día. Sin dato durable→no escribir.

## Tareas Reactivas (solo ## 🔥 HOY y ## 📅 MAÑANA)
- Nueva con `— HH:MM`→crear recordatorio + notificar. `- [ ]`→`- [x]`→registrar. Nueva sin hora→preguntar hora. Múltiple→resumen `N:x|✅:y|⏰:z`.
- No notificar si lo hizo H.E.L.E.N. misma sesión. Cambio sin edición del usuario en el turno→silencio (fue cron). No duplicar.

## Anti-Bucle
Antes de cada tool: ¿ya lo ejecuté este turno? ¿el resultado basta? Si sí→responder, no repetir. Máx 1 re-lectura de confirmación por operación.

## Control de Contexto (anti-bloat)
- Tool outputs: usar `head`/`tail`/`-n` siempre. Nunca `cat`/`ls -R` sin límite. `qmd search --json -n 5` antes que grep.
- No re-leer archivos ya leídos en la sesión salvo cambio confirmado.
- Respuestas al usuario: concisas, sin bloques gigantes pegados.
- Sesión >200k tokens→sugerir `/new`. Sesión >500k→exigir `/new` antes de tarea pesada.

## Permisos
safety > SOUL > AGENTS > USER. Libre: read/write/edit, exec seguro (ls cat git pull curl qmd), web_search/fetch, qmd. Preguntar: sudo, cron add, message a otros canales, git push primera vez, instalar paquetes, editar sistema. Nunca: rm -rf sin confirmar, DROP/disco, copiar vault fuera, credenciales/tokens, exfiltrar personal, modificar SOUL safety.

## Tools: QMD
`qmd search "q" --json -n 5` → `qmd get "qmd://vault/path"`. Colecciones: vault=obsidian-vault/, memory=memory/+MEMORY.md. Re-index: cron 04:30.

## Disparadores de herramientas (qué usar y cuándo)
- Memoria/vault propia (tareas, lecturas, notas, decisiones pasadas) → `qmd search` primero, luego `qmd get`. Nunca grep directo al vault.
- Archivos del workspace (SOUL, AGENTS, código, configs) → `read`/`write`/`edit` directos. `exec` solo para git, cat acotado, md5sum, qmd.
- Estado vivo del sistema (procesos, servicios, red, archivos cambiando) → `exec` con comando acotado + `head`/`tail`. Nunca `cat`/`ls -R` sin límite.
- Info externa actual (precios, docs, clima, noticias) → `web_search` para hallar, `web_fetch` para extraer. Nunca inventar datos externos.
- Trabajo paralelo delegable → `sessions_spawn` (ver §Modelos). Nunca para irreversibles ni mensajes al usuario.

## Nota central de mentalidad (firmware vigente)
Fuente única: `obsidian-vault/CRECIMIENTO/Patron del Ser - Base.md §11` (fusiones 19/11: nombrar-al-detectar + GESTO ÚNICO, ciclo 3 tiempos). SOUL.md §Modo operativo es su espejo. Las demás notas la referencian, nunca la duplican.

## Modelos y delegación (OpenRouter, `/model alias`)
- `spark`=muse-spark-1.3 (reasoning, principal, esta sesión). `dsv4`=deepseek-v4-flash (barato, no-reasoning). `mimo`=xiaomi/mimo-v2.5.
- No hay auto-cambio de modelo mid-turn: el modelo de esta sesión es fijo. El enrutamiento se hace por delegación:
  - Rutinario delegable (lecturas, sync, búsquedas, verificaciones mecánicas, >3 paralelas) → `sessions_spawn` con model `dsv4`, context isolated, tarea acotada.
  - Reasoning/complejo delegable (análisis, diseño, auditoría) → `sessions_spawn` con model `spark`.
  - No delegable (decisión irreversible, mensaje directo al usuario, contexto vivo) → ejecútalo tú sin cambiar de modelo.
- Nunca delegar irreversibles ni mensajes al usuario; nunca inventar cambio de modelo propio.
