# Comparativa 4 candidatos OpenClaw — 2026-11-06

Precios frescos: `https://openrouter.ai/api/v1/models` (2026-11-06). Blended 3:1 = (3×in+out)/4. Blended 1:1 = (in+out)/2. Turno típico agente = 10k in + 3k out.

## 1. Tabla comparativa

| # | Modelo | $/M in | $/M out | Blend 3:1 | Blend 1:1 | Turno 10k+3k | Ctx | Tools | Reasoning |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `meta/muse-spark-1.3-contributor` | 0.10 | 0.20 | 0.125 | 0.150 | **$0.00160** | 1M | ✅ | ✅ nativo |
| 2 | `deepseek/deepseek-v4-flash` (0423) | 0.091 | 0.182 | 0.114 | 0.137 | **$0.00146** | 1M | ✅ | ✅ |
| 3 | `deepseek/deepseek-v4-flash-0731` | 0.0434 | 0.30 | 0.108 | 0.172 | **$0.00133** | 1M | ✅ | ✅ |
| 4 | `xiaomi/mimo-v2.6-flash` | 0.14 | 0.28 | 0.175 | 0.210 | **$0.00224** | 1M | ✅ | ✅ |

## 2. Inteligencia (benchmarks públicos)

| Modelo | SWE-bench Ver. | Agente (DeepSWE / T-Bench) | Tool calling | Español |
|---|---|---|---|---|
| Spark 1.3 | s/d público (DeepSWE v1.1 75.4%, T-Bench 2.1 88.8% reporte Meta) | ✅ flagship | ✅ | ✅ bueno |
| V4 Flash 0423 | ~73.7–79.0 (preview, según esfuerzo) | DeepSWE 7.3, T-Bench 61.8, Toolathlon 49.7 | ✅ (V4.1-Flash BFCL ~77%) | ✅ bueno |
| V4 Flash 0731 | s/d SWE-bench aislado (release oficial, supera al preview) | **DeepSWE 54.4, T-Bench 82.7, Toolathlon 70.3** | ✅ | ✅ bueno |
| Mimo 2.6 Flash | s/d SWE-bench público | DeepSWE v1.1 ~66–73 (datos Xiaomi) | ✅ | ✅ muy bueno |

Fuentes: model cards DeepSeek/HF, release Xiaomi mimo-v2-6, Artificial Analysis / Vals.ai (nov-2026).

## 3. 0423 vs 0731: el duelo clave

- **0731 es el release oficial** que reemplaza al preview 0423: muy superior en agenticidad (DeepSWE 54.4 vs 7.3, T-Bench 82.7 vs 61.8).
- **Precio invertido:** 0731 input ~2× más barato ($0.0434 vs $0.091) pero output ~65% más caro ($0.30 vs $0.182).
- **Punto de corte:** 0731 sale más barato solo si ratio in/out > ~2.5:1. Turno típico OpenClaw (10k+3k = 3.3:1) → gana 0731 ($0.00133 vs $0.00146).
- **Pero:** OpenClaw genera MUCHO output (tool calls, reasoning, respuestas largas). En sesiones con output pesado (ratio <2.5:1) el 0423 es más barato. Y el output caro del 0731 penaliza justo lo que un agente más hace.
- **Veredicto duelo:** 0731 = más inteligente y más barato en turnos input-heavy típicos. 0423 = más predecible/económico si tu sesión genera muchísimo output. A igualdad de precio, 0731 rinde más por dólar por ser mejor modelo.

## 4. Costo por turno OpenClaw (10k in + 3k out)

| Modelo | Costo/turno | 100 turnos/día | 3000 turnos/mes |
|---|---|---|---|
| 0731 | $0.00133 | $0.13 | ~$4.00 |
| 0423 | $0.00146 | $0.15 | ~$4.37 |
| Spark contrib | $0.00160 | $0.16 | ~$4.80 |
| Mimo 2.6 Flash | $0.00224 | $0.22 | ~$6.72 |

