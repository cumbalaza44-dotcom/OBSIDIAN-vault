# Comparación: Xiaomi MiMo-V2.5 vs DeepSeek V4 Flash

**Fecha de investigación:** 2026-08-09
**Objetivo:** Decidir cuál usar como modelo principal de un sistema de asistente tipo OpenClaw (mucho input repetido: system prompt, memoria, tools, historial).

> ⚠️ **Nota importante de honestidad:** Los datos de este reporte provienen de fuentes oficiales (HuggingFace, docs de DeepSeek, sitio oficial de MiMo) y de OpenRouter/Artificial Analysis (independientes). Donde un dato no está disponible o una afirmación de marketing no está respaldada por benchmarks independientes, se indica explícitamente. No se inventaron valores.

---

## 1. Especificaciones

| Especificación | MiMo-V2.5-Pro (Xiaomi) | DeepSeek V4 Flash 0731 (DeepSeek) |
|---|---|---|
| **Versión exacta** | MiMo-V2.5-Pro (2026-04-22) | DeepSeek-V4-Flash-0731 (2026-07-31, supersede al preview) |
| **Fecha de lanzamiento** | 22 de abril de 2026 | 31 de julio de 2026 |
| **Arquitectura** | MoE con atención híbrida (SWA+GA) + MTP (3 capas) | MoE disperso con módulo de decodificación especulativa DSpark |
| **Parámetros totales** | 1.02T | 284B |
| **Parámetros activos** | 42B | 13B |
| **Contexto máximo** | 1M tokens (1,050,000) | 1M tokens (1,048,576) |
| **Output máximo** | 131,072 tokens | 384,000 tokens |
| **Modo thinking** | Sí (razonamiento opcional, `reasoning` no obligatorio) | Sí (thinking/no-thinking; `reasoning_effort`: low/high/max) |
| **Multimodal** | MiMo-V2.5-Pro: texto→texto. (El modelo base MiMo-V2.5 sí es omni-modal: texto+imagen+audio+video) | Texto→texto |
| **Licencia** | Open source (HuggingFace) | MIT |
| **Tokenizador** | Otro (propio) | DeepSeek |

**Fuentes:**
- MiMo-V2.5-Pro: https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro
- DeepSeek-V4-Flash-0731: https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731
- DeepSeek API (contexto 1M, output máx 384K, thinking): https://api-docs.deepseek.com/
- Especificaciones de contexto/output de OpenRouter: https://openrouter.ai/api/v1/models

---

## 2. Benchmarks

### 2a. Benchmarks de agentes (fuente: modelo card oficial de DeepSeek-V4-Flash-0731)

Estos son los benchmarks de capacidades agénticas publicados por DeepSeek en su modelo card. Incluyen comparación con V4-Pro (Preview), GLM-5.2 y Opus-4.8.

| Benchmark | DeepSeek V4 Flash 0731 | V4 Flash (Preview) | V4 Pro (Preview) | GLM-5.2 | Opus-4.8 |
|---|---|---|---|---|---|
| Terminal Bench 2.1 | **82.7** | 61.8 | 72.1 | 81.0 | 85.0 |
| NL2Repo | **54.2** | 39.4 | 38.5 | 48.9 | 69.7 |
| Cybergym | **76.7** | 38.7 | 52.7 | - | 83.1 |
| DeepSWE | **54.4** | 7.3 | 12.8 | 46.2 | 58.0 |
| Toolathlon-Verified | **70.3** | 49.7 | 55.9 | 59.9 | 76.2 |
| Agents' Last Exam | **25.2** | 15.8 | 16.5 | 23.8 | 25.7 |
| AutomationBench Public | **25.1** | 10.8 | 12.8 | 12.9 | 27.2 |
| DSBench-FullStack † | **68.7** | 37.0 | 41.8 | 61.8 | 71.6 |
| DSBench-Hard † | **59.6** | 25.8 | 31.1 | 54.5 | 71.7 |

† DSBench-FullStack y DSBench-Hard son test sets internos de DeepSeek (no públicos).

**Fuente:** https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731

