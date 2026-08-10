# Modelos con Cache Funcional en OpenRouter — Reporte

**Fecha:** 2026-08-09
**Fuente principal:** Catálogo OpenRouter (`https://openrouter.ai/api/v1/models`) consultado en vivo + detalles por endpoint (`/api/v1/models/{modelo}/endpoints`).
**Precios:** por millón de tokens, tomados del catálogo en vivo (no estimados).

---

## Resumen ejecutivo

Sí existen modelos con **cache funcional real** (cache-read barato y aplicado automáticamente) a precios **iguales o menores** que DeepSeek V4 Flash. Los mejores candidatos para OpenClaw son:

1. **Qwen3.7 Flash** (`qwen/qwen3.7-flash`) — el ganador claro: cache automático confirmado (`implicit=true`), cache-read $0.006/M, input $0.03/M, output $0.13/M. Todo más barato que DeepSeek V4 Flash.
2. **DeepSeek V4 Flash 0731** (`deepseek/deepseek-v4-flash-0731`) — misma familia que ya usas, pero más barato y con cache automático en el proveedor oficial.
3. **GPT-5 Nano** (`openai/gpt-5-nano`) — cache automático en proveedor OpenAI, cache-read $0.005/M, pero output más caro ($0.40/M).
4. **MiMo V2.5** (`xiaomi/mimo-v2.5`) — misma calidad/precio que DeepSeek V4 Flash pero **cache NO automático** (confirmado: todos los endpoints `implicit=false`). No recomendado si el cache es el factor dominante.

**Hallazgo clave:** MiMo vía OpenRouter expone precio de `input_cache_read` ($0.0028/M) pero **ningún endpoint tiene `supports_implicit_caching: true`**, lo que confirma que NO aplica cache automáticamente. DeepSeek V4 Flash, en cambio, **sí** tiene el proveedor oficial con `implicit=true` y cache-read de $0.0028/M.

---

## Tabla de candidatos principales

| Modelo | ID OpenRouter | Input/M | Output/M | Cache-read/M | Cache automático | Contexto | Nota |
|---|---|---|---|---|---|---|---|
| **Qwen3.7 Flash** | `qwen/qwen3.7-flash` | $0.03 | $0.13 | **$0.006** | ✅ Sí (Alibaba) | 1M | Mejor relación calidad-precio-cache |
| **DeepSeek V4 Flash 0731** | `deepseek/deepseek-v4-flash-0731` | $0.09 | $0.18 | $0.018 (oficial $0.0028) | ✅ Sí (proveedor DeepSeek) | 1M | Misma familia, más barato |
| **DeepSeek V4 Flash** (actual) | `deepseek/deepseek-v4-flash` | $0.14 | $0.28 | $0.028 (oficial $0.0028) | ✅ Sí (proveedor DeepSeek) | 1M | El que ya usas |
| **GPT-5 Nano** | `openai/gpt-5-nano` | $0.05 | $0.40 | $0.005 | ✅ Sí (OpenAI) | 400K | Cache muy barato, output caro |
| **MiMo V2.5** (Xiaomi) | `xiaomi/mimo-v2.5` | $0.14 | $0.28 | $0.0028 | ❌ NO (ningún endpoint) | 1M | Cache-read barato pero NO automático |
| **GLM 5.2** (Z.ai) | `z-ai/glm-5.2` | $0.07 | $0.22 | $0.013 | ⚠️ Solo con `cache_control` | 1M | Barato pero requiere marcadores explícitos |
| **Ling 3.0 Flash** | `inclusionai/ling-3.0-flash` | $0.021 | $0.063 | $0.0042 | ⚠️ No automático | 262K | Muy barato, calidad baja |
| **Nex-N2-Mini** | `nex-agi/nex-n2-mini` | $0.025 | $0.10 | $0.0025 | ⚠️ No automático | 262K | Cache-read ultra barato, calidad baja |

---

## Análisis detallado de los mejores candidatos

