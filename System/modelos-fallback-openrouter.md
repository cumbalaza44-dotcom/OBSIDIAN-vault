# Modelos Fallback OpenRouter

Evaluación 2026-11-22. Principal: `spark` (muse-spark-1.3, reasoning).

## Tabla comparativa

| Modelo | ID OpenRouter | Input / 1M | Output / 1M | Contexto | Capacidades |
|---|---|---|---|---|---|
| Tencent Hy4 Flash | `tencent/hy4-flash` | $0.035 | $0.1405 | 1M (1,048,576), salida hasta 64k | Multimodal texto+imagen, reasoning, tools, hybrid attention (sparse+SWA). Open-weight 224B. Ideal tareas cotidianas a 1/20 del costo del flagship. |
| InclusionAI Ling 3.2 Flash | `inclusionai/ling-3.2-flash:free` | $0 (free) | $0 (free) | 1M (1,048,576), salida hasta 262k | Multimodal texto+imagen (hasta 200 imgs/req), reasoning conmutable, tools. Variante `:free` sin costo. |
| Z.ai GLM 5.3 Flash | `z-ai/glm-5.3-flash:batch` | ~$0.075* | ~$0.25* | 1M (1,048,576) | Texto+imagen, tools, reasoning. Variante `:batch` = procesamiento por lotes con ~50% descuento, mayor latencia. EU routing disponible (Inceptron). |

\* Precio batch ≈ 50% del estándar Z.ai ($0.15 in / $0.50 out). Proveedores más baratos del estándar: Relace ($0.0399/$0.0784).

## Orden fallback recomendado

1. **spark** (principal, reasoning, esta sesión)
2. **`inclusionai/ling-3.2-flash:free`** — costo cero, contexto 1M, salida generosa 262k. Ideal para lecturas/sync/búsquedas rutinarias (rol actual de dsv4). Riesgo: límites de tasa en tier free.
3. **`tencent/hy4-flash`** — baratísimo pago ($0.035/$0.14), 1M contexto, multimodal + tools. Mejor calidad/precio para reasoning ligero y tareas delegables cuando free falla.
4. **`z-ai/glm-5.3-flash:batch`** — solo para trabajo no urgente por lotes (evaluaciones masivas, reindexado). No apto para interactivo por latencia batch.

## Notas
- Los tres tienen ventana de 1M tokens: sin problema de contexto para delegación.
- `:free` y `:batch` son variantes de enrutamiento OpenRouter, no modelos distintos.
- Reevaluar precios trimestralmente (los providers cambian tarifas).