Todos ridículamente baratos (<$7/mes uso intensivo). El precio NO decide; decide la inteligencia.

## 5. Economía: tokens útiles por dólar

- **(a) Principal reasoning:** Spark 1.3-contrib (flagship, T-Bench 88.8%) o 0731 (T-Bench 82.7, input baratísimo). Empate técnico; Spark tiene mejor techo.
- **(b) Rutinario barato:** 0731 — input a $0.0434/M es imbatible para lecturas/sync con contexto grande. 0423 segundo.
- **(c) Failover:** 0423 — precio output estable y barato, modelo maduro; si el contributor rate-limitea, este sostiene sin sustos en factura.

Mimo 2.6 Flash: el más caro de los 4 (+40% vs Spark) sin ventaja demostrada en benchmarks públicos de agente. Solo tendría sentido por español/código específico Xiaomi. No recomendado como default.

## 6. Ranking final y recomendación

1. **`meta/muse-spark-1.3-contributor` — PRINCIPAL.** Mejor techo (T-Bench 88.8%), precio subsidiado $0.125 blended. Aprovéchalo mientras exista.
2. **`deepseek/deepseek-v4-flash-0731` — RUTINARIO + alterno principal.** Input más barato del mercado ($0.0434), agenticidad muy superior al 0423. Ideal para dsv4/rutinario y sesiones largas input-heavy.
3. **`deepseek/deepseek-v4-flash` (0423) — FAILOVER.** Output barato y estable ($0.182). Red de seguridad si contributor o 0731 fallan o si la sesión genera output extremo.
4. **`xiaomi/mimo-v2.6-flash` — descartado por ahora.** +40% precio sin evidencia de superioridad. Re-evaluar si salen SWE-bench/BFCL independientes.

**Configuración concreta:** principal `spark`, rutinario `0731` (reemplaza al 0423 actual en alias dsv4), failover `0423`.

## 7. Anexo: Artificial Analysis + veredicto proveedores 0731 (2026-11-06)

Fuente: artificialanalysis.ai (consultado 2026-11-06). Si el modelo exacto no existe en AA, se usa el más cercano y se anota.

| Modelo (AA) | Intelligence Index | Output speed AA | Precio AA ref | Nota |
|---|---|---|---|---|
| Muse Spark 1.3 (Max) | 37 (artículo 1.3: xhigh 61 / max 62) | ~12.7 min/tarea | $2.39/tarea | AA mide costo por tarea, no por token; el tier contributor de OpenRouter ($0.125 blended) es subsidio aparte |
| DeepSeek V3.2 (Reasoning, proxy de v4-flash) | 42 | 34 tok/s | ~$0.10/M ref | V4 Pro sube a 52; v4-flash hereda esa familia |
| DeepSeek V4 Flash (0423) | ~40-42 (familia V3.2/V4) | ~33 tok/s | ~$0.30/M ref | Modelo maduro, precio estable |
| Xiaomi MiMo-V2.6-Pro | 30 | 44.7 min/tarea (más rápido Xiaomi) | — | MiMo-V2.6-Flash: $0.13/tarea (el más barato Xiaomi) |

**Veredicto proveedor 0731 (screenshot usuario):**
- Baidu 90% off: $0.04576 in / $0.1373 out, 100 tok/s, latencia 0.75s → más barato en output.
- Wafer: $0.0448 in / $0.30 out, 173 tok/s, latencia 0.34s → más rápido (casi 2x) y menor latencia.
- Resto: $0.09–$0.44 in → fuera de competencia.
- Regla: sesiones output-heavy → Baidu; interactivas/latencia → Wafer.

**Confirmación economía spark-contributor:** ningún proveedor del 0731 ni ningún dato AA lo desbanca. Spark-contrib a $0.125 blended con T-Bench 88.8% sigue siendo rey económico: más inteligente que todo lo comparado y más barato que Mimo (+40%) y que cualquier 0731 con output caro. Veredicto del reporte (secciones 1–6) se mantiene.