> **Observación clave:** DeepSeek-V4-Flash-0731 **supera a su propio V4-Pro (Preview)** en todos estos benchmarks de agentes, pese a tener muchos menos parámetros activos (13B vs 49B). Esto la hace muy relevante para uso agéntico tipo OpenClaw.

### 2b. Benchmarks de modelo base (fuente: modelo card de MiMo-V2.5-Pro)

Xiaomi publicó una tabla comparativa de modelos base (sin post-training) que incluye a DeepSeek-V4-Flash. Estos son valores de **modelos base**, no del modelo final de chat.

| Benchmark | MiMo-V2.5-Pro Base | MiMo-V2.5 Base | DeepSeek-V4-Pro Base | DeepSeek-V4-Flash Base | Kimi-K2 Base |
|---|---|---|---|---|---|
| **Params activos/total** | 42B/1.02T | 15B/310B | 49B/1.6T | 13B/284B | 32B/1.04T |
| MMLU (5-shot) | **89.4** | 86.3 | 90.1 | 88.7 | 87.8 |
| MMLU-Pro (5-shot) | 68.5 | 65.8 | **73.5** | 68.3 | 69.2 |
| MMLU-Redux | **92.8** | 89.8 | 90.8 | 89.4 | 90.2 |
| GPQA-Diamond | **66.7** | 58.1 | - | - | 48.1 |
| MATH (4-shot) | **86.2** | 67.7 | 64.5 | 57.4 | 70.2 |
| GSM8K (8-shot) | **99.6** | 83.3 | 92.6 | 90.8 | 92.1 |
| HumanEval+ (1-shot) | 75.6 | 71.3 | - | - | **84.8** |
| MBPP+ (3-shot) | **74.1** | 70.9 | - | - | 73.8 |
| LiveCodeBench v6 (1-shot) | **39.6** | 35.5 | - | - | 26.3 |
| SWE-Bench AgentLess (3-shot) | **35.7** | 30.8 | - | - | 28.2 |
| BBH (3-shot) | 88.4 | 87.2 | 87.5 | **86.9** | 88.7 |
| C-Eval (chino) | 91.5 | 88.6 | **93.1** | 92.1 | 92.5 |
| GlobalMMLU (multilingüe) | **83.6** | 77.4 | - | - | 80.7 |

**Fuente:** https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro

> **Nota:** Estos son modelos *base*. MiMo-V2.5-Pro Base gana en MATH, MMLU-Redux, GPQA-Diamond y LiveCodeBench, pero **pierde en HumanEval+ frente a Kimi-K2** y DeepSeek no reporta varios de estos valores en esta tabla. Los valores de DeepSeek-V4-Flash en esta tabla son del modelo base y no reflejan el modelo final de chat (que es el que se usa en producción).

### 2c. Índices independientes (Artificial Analysis, vía OpenRouter)

| Índice | MiMo-V2.5-Pro | MiMo-V2.5 (omni) | DeepSeek V4 Flash 0731 |
|---|---|---|---|
| Intelligence Index | 42.9 | 38.0 | **51.8** |
| Coding Index | 60.2 | 56.8 | **69.1** |
| Agentic Index | 29.5 | 24.4 | **48.4** |

**Fuente:** https://openrouter.ai/api/v1/models (campo `benchmarks.artificial_analysis`)

