# MEMORY.md

## 2026-05-07

- Revisión completa de AGENTS.md: 8 problemas detectados (Group Chats sobrerrepresentado, MEMORY.md vacío, vault pipeline sobre-documentado, falta jerarquía de prioridades, sin manejo de errores, sin conciencia de costos).
- Mr. Jair aportó 8 puntos de mejora quirúrgicos desde su perspectiva.
- **Mecanismo #1 implementado:** Detección de MAIN SESSION vía `inbound_meta.chat_type`. Única regla: `direct` = main session; else = ligero.
- **Mecanismo #2 implementado:** Sistema Two-Zone en daily notes (Live/Archived). Máx 40 líneas en Live. Compactación automática alimenta MEMORY.md.
- **Decisión estratégica:** MEMORY.md se puebla automáticamente al compactar Live → Archived. Sin contadores, sin heartbeats, sin revisión manual. La compactación es el trigger natural.