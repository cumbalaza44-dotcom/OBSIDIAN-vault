# Guía: Cambio de Modelo en OpenClaw

## Fuente de verdad
`~/.openclaw/openclaw.json` → `agents.list[0].model.primary`

## Cambiar modelo
1. Editar `~/.openclaw/openclaw.json`
2. Cambiar el valor de `agents.list[0].model.primary`
3. Ejecutar: `openclaw gateway restart`
4. Verificar con: `session_status`

## Fallback
Si el primario falla, OpenClaw salta automáticamente al siguiente en `agents.list[0].model.fallbacks`.

## Notas
- El modelo activo se refleja automáticamente en el system prompt de cada sesión
- `AGENTS.md` no necesita mencionar el modelo — la fuente de verdad es `openclaw.json`
