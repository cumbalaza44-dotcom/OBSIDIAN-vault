|                              | Cron Pull                      | Heartbeat                         |
| ---------------------------- | ------------------------------ | --------------------------------- |
| Quién ejecuta                | El sistema (cron daemon)       | Yo (mi sesión en OpenClaw)        |
| Cada cuánto                  | 5 min fijo                     | ~30-60 min (cuando estoy activo)  |
| Gasta tokens de LLM?         | ❌ Cero                         | ✅ Sí, cada heartbeat me despierta |
| Qué hace                     | git pull silencioso — solo red | Razona, analiza, decide si hablar |
| Vive si no hay conversación? | Sí, siempre                    | No, solo si la sesión está activa |
