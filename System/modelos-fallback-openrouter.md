# Modelos Fallback OpenRouter

Evaluación 2026-11-22 (ampliada con capacidades reales). Principal: `spark` (muse-spark-1.3, reasoning).

## Tabla comparativa

| Modelo | ID OpenRouter | Input / 1M | Output / 1M | Contexto | Capacidades |
|---|---|---|---|---|---|
| Tencent Hy4 Flash | `tencent/hy4-flash` | $0.035 | $0.1405 | 1M (1,048,576), salida hasta 64k | MoE 224B total (12B activos/token), texto+imagen in, reasoning nativo (Deep Reasoning), function calling, structured output. Open-weight. Sin EU routing. |
| InclusionAI Ling 3.2 Flash | `inclusionai/ling-3.2-flash:free` | $0 (free) | $0 (free) | 1M (1,048,576), salida hasta 262k | Closed-weight, hybrid reasoning conmutable (thinking on/off por request), texto+imagen (hasta 200 imgs/req), tools. Variante `:free` sin costo, con rate limits. Sin EU routing. |
| Z.ai GLM 5.3 Flash | `z-ai/glm-5.3-flash:batch` | ~$0.075* | ~$0.25* | 1M (1,048,576), salida hasta 128k | MoE 320B (18B activos), texto+imagen+video in, tools + reasoning (`reasoning` + `reasoning_effort`), foco coding/agentic long-horizon. Variante `:batch` = ~50% descuento, mayor latencia. EU routing disponible (Inceptron). |

\* Precio batch ≈ 50% del estándar Z.ai ($0.15 in / $0.50 out). Proveedores más baratos del estándar: Relace ($0.0399/$0.0784).

## Evaluación de capacidades (verificado 2026-11-22)

Fuentes: páginas OpenRouter (parámetros aceptados: `tools`, `tool_choice`, `reasoning` en los 3) + specs oficiales (Tencent Hunyuan, InclusionAI, Z.ai).

### 1. Tool calling
| Modelo | Soporta | Paralelas | Nota |
|---|---|---|---|
| Hy4 Flash | ✅ (`tools` + `tool_choice`) | No documentado (estándar OpenAI-compatible, asumir secuencial/parcial) | Function Calling listado por Tencent Cloud. Sin dato de N paralelas. |
| Ling 3.2 Flash | ✅ (`tools` + `tool_choice`) | No documentado | Reportado en varias páginas de providers. Hybrid: con thinking off, tools más rápidos. |
| GLM 5.3 Flash | ✅ (`tools` + `tool_choice`, + `reasoning_effort`) | No documentado, pero diseñado para agentes | El más orientado a agentic: benchmarks coding + long-horizon agent tasks. Mejor candidato para tool calling intensivo. |

Ningún provider publica límite exacto de herramientas paralelas; los 3 usan el esquema OpenAI-compatible (múltiples `tool_calls` por turno según el modelo decida).

### 2. Reasoning
| Modelo | Tipo |
|---|---|
| Hy4 Flash | Nativo ("Deep Reasoning" según Tencent). Parámetro `reasoning` aceptado en OpenRouter. Sin control de esfuerzo. |
| Ling 3.2 Flash | Híbrido conmutable: thinking on/off por request. Ideal para modo rápido (off) vs análisis (on). |
| GLM 5.3 Flash | Nativo + `reasoning_effort` ajustable. El más controlable para reasoning técnico graduado. |

### 3. Multimodal (imagen input)
- Hy4 Flash: texto+imagen ✅
- Ling 3.2 Flash: texto+imagen, hasta 200 imágenes/req ✅ (algunas fuentes mencionan video, no confirmado)
- GLM 5.3 Flash: texto+imagen+video ✅ (el más completo)

Ninguno genera imagen; solo texto de salida.

### 4. Español
Ningún benchmark público reporta calidad de español para estos 3 modelos flash (noviembre 2026, modelos muy recientes). Heurística:
- GLM (Z.ai): la familia GLM-4+ tiene el mejor multilingüe documentado de los tres; apuesta más segura para español neutro.
- Hy4 (Tencent Hunyuan): fuerte en chino/inglés; español funcional pero menos probado.
- Ling (InclusionAI): modelo más nuevo y menos evaluado; mayor incertidumbre.
- Matiz colombiano/cálido: depende del system prompt, no del modelo. Cualquiera de los 3 lo sigue si se instruye.

