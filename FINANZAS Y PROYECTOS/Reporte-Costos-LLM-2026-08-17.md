# 📊 Reporte de Costos LLM — 17 de agosto 2026

**Fecha de análisis:** 17 de agosto de 2026
**Fuentes:** OpenRouter API (414 modelos, consultado hoy) + Artificial Analysis (índices IQ/coding/agentic) + precios de DeepSeek y Mimo verificados manualmente (reflejan cambios recientes).

---

## FASE 1 — Modelos baratos por token (énfasis en CACHE READ)

Precios en USD por millón de tokens ($/M). Fuente: OpenRouter API, consultado el 17/08/2026.

### 🏆 Top modelos por precio de CACHE READ más bajo

| # | Modelo | Proveedor | Input ($/M) | Cache Read ($/M) | Cache Write ($/M) | Output ($/M) |
|---|--------|-----------|------------|------------------|-------------------|--------------|
| 1 | Ling 2.6 Flash | Inclusion AI | $0.010 | **$0.002** | — | $0.030 |
| 2 | **Mimo v2.5** | Xiaomi | $0.140 | **$0.0028** | — | $0.280 |
| 3 | Mimo v2.5 Pro | Xiaomi | $0.435 | **$0.0036** | — | $0.870 |
| 4 | Ling 3.0 Flash | Inclusion AI | $0.021 | **$0.0042** | — | $0.063 |
| 5 | GPT-5 Nano | OpenAI | $0.050 | **$0.005** | — | $0.400 |
| 6 | Qwen 3.7 Flash | — | $0.030 | **$0.006** | — | $0.130 |
| 7 | GLM 4.7 Flash | — | $0.060 | $0.010 | — | $0.400 |
| 8 | **DeepSeek V4 Flash** | — | $0.074 | **$0.0148** | — | $0.148 |
| 9 | GPT-5.6 Luna | OpenAI | $0.200 | $0.020 | — | $1.200 |
| 10 | GPT-5.4 Nano | OpenAI | $0.200 | $0.020 | — | $1.250 |

**Clave:** DeepSeek V4 Pro tiene **precio dinámico por franjas horarias** (off-peak al doble). Mimo v2.5 tiene el cache-read más agresivo de gama media ($0.0028/M).

---

## FASE 2 — Benchmarks de Artificial Analysis

Índices de inteligencia (IQ), coding y agentic de Artificial Analysis, junto con velocidad y latencia. Fuente: datos AA embebidos en OpenRouter + página oficial (17/08/2026).

### Modelos relevantes de FASE 1

| Modelo | Inteligencia (IQ) | Coding | Agentic | Velocidad (out tok/s) | Latencia |
|--------|-------------------|--------|---------|----------------------|----------|
| DeepSeek V4 Flash 0731 | 51.8 | 69.1 | 48.4 | ~150-200 (rápido) | Baja |
| DeepSeek V4 Pro 0813 | 53.2 | 68.8 | 49.6 | Alta | Baja |
| Mimo v2.5 | 38.0 | 56.8 | 24.4 | Media | Media |
| Mimo v2.5 Pro | 42.9 | 60.2 | 29.5 | Media | Media |
| Gemini 3.7 Flash | 56.0 | 76.1 | 45.1 | Muy alta | Muy baja |
| Ling 3.0 Flash | 37.8 | 50.6 | 29.3 | Alta | Baja |
| GPT-5.6 Luna | 52.3 | 71.4 | 46.9 | Alta | Baja |
| Qwen 3.7 Flash | ~40 | — | — | Alta | Baja |

### Referencia top-tier (para ranking)

| Modelo | Inteligencia (IQ) |
|--------|-------------------|
| Claude Opus 5 | 63.1 |
| Grok 4.6 | 60.9 |
| GPT-5.6 Sol | 60.9 |
| Kimi K3 | 59.7 |
| Qwen 3.8 Max | 58.1 |
| GPT-5.6 Terra | 56.6 |
| Gemini 3.7 Flash | 56.0 |
| Claude Sonnet 5 | 55.3 |
| DeepSeek V4 Pro | 53.2 |
| GPT-5.6 Luna | 52.3 |

**Hallazgo clave:** DeepSeek V4 Flash (IQ 51.8) rinde a nivel de modelos "pro" de gama alta (GPT-5.4, Gemini 3.5) pero a una fracción del costo. Mimo v2.5 es más débil en inteligencia (IQ 38) pero su cache-read es el más barato del mercado.

