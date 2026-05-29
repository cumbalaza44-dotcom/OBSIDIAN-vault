# 💰 Análisis: < $20 USD para 30M tokens/día

*Última actualización: 2026-05-27*

## 📐 Requisitos calculados

| Parámetro | Valor |
|---|---|
| Tokens por día | 30,000,000 |
| Días del mes | 30 |
| **Total mensual** | **900,000,000 tokens** |
| Presupuesto máximo | $20 USD |
| **Precio máximo por 1M tokens** | **$0.022** |

---

## 🏷️ Comparativa de proveedores

### ✅ Modelos que CUMPLEN (< $20/mes)

| Proveedor | Modelo | Precio/1M input | Precio/1M output | Costo estimado/mes | ¿Cabe? |
|---|---|---|---|---|---|
| **DeepSeek** | V4 Flash | $0.01 | $0.01 | ~$18 | ✅ |
| **Groq** | Llama 3.1 8B (free) | $0 | $0 | $0 (con rate limit) | ✅ |
| **Groq** | Llama 3.1 8B (paid) | $0.05 | $0.05 | ~$90 | ⚠️ |
| **Google AI Studio** | Gemini 2.0 Flash (free) | $0 | $0 | $0 (con rate limit) | ✅ |
| **OpenRouter** | Modelos free | $0 | $0 | $0 (con rate limit) | ✅ |

### ⚠️ Modelos que NO cumple (> $20/mes)

| Proveedor | Modelo | Precio/1M output | Costo estimado/mes | Exceso |
|---|---|---|---|---|
| DeepSeek V4 Pro | V4 Pro | ~$0.27 | ~$243 | +2,230% |
| OpenAI GPT-4o-mini | 4o-mini | ~$0.15 | ~$135 | +1,150% |
| OpenAI GPT-4o | 4o | ~$5.00 | ~$4,500 | +22,400% |
| Anthropic Claude 3.5 Haiku | Haiku | ~$0.80 | ~$720 | +3,500% |
| Google Gemini 1.5 Pro | Pro | ~$1.25 | ~$1,125 | +5,525% |

---

## 🧩 Estrategias para lograrlo

### ✅ Estrategia VALIDADA: OpenClaw + Cache (recomendada)

**Sistema actual en producción:**
- Modelo: `openrouter/xiaomi/mimo-v2.5`
- Cache hit rate: **77%** (40k cached)
- Ratio input/output: **~5:1** (más input que output)

**Por qué funciona:**
- **77% del input** se cobra a precio reducido (cache)
- **Output real** es bajo (respuestas compactas)
- **Xiaomi MiMo** es de los modelos más baratos en OpenRouter
- **Fallback** a DeepSeek V4 Flash si falla

**Costo real estimado (OpenClaw):**
- Input total: 900M/mes → 77% cached = 693M cached + 207M fresh
- Output real: ~120M/mes (ratio 5:1)
- Precio Xiaomi MiMo: ~$0.02/1M input, ~$0.06/1M output
- **Costo estimado: $3-8/mes** ✅

**Componentes del éxito:**
- Cache layer nativo de OpenClaw
- Modelo barato (Xiaomi MiMo)
- Respuestas compactas (bajo output)
- Fallback a DeepSeek V4 Flash

### Otras opciones (alternativas)

#### Estrategia 1: Free tiers (riesgo alto)
- **Groq free** + **Google AI Studio free** + **OpenRouter free**
- Costo: $0
- Riesgo: Rate limits, disponibilidad variable, sin SLA

### Estrategia 2: DeepSeek V4 Flash (recomendada)
- Proveedor: DeepSeek
- Modelo: V4 Flash
- Costo: ~$18/mes
- Ventaja: más barato entre opciones pagas con SLA

### Estrategia 3: Hybrid (mixto)
- 70% tráfico → modelos free (Groq/Google)
- 30% tráfico → DeepSeek V4 Flash
- Costo estimado: ~$5-6/mes
- Balance: ahorro + fallback

### Estrategia 4: Self-hosting (open source)
- Modelos: Llama 3.1 8B, Mistral 7B, Qwen2 7B
- Infra: GPU alquilada (RunPod, Vast.ai, Lambda)
- Costo GPU: ~$10-25/mes (T4 o similar)
- Ventaja: control total, sin rate limits
- Riesgo: mantenimiento, uptime propio

---

## 🏗️ Arquitectura recomendada

```
                    ┌─────────────────┐
                    │   Rate Limiter   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
      ┌───────▼──────┐ ┌────▼─────┐ ┌──────▼──────┐
      │  Groq Free   │ │  Google  │ │  DeepSeek   │
      │  Llama 3.1   │ │ Gemini   │ │  V4 Flash   │
      │              │ │  Flash   │ │             │
      └───────┬──────┘ └────┬─────┘ └──────┬──────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │   Cache Layer   │
                    │  (Redis/Local)  │
                    └─────────────────┘
```

**Componentes clave:**
- **Cache** de respuestas frecuentes (reduce 30-50% llamadas)
- **Router inteligente** (priorizar free → fallback a paid)
- **Batch processing** para tareas no urgentes
- **Monitoring** de uso y costos diarios

---

## 📋 Checklist de implementación

- [ ] Crear cuentas en Groq, Google AI Studio, DeepSeek
- [ ] Obtener API keys
- [ ] Implementar cache layer
- [ ] Configurar rate limiter
- [ ] Configurar router de modelos
- [ ] Monitoreo de costos diario
- [ ] Alerta al 80% del presupuesto ($16)

| Opción                  | Pros                     | Contras                             |
| ----------------------- | ------------------------ | ----------------------------------- |
| Webhook                 | Notificación instantánea | Requiere configurar servidor en iOS |
| File watcher            | Detección en tiempo real | No aplica (iOS es remoto)           |
| Cron cada 5 min         | Proactivo                | Más tokens, más complejidad         |
| Atual (pull+cada turno) | Simple, confiable        | Solo actualiza cuando hay chat      |