### 5. Contexto real útil y throughput
- Los 3 anuncian 1M tokens. Contexto útil real en modelos MoE flash suele degradarse pasado ~200-400k (needle-in-haystack); suficiente para delegación H.E.L.E.N. (tareas acotadas, no sesiones completas).
- Throughput: Hy4 Flash posicionado como "high-speed cost-efficient" (50T tokens día 1 según Tencent). GLM Flash: 18B activos → inferencia rápida. Ling: sin datos públicos.
- Salida máxima: Ling 262k > GLM 128k > Hy4 64k. Para sesiones largas con sliding window importa el input, no el output; los 3 sobran.

### 6. Límites free tier / batch
- Ling `:free`: costo $0, pero rate limits estrictos (típico OpenRouter free: ~20 req/min, 50-200 req/día según carga; puede dar 429 en picos). Reintentar con backoff o caer al siguiente fallback.
- GLM `:batch`: ~50% descuento, latencia de minutos-horas. Solo trabajo no urgente.
- Hy4: sin variante free/batch; pago directo baratísimo.

## FIT con H.E.L.E.N.

| Requisito | Hy4 Flash | Ling 3.2 Flash | GLM 5.3 Flash |
|---|---|---|---|
| (1) Tool calling intensivo | ⚠️ funciona, sin garantías agentic | ⚠️ funciona, mejor con thinking off | ✅ mejor opción (diseño agentic) |
| (2) Respuestas cortas Telegram rápido | ✅ rápido y barato | ✅ thinking off = ideal modo rápido | ⚠️ batch NO sirve; usar variante estándar |
| (3) Reasoning técnico DC | ⚠️ básico | ✅ hybrid on | ✅ mejor (`reasoning_effort`) |
| (4) Español neutro cálido | ⚠️ menos probado | ⚠️ incierto | ✅ apuesta más segura |
| (5) Sesiones largas sliding window | ✅ 1M | ✅ 1M + salida 262k | ✅ 1M |

## Veredicto por modelo

- **Tencent Hy4 Flash → rutinario/delegable (pago).** Baratísimo ($0.035/$0.14), rápido, tools+reasoning básicos. Rol: sustituto de pago cuando `:free` da 429. No para reasoning profundo ni español exigente.
- **InclusionAI Ling 3.2 Flash `:free` → rutinario/delegable (costo cero).** Primera opción de delegación (rol actual de dsv4): lecturas, sync, búsquedas. Thinking conmutable lo hace dual rápido/análisis. Riesgo: rate limits; siempre con fallback a Hy4.
- **Z.ai GLM 5.3 Flash → reasoning/complejo (estándar) + batch/no-urgente (`:batch`).** El único apto para delegación compleja: agentic, coding, reasoning graduado, mejor español. Variante `:batch` solo para evaluaciones masivas/reindexado, jamás interactivo.

## Orden fallback recomendado

1. **spark** (principal, reasoning, esta sesión)
2. **`inclusionai/ling-3.2-flash:free`** — costo cero, contexto 1M, salida 262k, thinking conmutable. Rutinario.
3. **`tencent/hy4-flash`** — pago mínimo, rápido. Rutinario cuando free falla.
4. **`z-ai/glm-5.3-flash`** (estándar, no batch) — delegación compleja: reasoning técnico, agentic, español exigente.
5. **`z-ai/glm-5.3-flash:batch`** — solo lotes no urgentes.

## Notas
- Los tres tienen ventana de 1M tokens: sin problema de contexto para delegación.
- `:free` y `:batch` son variantes de enrutamiento OpenRouter, no modelos distintos.
- Paralelismo de tools no documentado en ninguno; asumir comportamiento OpenAI-compatible.
- Español: sin benchmarks públicos (2026-11-22); reevaluar cuando haya evaluaciones multilingües.
- Reevaluar precios trimestralmente (los providers cambian tarifas).