### 1. Qwen3.7 Flash (`qwen/qwen3.7-flash`) — RECOMENDADO
- **Precios:** input $0.03/M | output $0.13/M | cache-read $0.006/M | cache-write $0.038/M
- **Cache automático:** ✅ `supports_implicit_caching: true` en el proveedor Alibaba.
- **Contexto:** 1M tokens.
- **Por qué:** Es el único candidato con cache automático confirmado **y** precios inferiores a DeepSeek V4 Flash en las tres métricas (input, output y cache-read). El cache-read de $0.006/M es 4.6× más barato que el cache-read nominal de DeepSeek V4 Flash ($0.028/M) y 2× más barato que el del proveedor oficial ($0.0028/M vs... ojo, $0.006 > $0.0028, así que en cache-read estricto DeepSeek oficial gana; pero Qwen gana en input y output). Para cargas muy pesadas de cache-read repetido, DeepSeek oficial sigue siendo imbatible en cache-read ($0.0028/M).
- **Nota sobre OpenClaw:** Qwen usa slug `qwen/*`, que **NO** está en la lista de prefijos de cache-ttl de OpenClaw (`anthropic`, `deepseek`, `moonshot`, `moonshotai`, `zai`). Sin embargo, como el cache es **automático** en el proveedor (no requiere `cache_control` que OpenClaw inyecte), funciona igual. El único matiz es que `contextPruning.mode: "cache-ttl"` no aplica a este prefijo.
- **Fuente:** `https://openrouter.ai/api/v1/models/qwen/qwen3.7-flash/endpoints` (Alibaba, implicit=true, cR $0.006/M).

### 2. DeepSeek V4 Flash 0731 (`deepseek/deepseek-v4-flash-0731`) — RECOMENDADO
- **Precios:** input $0.09/M | output $0.18/M | cache-read $0.018/M (promedio) | **$0.0028/M en el proveedor oficial DeepSeek**
- **Cache automático:** ✅ `supports_implicit_caching: true` SOLO en el proveedor `DeepSeek` (los ~24 terceros hosts tienen `implicit=false` pero igual cachean).
- **Contexto:** 1M tokens.
- **Por qué:** Es la misma arquitectura que ya usas (DeepSeek V4 Flash) pero la revisión 0731 es **más barata** en input ($0.09 vs $0.14) y output ($0.18 vs $0.28). El cache-read en el proveedor oficial es idéntico ($0.0028/M). Está en el prefijo `deepseek/*` que OpenClaw reconoce para cache-ttl.
- **Fuente:** `https://openrouter.ai/api/v1/models/deepseek/deepseek-v4-flash-0731/endpoints` (proveedor DeepSeek, implicit=true, cR $0.0028/M).

### 3. GPT-5 Nano (`openai/gpt-5-nano`) — OPCIONAL
- **Precios:** input $0.05/M | output $0.40/M | cache-read $0.005/M (OpenAI) / $0.0025/M (otro endpoint OpenAI)
- **Cache automático:** ✅ `supports_implicit_caching: true` en los endpoints de OpenAI (Azure tiene `implicit=false`).
- **Contexto:** 400K tokens.
- **Por qué:** Cache-read muy barato ($0.005/M) y input barato ($0.05/M), pero **output caro** ($0.40/M, 43% más que DeepSeek). Si tu uso genera bastante output (razonamiento/agentic), esto encarece. Cache automático real confirmado.
- **Fuente:** `https://openrouter.ai/api/v1/models/openai/gpt-5-nano/endpoints` (OpenAI, implicit=true, cR $0.005/M).

### 4. MiMo V2.5 (`xiaomi/mimo-v2.5`) — NO RECOMENDADO para cache
- **Precios:** input $0.14/M | output $0.28/M | cache-read $0.0028/M
- **Cache automático:** ❌ `supports_implicit_caching: false` en TODOS los endpoints.
- **Contexto:** 1M tokens.
- **Por qué NO:** Confirma tu observación. Aunque el catálogo muestra `input_cache_read: $0.0028/M`, **ningún proveedor lo aplica automáticamente**. OpenClaw no puede activar el cache sin marcadores `cache_control`, y MiMo vía OpenRouter no los soporta de forma implícita. El precio "cache-read" es teórico/disponible solo si hubiera forma de marcarlo, que no la hay en este caso.
- **Fuente:** `https://openrouter.ai/api/v1/models/xiaomi/mimo-v2.5/endpoints` (todos los endpoints implicit=false).

### 5. GLM 5.2 (`z-ai/glm-5.2`) — OPCIONAL
- **Precios:** input $0.07/M | output $0.22/M | cache-read $0.013/M
- **Cache automático:** ⚠️ `implicit=false` en todos los endpoints (requiere `cache_control` explícito).
- **Contexto:** 1M tokens.
- **Por qué:** Precios competitivos y buena calidad (AA: intel 52.6, coding 68.8, agentic 45.7), pero el cache NO es automático. **Importante:** el slug de OpenRouter es `z-ai/glm-5.2` (con guion), mientras que OpenClaw reconoce el prefijo `zai/*` (sin guion). Esto significa que el prefijo `zai/*` de OpenClaw **no coincide** con el slug real `z-ai/*` de OpenRouter. Verificar si OpenClaw normaliza `z-ai` → `zai`.
- **Fuente:** `https://openrouter.ai/api/v1/models/z-ai/glm-5.2/endpoints`.

