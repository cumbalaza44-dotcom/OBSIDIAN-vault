---
created: 2026-05-13
type: template-script
purpose: Generate System/JARVIS/daily-context.md
---
Onfra estructura iluminación y alimentación 

Orden de estandar
Documentación de profesor

Martes jueves





75 orbs  50 listas 

- [x] 100 cajas ✅ 2026-05-13
100 parrilas
- [x] 100 sueches 


- [ ] Charla de sentimiento con Jarvis📅 2026-05-17 

| Dimensi贸n              | Hermes Agent                                                                                                                                       | OpenClaw                                                                                      |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Naturaleza             | Agente autónomo con aprendizaje continuo                                                                                                           | Gateway multi-canal para conectar chats con agentes AI                                        |
| Stack                  | Python (uv, Nous Research)                                                                                                                         | Node.js                                                                                       |
| Ciclo de aprendizaje   | ✅ Loop cerrado — crea skills desde la experiencia, se automajora, persiste conocimiento, modela al usuario (Honcho)                                | ❌ No tiene — es un enrutador de enrutamiento, sin aprendizaje autónomo                        |
| Skills                 | Autocreación autónoma tras t                                                                                                                       | Skills estáticas (SKILL.md), cargadas por el usuario                                          |
| Memoria                | FTS5 + LLM cross-session, nudges periódicos, modelado dialéctico                                                                                   | MEMORY.md + archivos markdown, ventana deslizante, formato fijo                               |
| Aspecto                | OpenClaw                                                                                                                                           | Hermes Agent                                                                                  |
| System prompt          | ~9,600 tok promedio. Incluye: tool schemas (~8,000), skills list, workspace files (AGENTS.md, SOUL.md, TOOLS.md, etc.), runtime metadata, timezone | ~1,300 tok fijos de memoria (MEMORY.md + USER.md) + SOUL.md. Tool schemas se cargan on-demand |
| Memoria fija           | MEMORY.md se inyecta en startup, memory/*.md on-demand vía tool de búsqueda                                                                        | MEMORY.md (~800 tok) + USER.md (~500 tok) = ~1,300 tok fijos por sesión                       |
| Workspace files        | Se inyectan literalmente al sistema — AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, HEARTBEAT.md, BOOTSTRAP.md.                              |                                                                                               |
| Aspecto                | OpenClaw                                                                                                                                           | Hermes Agent                                                                                  |
| System prompt          | ~9,600 tok promedio. Incluye: tool schemas (~8,000), skills list, workspace files (AGENTS.md, SOUL.md, TOOLS.md, etc.), runtime metadata, timezone | ~1,300 tok fijos de memoria (MEMORY.md + USER.md) + SOUL.md. Tool schemas se cargan on-demand |
| Memoria fija           | MEMORY.md se inyecta en startup, memory/*.md on-demand vía tool de búsqueda                                                                        | MEMORY.md (~800 tok) + USER.md (~500 tok) = ~1,300 tok fijos por sesión                       |
| Workspace files        | Se inyectan literalmente al sistema — AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, HEARTBEAT.md, BOOTSTRAP.md.                              |                                                                                               |
| Componente             | OpenClaw                                                                                                                                           | Hermes Agent                                                                                  |
| System prompt          | ~10,000–15,000 tok (tool schemas pesan)                                                                                                            | ~3,000 tok (memoria compacta + SOUL)                                                          |
| Historial conversación | Se acumula hasta compaction                                                                                                                        | Se acumula hasta /reset (sin compaction automático)                                           |
| Overhead fijo          | Alto — herramientas, skills, workspace files se inyectan siempre                                                                                   | Bajo — solo memoria comprimida + SOUL.md                                                      |
| Tokens por compaction  |                                                                                                                                                    |                                                                                               |
