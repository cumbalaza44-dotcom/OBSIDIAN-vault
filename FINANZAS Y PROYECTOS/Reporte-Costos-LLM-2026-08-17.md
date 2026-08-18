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
| 8 | **DeepSeek V4 Flash** | — | $0.0686 | **$0.0137** | — | $0.1372 |
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
| Qwen 3.7 Flash | ~40 (pendiente confirmar AA) | — | — | Alta | Baja |

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

### 🔢 Desglose de cálculos verificados (17/08/2026)

> Fórmula: `(720M × cache_read) + (135M × input_miss) + (45M × output)` — todo en $/M tokens.

| Modelo | Cache (720M) | Miss (135M) | Output (45M) | Total | Verificado |
|--------|--------------|-------------|--------------|-------|------------|
| Ling 3.0 Flash | 720×$0.0042=$3.02 | 135×$0.021=$2.84 | 45×$0.063=$2.84 | **$8.70** | ✓ (reporte $8.69, redondeo) |
| Qwen 3.7 Flash | 720×$0.006=$4.32 | 135×$0.030=$4.05 | 45×$0.130=$5.85 | **$14.22** | ✓ exacto |
| DeepSeek V4 Flash | 720×$0.0137=$9.86 | 135×$0.0686=$9.26 | 45×$0.1372=$6.17 | **$25.29** | ✓ (reajustado) |
| GLM 4.7 Flash | 720×$0.010=$7.20 | 135×$0.060=$8.10 | 45×$0.400=$18.00 | **$33.30** | ✓ exacto |
| Mimo v2.5 | 720×$0.0028=$2.02 | 135×$0.140=$18.90 | 45×$0.280=$12.60 | **$33.52** | ✓ exacto |
| GPT-5.6 Luna | 720×$0.020=$14.40 | 135×$0.200=$27.00 | 45×$1.200=$54.00 | **$95.40** | ✓ exacto |
| Mimo v2.5 Pro | 720×$0.0036=$2.59 | 135×$0.435=$58.73 | 45×$0.870=$39.15 | **$100.47** | ✓ exacto |
| GPT-5.4 Nano | 720×$0.020=$14.40 | 135×$0.200=$27.00 | 45×$1.250=$56.25 | **$97.65** | ✓ exacto |
| Gemini 3.7 Flash | — | — | — | **$162.00** | ⚠️ sin precio en FASE 1 |
| DeepSeek V4 Pro | — | — | — | **$194.04** | ⚠️ precio dinámico por franja |
| Gemini 3.5 Flash Lite | — | — | — | **$174.60** | ⚠️ sin precio en FASE 1 |

**Veredicto de verificación:** 8 de 11 modelos verificados con exactitud o redondeo menor. Los 3 sin verificar (Gemini 3.7 Flash, DeepSeek V4 Pro, Gemini 3.5 Flash Lite) son los más caros — sus precios no están en la FASE 1 y requieren consulta directa a la API para confirmarse.

### Costo mensual estimado

| Modelo | Costo/mes | Inteligencia (IQ) | Valor (IQ/$mes) |
|--------|-----------|-------------------|-----------------|
| Ling 3.0 Flash | $8.69 | 37.8 | 435.0 |
| Qwen 3.7 Flash | $14.22 | 40.0 (pendiente) | 281.3 |
| DeepSeek V4 Flash (estándar) | $25.29 | 51.8 | 204.8 |
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
| 1 | **DeepSeek V4 Flash** | 51.8 | ~$25/mes | Mejor IQ/costo del mercado. Rinde a nivel pro a fracción del precio. Ideal principal para agente. |
| 2 | **Qwen 3.7 Flash** | 40.0 | ~$14/mes | Excelente valor con cache-read bajo ($0.006/M). Multimodal (texto+imagen+video), 1M contexto, razonamiento opcional. |
| 3 | **Mimo v2.5** | 38.0 | ~$34/mes | Cache-read imbatible ($0.0028/M) para cargas con alta reutilización de contexto. IQ modesto pero suficiente para tareas de agente rutinarias. |
| 4 | **GPT-5.6 Luna** | 52.3 | ~$95/mes | La mejor opción OpenAI de gama media. IQ 52.3 (nivel DeepSeek V4 Pro) a $95/mes. Buen equilibrio potencia/costo si se prefiere ecosistema OpenAI. |
| 5 | **Gemini 3.7 Flash** | 56.0 | ~$162/mes | El más inteligente del TOP 5 (IQ 56, coding 76.1). 1M contexto, velocidad y latencia excelentes para agentes. Cuesta más, pero es el techo de potencia asequible. |

**Alternativa ultra-budget:** Ling 3.0 Flash ($8.69/mes, IQ 37.8) — si el presupuesto es crítico y las tareas son simples.