> **⚠️ Discrepancia importante y honesta:** Xiaomi afirma en su sitio que MiMo-V2.5-Pro "rivaliza con Claude Opus 4.6 en cargas de trabajo agénticas" (https://mimo.mi.com/). Sin embargo, el **índice agéntico independiente de Artificial Analysis es mucho más bajo para MiMo-V2.5-Pro (29.5) que para DeepSeek V4 Flash (48.4)**. La afirmación de marketing de Xiaomi no está respaldada por el benchmark independiente disponible. No encontré benchmarks públicos de MiMo-V2.5-Pro en los mismos test sets agénticos (Terminal Bench, Toolathlon) que DeepSeek publica.

### 2d. Long context

- **MiMo-V2.5-Pro:** Xiaomi reporta en su modelo card una evaluación de long-context (GraphWalks de OpenAI) donde V2.5-Pro mantiene rendimiento a 512k (0.56 BFS / 0.92 Parents) y 1M (0.37 / 0.62), mientras que V2 Pro colapsa a 0.00 a 1M. Fuente: https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro
- **DeepSeek V4 Flash:** El paper técnico se titula "DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence" (https://arxiv.org/abs/2606.19348). DeepSeek no publicó en el modelo card una tabla de long-context comparable a GraphWalks. Ambos soportan 1M de contexto.

---

## 3. Capacidades

| Capacidad | MiMo-V2.5-Pro | DeepSeek V4 Flash 0731 |
|---|---|---|
| **Tool calling** | Sí (OpenAI/Anthropic compatibles) | Sí (OpenAI/Anthropic compatibles) |
| **JSON mode** | Sí (`response_format`, `structured_outputs`) | Sí (`response_format`, `structured_outputs`) |
| **Responses API** | No indicado | Sí (solo V4 Flash, no V4 Pro) |
| **Chat prefix / FIM** | No indicado | Sí (FIM solo en non-thinking) |
| **Velocidad** | MTP 3 capas (triplica velocidad de output en inferencia según Xiaomi) | DSpark speculative decoding (acelera output) |
| **Calidad en español** | No hay benchmark específico publicado; GlobalMMLU multilingüe 83.6 (base) | No hay benchmark específico publicado |
| **Contexto largo** | 1M (con atención híbrida SWA/GA, reduce KV-cache ~7x) | 1M (optimizado para contexto millón-token) |
| **Integración OpenClaw** | MiMo tiene un producto llamado "MiMo Claw" con integración nativa de OpenClaw | DeepSeek documenta integración con agentes (Claude Code, Copilot, OpenCode) |

**Fuentes:**
- MiMo capacidades: https://mimo.mi.com/ y https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro
- DeepSeek capacidades: https://api-docs.deepseek.com/ y https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731

---

## 4. Precios (por millón de tokens)

| Concepto | MiMo-V2.5-Pro | DeepSeek V4 Flash 0731 |
|---|---|---|
| **Input (cache hit)** | $0.0036 | **$0.0028** |
| **Input (cache miss)** | $0.435 | **$0.14** |
| **Output** | $0.87 | **$0.28** |
| Concurrencia | No indicado | 2500 (alto) |

**Para contexto, MiMo-V2.5 (omni, no-Pro):** $0.0028 cache-hit / $0.14 cache-miss / $0.28 output. (O sea, el MiMo-V2.5 base tiene exactamente el mismo precio que DeepSeek V4 Flash.)

**Fuentes:**
- Precios oficiales DeepSeek: https://api-docs.deepseek.com/quick_start/pricing
- Precios oficiales MiMo: https://mimo.mi.com/ y OpenRouter: https://openrouter.ai/api/v1/models

> **⚠️ Advertencia oficial de DeepSeek:** En su página de precios, DeepSeek indica: *"Planeamos subir el precio general de los servicios de la API de DeepSeek en el futuro cercano, con un aumento significativo esperado."* (https://api-docs.deepseek.com/quick_start/pricing). Esto es relevante para decisiones de largo plazo.

---

## 5. Pros y contras

### MiMo-V2.5-Pro (Xiaomi)

**Pros:**
- Muy fuerte en razonamiento matemático y científico en modelo base (MATH 86.2, GPQA-Diamond 66.7, GSM8K 99.6).
- Arquitectura eficiente (1.02T total / 42B activos) con atención híbrida que reduce KV-cache ~7x y MTP que triplica velocidad de output.
- 1M de contexto con buen mantenimiento de rendimiento hasta 512k-1M (GraphWalks).
- Open source, con integración nativa de OpenClaw (producto "MiMo Claw").
- Familia omni-modal (MiMo-V2.5 base procesa imagen, audio, video).

**Contras:**
- **Índice agéntico independiente bajo (29.5 en Artificial Analysis)** — la afirmación de "rivaliza con Claude Opus 4.6 en agentic" no está respaldada por benchmarks independientes.
- **Mucho más caro** que DeepSeek V4 Flash: input cache-miss $0.435 vs $0.14, output $0.87 vs $0.28 (~3x más caro).
- No publica benchmarks agénticos en test sets estándar comparables (Terminal Bench, Toolathlon) en su modelo card.
- Solo texto (la versión Pro); el modelo omni-modal es la variante no-Pro.

### DeepSeek V4 Flash 0731

**Pros:**
- **Excelente en capacidades agénticas** (Terminal Bench 2.1: 82.7, Toolathlon: 70.3, Cybergym: 76.7) — supera a su propio V4-Pro (Preview) en todos los benchmarks de agentes.
- **Muy barato** con cache: input cache-hit $0.0028, cache-miss $0.14, output $0.28. Ideal para mucho input repetido (system prompt, memoria, tools).
- 1M contexto + hasta 384K output (el más alto de los dos).
- Índices independientes más altos (intelligence 51.8, coding 69.1, agentic 48.4).
- Alto límite de concurrencia (2500), MIT license, DSpark speculative decoding para velocidad.
- Es el modelo con el que ya estoy ejecutando (DeepSeek V4 Flash).

**Contras:**
- Modelo base pierde en algunos benchmarks de razonamiento puro frente a MiMo-V2.5-Pro Base (MATH 57.4 vs 86.2, MMLU-Pro 68.3 vs 68.5).
- Solo texto (sin multimodal).
- **Precios subirán significativamente** según aviso oficial de DeepSeek (aunque incluso subiendo, probablemente siga muy por debajo de MiMo-Pro).
- Output máximo de 384K recomendado solo para reasoning high/max (consume más).

---

## 6. Recomendación para uso tipo OpenClaw

**Recomendación clara: DeepSeek V4 Flash 0731.**

Razones para el caso de uso específico (asistente OpenClaw con mucho input repetido — system prompt, memoria, tools, historial):

1. **Costo con cache-read es el factor decisivo.** OpenClaw reenvía constantemente el mismo system prompt, memoria y definiciones de tools. Con cache-read a **$0.0028/M** (DeepSeek) vs **$0.0036/M** (MiMo-Pro), y sobre todo en cache-miss **$0.14 vs $0.435** y output **$0.28 vs $0.87**, DeepSeek es ~3x más barato. Para un asistente de uso intensivo y continuo, esto es enorme.

2. **Capacidades agénticas superiores y verificadas.** El corazón de OpenClaw es el tool calling / ejecución de agentes. DeepSeek V4 Flash 0731 tiene benchmarks agénticos públicos excelentes (Terminal Bench 82.7, Toolathlon 70.3) y un índice agéntico independiente de 48.4 vs 29.5 de MiMo-Pro. MiMo no publica benchmarks agénticos comparables en test sets estándar.

3. **Output máximo más alto** (384K vs 131K) — útil para tareas largas de agente.

4. **Alto límite de concurrencia** (2500) — escala bien.

**Cuándo elegir MiMo-V2.5-Pro:**
- Si necesitas razonamiento matemático/científico puro de alto nivel (MATH, GPQA) y el costo no es problema.
- Si valoras el ecosistema "MiMo Claw" con integración nativa de OpenClaw y el plan de suscripción ¥14.9/mes.
- Si necesitas multimodal (en ese caso usarías MiMo-V2.5 base, no el Pro).

**Advertencias finales:**
- La afirmación de marketing de MiMo ("rivaliza con Claude Opus 4.6 en agentic") no está respaldada por benchmarks independientes.
- DeepSeek avisó que subirá precios. Si el costo es crítico, monitorea esa página.
- No hay datos públicos de velocidad (tokens/seg) comparables, ni benchmarks de calidad en español específicos para ninguno de los dos.

---

## 7. Fuentes

| Fuente | URL |
|---|---|
| Sitio oficial MiMo (precios, capacidades) | https://mimo.mi.com/ |
| Modelo card MiMo-V2.5-Pro (specs + benchmarks) | https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro |
| Docs API DeepSeek (specs, thinking, JSON, tools) | https://api-docs.deepseek.com/ |
| Precios oficiales DeepSeek | https://api-docs.deepseek.com/quick_start/pricing |
| Modelo card DeepSeek-V4-Flash-0731 (benchmarks agentes) | https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731 |
| Paper técnico DeepSeek-V4 | https://arxiv.org/abs/2606.19348 |
| OpenRouter (pricing + Artificial Analysis + specs) | https://openrouter.ai/api/v1/models |
