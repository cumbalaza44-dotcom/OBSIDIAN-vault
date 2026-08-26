# Sesión de Ajuste de Configuración — 24/08/2026

## 1. Diagnóstico del error de billing
- El error *"API provider returned a billing error"* se activaba cuando la API key de OpenRouter no tenía créditos o era inválida
- El sistema saltaba al fallback automáticamente
- Se resolvió con una key válida ($2.90 de crédito actual)

## 2. Limpieza de `AGENTS.md`
- Se eliminó la referencia a un modelo fantasma (`custom-api-deepseek-com/deepseek-v4-flash`)
- Se guardó la guía operativa en el vault: `obsidian-vault/Guía-Cambio-de-Modelo.md`
- `AGENTS.md` quedó limpio y sin menciones de modelos

## 3. Unificación de API keys
- Había 2 keys diferentes: una obsoleta en `gateway.systemd.env` y otra funcional en `models.json`
- Se reemplazó la obsoleta con la que funciona
- Resultado: una sola key activa

## 4. Limpieza de `models.json`
- Antes: **7 providers** (6 muertos + 1 activo)
- Ahora: **1 provider** (`openrouter-xiaomi`)
- Se eliminaron: `codex`, `custom-api-deepseek-com`, `custor-ai-deepseek`, `custom-openrouter-ai-deepseek`, `custom-openrouter-mimo`, `custom-openrouter-ai`

## 5. Optimización de `openclaw.json`
- `maxTokens`: 4,096 → **16,384** (capacidad real del modelo)
- `contextWindow`: 128,000 → **1,050,000**
- Costos reales del modelo (ya no en 0)

## 6. Cron jobs heredan el modelo
- Se eliminó el campo `"model"` hardcodeado de los 8 jobs activos
- Ahora heredan automáticamente de `openclaw.json`
- Cambio de modelo en un solo lugar → todos los jobs lo siguen

---

## Estado final

| Componente | Estado |
|------------|--------|
| API key | Una sola, funcionando |
| Provider | `openrouter-xiaomi` |
| Modelo | `xiaomi/mimo-v2.5` |
| Config optimizada | maxTokens 16K, contexto 1M |
| Cron jobs | Heredan modelo del agente |
| AGENTS.md | Limpio |
| Gateway | Corriendo |

---

## Nota técnica
- **Ficha del modelo MiMo v2.5:** Contexto 1,050,000 tokens, max completion 131,072 tokens, soporta reasoning, tools, structured outputs, image, audio, video
- **Costo real:** $0.14/M input, $0.28/M output (OpenRouter)
- **Cambio de modelo:** Editar `~/.openclaw/openclaw.json` → `agents.list[0].model.primary` → `openclaw gateway restart`