---

## Ranking de recomendación para uso tipo OpenClaw

Considerando: cache-read barato + input/output competitivo + cache automático + calidad agentic/código.

| # | Modelo | Veredicto | Razón |
|---|---|---|---|
| 1 | **Qwen3.7 Flash** | ⭐ Mejor opción | Cache automático + precios inferiores en todo + 1M contexto. Único con cache automático confirmado y más barato que DeepSeek. |
| 2 | **DeepSeek V4 Flash 0731** | ⭐ Mejor "drop-in" | Misma familia que ya usas, más barato, cache automático en proveedor oficial, prefijo `deepseek/*` reconocido por OpenClaw. |
| 3 | **GPT-5 Nano** | 👍 Bueno si el output no domina | Cache-read ultra barato, pero output $0.40/M lo encarece en cargas agentic. |
| 4 | **GLM 5.2** | 👍 Bueno si aceptas cache explícito | Barato y capaz, pero requiere `cache_control` y el prefijo `zai/*` no coincide con el slug `z-ai/*`. |
| 5 | **MiMo V2.5** | ❌ Evitar para cache | Cache-read barato pero NO automático — el problema que ya tienes. |

---

## Notas importantes / Honestidad sobre limitaciones

1. **`supports_implicit_caching` no está en el endpoint principal** (`/api/v1/models`). Hay que consultar `/api/v1/models/{modelo}/endpoints` por modelo. Lo hice para los candidatos clave.
2. **El cache-read "de catálogo" no garantiza cache automático.** MiMo es el caso: muestra `input_cache_read` pero ningún endpoint lo aplica solo. La señal real de cache automático es `supports_implicit_caching: true` a nivel endpoint.
3. **DeepSeek tiene cache automático solo en el proveedor oficial** (`DeepSeek`). Los ~24 terceros hosts (Together, Fireworks, CoreWeave, etc.) tienen `implicit=false`. OpenRouter usa **sticky routing** para mantener el cache caliente en el proveedor que lo sirvió, así que si OpenClaw aterriza en el proveedor DeepSeek, el cache automático funciona.
4. **Prefijos de OpenClaw vs slugs reales de OpenRouter:**
   - OpenClaw reconoce: `anthropic/*`, `deepseek/*`, `moonshot/*`, `moonshotai/*`, `zai/*` (fuente: docs OpenClaw, `extensions/openrouter/index.ts`).
   - Los slugs reales de Z.ai en OpenRouter usan `z-ai/*` (con guion). El prefijo `zai/*` de OpenClaw **no coincide** con `z-ai/*`. Esto merece verificación antes de depender de GLM para cache-ttl.
   - Qwen usa `qwen/*`, que no está en la lista de prefijos, pero su cache es automático (no necesita los marcadores de OpenClaw).
5. **Cache-read nominal vs real:** El catálogo muestra el cache-read del modelo agregado (promedio). El cache-read real depende del proveedor que sirva la request. Para DeepSeek V4 Flash, el agregado es $0.028/M pero el proveedor oficial cobra $0.0028/M.
6. **Calidad (Artificial Analysis):** DeepSeek V4 Flash 0731 (intel 51.8, coding 69.1, agentic 48.4) y GLM 5.2 (intel 52.6, coding 68.8, agentic 45.7) son los más capaces de los candidatos baratos. Qwen3.7 Flash y GPT-5 Nano no tienen métricas AA publicadas en el catálogo. Ling/Nex-N2 tienen calidad baja (agentic <30).

---

## Fuentes

- Catálogo de modelos OpenRouter (en vivo): `https://openrouter.ai/api/v1/models`
- Detalles por endpoint: `https://openrouter.ai/api/v1/models/{modelo}/endpoints`
- Docs OpenRouter — Prompt Caching (multiplicadores de cache: DeepSeek 0.1, Alibaba 0.1, Anthropic 0.1; sticky routing): `https://openrouter.ai/docs/guides/best-practices/prompt-caching.md`
- Docs OpenClaw — Prompt Caching (prefijos `anthropic/deepseek/moonshot/moonshotai/zai` para cache-ttl; DeepSeek cache best-effort): `https://docs.openclaw.ai/reference/prompt-caching.md`