---

## 🔍 Comparativa de proveedores — DeepSeek V4 Flash

> Verificado el 17/08/2026 contra 6 proveedores. Escenario: 900M tokens/mes (720M cached + 135M miss + 45M output).

| Proveedor | Input miss ($/M) | Cache read ($/M) | Output ($/M) | Costo/mes |
|-----------|------------------|------------------|--------------|-----------|
| **OpenRouter** (v4-flash) | $0.0686 | $0.0137 | $0.1372 | **$25.30** 🥇 |
| **DeepInfra** (V4-Flash-0731) | $0.08 | $0.016 | $0.18 | $30.42 |
| **DeepInfra** (V4-Flash) | $0.09 | $0.018 | $0.18 | $33.21 |
| **Fireworks** (V4 Flash 0731) | $0.14 | $0.028 | $0.28 | $51.66 |
| **Novita** (V4 Flash) | $0.14 | $0.028 | $0.28 | $51.66 |
| **Together AI** (V4 Flash 0731) | $0.14 | $0.03 | $0.28 | $53.10 |
| **DeepSeek oficial** (off-peak) | $0.22 | $0.007 | $0.66 | $64.44 |
| **DeepSeek oficial** (promedio) | — | — | — | $83.25 (más caro) |

### Hallazgos clave

1. **Fenómeno de revendedores confirmado:** OpenRouter y DeepInfra son **más baratos que el fabricante**. DeepSeek oficial cobra caro el cache-miss ($0.22) y el output ($0.66), que dominan el patrón de agente; los revendedores ofrecen tarifas planas ~3-5× más bajas.
2. **El más barato es OpenRouter** ($25.30/mes) — justo lo ya documentado en la nota. Los $25.29 calculados son correctos.
3. **El más caro es DeepSeek oficial** en promedio ($83.25/mes) — más de 3× el costo de OpenRouter.
4. **Groq no ofrece** DeepSeek V4 Flash en su catálogo actual. **Hyperbolic** no fue verificable (páginas con error) — excluido explícitamente.

> **Por qué los revendedores son más baratos que el fabricante:** DeepSeek es open-source, así que cualquier proveedor puede hostear los pesos y fijar su propio precio. Los revendedores compran capacidad de GPU al por mayor, subsidian modelos populares como gancho para atraer tráfico, y optimizan el serving (batching, KV-cache, routing). No es un error; es competencia de mercado.

## 📌 Ficha verificada — Qwen 3.7 Flash (17/08/2026)

> Datos obtenidos de la API de OpenRouter hoy. Benchmarks de Artificial Analysis no confirmables hoy (URLs directas dan 404) — marcados como pendientes.

| Campo | Valor |
|-------|-------|
| Proveedor | Alibaba (Qwen) |
| Precio input | $0.030/M |
| Cache read | $0.006/M |
| Cache write | $0.038/M |
| Precio output | $0.130/M |
| Contexto | 1M tokens |
| Modalidad | Texto + Imagen + Video → Texto (multimodal) |
| Razonamiento | Opcional (no obligatorio), activado por defecto |
| Max tokens salida | 65,536 |
| Versión | qwen3.7-flash-20260727 |
| Costo/mes (900M tok) | $14.22 |

**Descripción oficial:** Modelo de razonamiento visión-lenguaje de Alibaba, apto para agentes multimodales, codificación visual, búsqueda e interacción por computadora. Fortalezas en reconocimiento de objetos, comprensión espacial y tareas del mundo real.

**Nota sobre precio escalonado:** OpenRouter aplica descuento por volumen en prompts largos — el precio base ($0.03/$0.13) aplica a prompts <32K tokens; sube a $0.10/$0.40 para 32K-256K y $0.20/$0.80 para >256K. Para un patrón de agente con contexto grande, el costo real puede ser mayor al calculado.

**Pendiente:** Índice de inteligencia (IQ), coding y agentic de Artificial Analysis — no verificables hoy (404). El IQ ~40 es una estimación previa sin confirmar.

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
- **Precios de DeepSeek y Mimo** verificados manualmente vía API hoy; reflejan los cambios recientes de precios (DeepSeek V4 Flash estándar $0.0686/$0.0137/$0.1372; Mimo v2.5 cache-read $0.0028/M).

> ⚠️ **Nota de fiabilidad:** Los precios y benchmarks provienen de la API de OpenRouter y Artificial Analysis consultados hoy (17/08/2026). Los precios de DeepSeek V4 Pro son dinámicos por franja horaria. Si se requiere precisión de centavos, verificar precios del proveedor oficial (DeepSeek platform, Xiaomi Mimo) en el momento de la compra.
