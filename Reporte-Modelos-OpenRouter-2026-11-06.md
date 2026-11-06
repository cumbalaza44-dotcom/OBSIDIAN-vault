# Comparativa OpenRouter vs Muse Spark 1.3 — 2026-11-06

Fuente de precios: `https://openrouter.ai/api/v1/models` (consultado 2026-11-06). Precios convertidos a **$/M tokens** (API da $/1k → ×1000). Blended = (3×in + out)/4.

## 0. Modelo actual

| Modelo | $/M in | $/M out | Blended 3:1 | Ctx | Tools | Reasoning |
|---|---|---|---|---|---|---|
| `meta/muse-spark-1.3-contributor` | **0.10** | **0.20** | **0.125** | 1M | ✅ | ✅ nativo |
| `meta/muse-spark-1.3` (tier normal) | 1.25 | 4.25 | 2.00 | 1M | ✅ | ✅ nativo |

Benchmarks Spark 1.3 (reporte oficial Meta): DeepSWE v1.1 **75.4%**, Terminal-Bench 2.1 **88.8%**, SWE-Atlas QnA 59.4%. Sin score público SWE-bench Verified.
⚠️ El tier **contributor es ~16× más barato** que el normal: es precio subsidiado/experimental. Todo el análisis se hace contra este precio.

## 1. Candidatos (precios frescos OpenRouter)

| # | Modelo (id exacto) | $/M in | $/M out | Blended | Ctx | Tools | Reasoning | vs Spark |
|---|---|---|---|---|---|---|---|---|
| 1 | `deepseek/deepseek-v4-flash` | 0.091 | 0.182 | **0.114** | 1M | ✅ | ✅ | ~igual, levemente más barato; SWE-b Verified ~80% (fam. V4 Pro 80.6%) |
| 2 | `openai/gpt-oss-120b` | 0.02 | 0.075 | **0.034** | 128K | ✅ | ✅ | **más débil** en código/agente general; imbatible en precio |
| 3 | `xiaomi/mimo-v2.6-flash` | 0.14 | 0.28 | 0.175 | 1M | ✅ | ✅ | nivel medio-alto, bueno en ES/código; un poco más caro |
| 4 | `z-ai/glm-5.3-flash` | 0.15 | 0.50 | 0.24 | 1M | ✅ | ✅ | buen agente/código; ~2× el precio |
| 5 | `z-ai/glm-5.3` | 0.07 | 1.40 | 0.40 | 1M | ✅ | ✅ | flagship Z.ai, SWE-b Ver. 77.8%; output caro |
| 6 | `qwen/qwen3.8-flash` | 0.15 | 0.47 | 0.23 | 1M | ✅ | ✅ | sólido código/herramientas; ~2× precio |
| 7 | `xiaomi/mimo-v2.6-pro` | 0.435 | 0.87 | 0.54 | 1M | ✅ | ✅ | flagship Xiaomi >1T; ~4× precio, posible upgrade real |
| 8 | `deepseek/deepseek-v4-pro` | 0.79 | 1.58 | 0.99 | 1M | ✅ | ✅ | 1.6T MoE, SWE-b Ver. 80.6%; ~8× precio |
| 9 | `moonshotai/kimi-k2.5` | 0.50 | 2.50 | 1.00 | 256K | ✅ | ✅ | gran coding visual/agente; ~8× precio, ctx menor |
| 10 | `moonshotai/kimi-k3.1-pro` | 2.00 | 10.00 | 4.00 | 1M | ✅ | ✅ | flagship Moonshot; ~32× precio |
| 11 | `qwen/qwen3-coder-next` | 0.12 | 0.80 | 0.29 | 256K | ✅ | parcial | especialista código, barato; no generalista |
| 12 | `mistralai/devstral-2512` | 0.40 | 2.00 | 0.80 | 256K | ✅ | — | especialista código 123B; ~6× precio |
| 13 | `meta-llama/llama-4-maverick` | 0.35 | 1.00 | 0.51 | 512K | ✅ | — | buen open, sin reasoning nativo; ~4× precio |

Benchmarks de terceros (SWE-bench Verified / BFCL v4, nov-2026): DeepSeek V4 Pro **80.6%**, GLM-5 **77.8%**, Kimi K2.5 76.8%, Qwen3.8 Max BFCL 77.2%, DeepSeek V4.1-Flash BFCL 77.0%.

## 2. Filtro: igualan o superan a Spark Y cuestan igual o menos (blended ≤ $0.125/M)

| Pasa el filtro | Blended | Veredicto capacidad |
|---|---|---|
| `deepseek/deepseek-v4-flash` (0.114) | ✅ más barato | ✅ Igual: 1M ctx, tools, reasoning, benchmarks V4 ≥ Spark |
| `openai/gpt-oss-120b` (0.034) | ✅ 4× más barato | ⚠️ Casi: reasoning+tools OK, pero un escalón abajo en código/agente y ctx 128K |
| `qwen/qwen3-coder-next` (0.29) | ❌ 2.3× más caro | Solo código; no pasa precio |
| Todo flagship (GLM-5.3, Kimi, Qwen Max, V4 Pro, Mimo Pro) | ❌ 2–32× más caro | Superan a Spark pero NO a igual/menor precio |

**Conclusión del filtro: solo `deepseek-v4-flash` iguala capacidad a menor precio. `gpt-oss-120b` es el único dramáticamente más barato con capacidad aceptable (concesión real).**

## 3. Ranking top 5 y recomendación

1. **`meta/muse-spark-1.3-contributor` — SEGUIR como principal.** $0.125 blended, flagship con reasoning, 1M ctx. Nada lo supera a este precio; el precio es subsidiado, aprovéchalo mientras exista.
2. **`deepseek/deepseek-v4-flash` — alterno principal / failover.** Prácticamente mismo precio ($0.114), benchmarks V4 de 80% en SWE-bench, 1M ctx. Úsalo si el contributor rate-limitea o se acaba el subsidio.
3. **`openai/gpt-oss-120b` — rutinario barato (reemplaza dsv4 si quieres).** $0.034 blended (~4× más barato que spark-contrib). Para lecturas, sync, búsquedas, tareas simples. No para reasoning pesado (ctx 128K, un escalón abajo).
4. **`xiaomi/mimo-v2.6-flash` — rutinario alternativo.** $0.175 blended, 1M ctx, buen español (Xiaomi), reasoning. Un poco más caro que spark-contrib; solo tiene sentido si buscas variedad.
5. **`xiaomi/mimo-v2.6-pro` — upgrade pago cuando el precio no importe.** $0.54 blended (~4×), flagship >1T. Candidato a principal premium si el contributor sube de precio.

### Configuración sugerida
- Principal: `spark` (contributor) — sin cambio.
- Rutinario: cambiar `dsv4` → `openai/gpt-oss-120b` para lo trivial ($0.034/M), o mantener `deepseek-v4-flash` como rutinario "casi gratis pero capaz".
- Failover principal: `deepseek/deepseek-v4-flash`.
- Vigilar: si `muse-spark-1.3-contributor` pierde el subsidio (salta a $2.00 blended del tier normal), el reemplazo principal pasa a ser `deepseek-v4-flash` y el premium `mimo-v2.6-pro`/`glm-5.3`.