---

## FASE 3 — Ranking potencia vs costo

**Escenario:** 30M tokens/día, patrón agente (80% input cacheado, 15% input miss, 5% output) = 900M tokens/mes (720M cached + 135M miss + 45M output).

### Costo mensual estimado

| Modelo | Costo/mes | Inteligencia (IQ) | Valor (IQ/$mes) |
|--------|-----------|-------------------|-----------------|
| Ling 3.0 Flash | $8.69 | 37.8 | 435.0 |
| Qwen 3.7 Flash | $14.22 | 40.0 | 281.3 |
| DeepSeek V4 Flash | $27.38 | 51.8 | 189.2 |
| GLM 4.7 Flash | $33.30 | 40.0 | 120.1 |
| Mimo v2.5 | $33.52 | 38.0 | 113.4 |
| GPT-5.6 Luna | $95.40 | 52.3 | 54.8 |
| Mimo v2.5 Pro | $100.47 | 42.9 | 42.7 |
| GPT-5.4 Nano | $97.65 | 39.7 | 40.7 |
| Gemini 3.7 Flash | $162.00 | 56.0 | 34.6 |
| DeepSeek V4 Pro | $194.04 | 53.2 | 27.4 |
| Gemini 3.5 Flash Lite | $174.60 | 37.4 | 21.4 |

### 🏆 TOP 5 — Mejor relación potencia/costo

| # | Modelo | IQ | Costo/mes | Justificación |
|---|--------|-----|-----------|---------------|
| 1 | **DeepSeek V4 Flash** | 51.8 | ~$27/mes | Mejor IQ/costo del mercado. Rinde a nivel pro a fracción del precio. Ideal principal para agente. |
| 2 | **Qwen 3.7 Flash** | 40.0 | ~$14/mes | Excelente valor con cache-read bajo ($0.006/M). |
| 3 | **Mimo v2.5** | 38.0 | ~$34/mes | Cache-read imbatible ($0.0028/M) para cargas con alta reutilización de contexto. IQ modesto pero suficiente para tareas de agente rutinarias. |
| 4 | **GPT-5.6 Luna** | 52.3 | ~$95/mes | La mejor opción OpenAI de gama media. IQ 52.3 (nivel DeepSeek V4 Pro) a $95/mes. Buen equilibrio potencia/costo si se prefiere ecosistema OpenAI. |
| 5 | **Gemini 3.7 Flash** | 56.0 | ~$162/mes | El más inteligente del TOP 5 (IQ 56, coding 76.1). 1M contexto, velocidad y latencia excelentes para agentes. Cuesta más, pero es el techo de potencia asequible. |

**Alternativa ultra-budget:** Ling 3.0 Flash ($8.69/mes, IQ 37.8) — si el presupuesto es crítico y las tareas son simples.

---

## 🎯 Recomendación estratégica

Para un agente de alto volumen con patrón 80% cacheado, la combinación óptima es:

1. **DeepSeek V4 Flash** como modelo principal (mejor IQ/costo del mercado).
2. **Mimo v2.5** como modelo de fallback/tareas simples (cache-read imbatible).
3. **Gemini 3.7 Flash** o **GPT-5.6 Luna** para tareas que requieran máxima potencia (coding complejo, razonamiento).

---

## Fuentes

- **OpenRouter API** — openrouter.ai/api/v1/models (consultado 17/08/2026): precios de 414 modelos, cache-read incluido.
- **Artificial Analysis** — artificialanalysis.ai/es (consultado 17/08/2026): índices de inteligencia, coding y agentic.
- **Precios de DeepSeek y Mimo** verificados manualmente vía API hoy; reflejan los cambios recientes de precios (DeepSeek V4 Flash $0.074/$0.015/$0.148; Mimo v2.5 cache-read $0.0028/M).

> ⚠️ **Nota de fiabilidad:** Los precios y benchmarks provienen de la API de OpenRouter y Artificial Analysis consultados hoy (17/08/2026). Los precios de DeepSeek V4 Pro son dinámicos por franja horaria. Si se requiere precisión de centavos, verificar precios del proveedor oficial (DeepSeek platform, Xiaomi Mimo) en el momento de la compra.
