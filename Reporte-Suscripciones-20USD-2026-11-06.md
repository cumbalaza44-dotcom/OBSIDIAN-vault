# Reporte: Suscripciones ~$20/mes vs API para OpenClaw

**Fecha:** 2026-11-06 · **Para:** Mr. Jair (Medellín) · **Tope:** ~$20 USD/mes (sistema + ecosistema)

## 1. Gasto API actual estimado (screenshot OpenRouter Oct–Nov 2026)

Precios OpenRouter vigentes (nov 2026):

| Modelo | Tokens | Precio in / out (por 1M) | Supuesto split | Costo est. |
|---|---|---|---|---|
| Mimo-V2.6-Flash | 116M (81.8%) | $0.10–0.14 / $0.28 | 90M in + 26M out | **$16–20** |
| Muse Spark 1.3 contributor | 18.3M (12.9%) | $0.10 / $0.20 | 14M in + 4.3M out | **~$2.26** |
| DeepSeek V4 Flash 0731 | 4.53M (3.2%) | $0.046 / $0.137 | 3.5M in + 1M out | **~$0.30** |
| Resto (<1%) | ~2.4M | mixto | — | **~$1–2** |
| **TOTAL** | **~141.7M** | | | **~$19–24/mes** |

> **Conclusión:** ya gastas ≈ **$20/mes en puro API**. Estás justo en el tope. Cualquier suscripción chat se suma, no reemplaza, salvo que migres carga a OAuth.

## 2. Tabla comparativa suscripciones (precios nov 2026)

| Plan | Precio | ¿Incluye API credits? | ¿Sirve para OpenClaw? | Notas |
|---|---|---|---|---|
| **ChatGPT Plus** | $20/mes | ❌ No (API se paga aparte) | ⚠️ Parcial: **Codex OAuth** sí (usa cupo del plan; límites por modelo, ej. GPT-5.5 15–80 tareas; desde dic-2026 cupo compartido Chat+Codex) | Chat GPT-5 ilimitado gral.; Thinking ~3.000 msg/sem. Ideal ecosistema (imagen/video/Sora). |
| ChatGPT Pro | $200/mes | ❌ No | Mismo truco, más cupo | Fuera de presupuesto. |
| **Claude Pro** | $20/mes | ❌ No (Max/Team sí dan credits) | ⚠️ Parcial: **OAuth en Claude Code / Agent SDK** (uso individual ordinario; NO para backends de terceros). OpenClaw vía plugin/CLI con login propio puede funcionar, con límites 5h + semanal; Opus gasta más rápido | No es API key. Si OpenClaw usa OpenRouter → no aplica. |
| Claude Max | $100–200/mes | ✅ Sí (monthly API credits) | ✅ Pero caro | Fuera de tope. |
| **Google AI Pro** | $19.99/mes | ⚠️ **$10/mes en GenAI/Cloud credits** (único de los grandes que da algo) | ⚠️ App Gemini 4x vs free (límite 5h + semanal); los $10 de credits rinden en API Flash/Lite | Mejor "híbrido" $20: chat + $10 API. Incluye 2TB, NotebookLM, Veo/Flow. |
| Google AI Ultra | $249/mes | ✅ Más credits | Fuera de tope | — |
| **xAI SuperGrok / X Premium** | $30/mes | ❌ No | ❌ Chat/app X + Grok; sin API | **Sobre el tope.** Descarta. |
| **Microsoft Copilot Pro** | $20/mes | ❌ (GitHub Copilot Pro $10/mes sí da 1.500 AI credits, distinto producto) | ❌ No alimenta OpenClaw | Solo ecosistema Office. |
| **Perplexity Pro** | $20/mes | ❌ (API aparte) | ❌ | Gran buscador, nulo para agentes. |
| **Zhipu GLM Coding Plan** | ~$18/mes | ✅ Credits coding (Claude Code/Cursor) | ✅ Si tu stack acepta GLM | Opción china barata p/ coding. |
| **Kimi / Moonshot membresía** | ~$19/mes | ⚠️ Mixto membresía + API medido | ⚠️ | Variable; contexto largo su fuerte. |
| **Qwen token plan** | $8–16/mes | ✅ Tokens, no subscripción pura | ✅ Vía API/OpenRouter | Barato pero no es "subscripción agente". |
| **Mistral** | — | API pay-go | ✅ Vía API | Sin plan $20 relevante. |
| **DeepSeek directo** | — | API baratísima ($0.05–0.45/M) | ✅ | Sin subscripción; tu 3.2% ya lo prueba. |

## 3. Punto CLAVE: chat ≠ API

- **Ninguna suscripción $20 incluye API key ilimitada.** OpenClaw consume vía API (OpenRouter u OAuth directo).
- **Trucos OAuth usables en agentes:**
  - **ChatGPT Plus → Codex OAuth / "Sign in with ChatGPT":** apps terceras descuentan del cupo del plan. Límites reales por modelo y tarea; desde dic-2026 **cupo único compartido Chat+Codex**. Útil si migras parte del trabajo a Codex/CLI, NO si sigues 100% OpenRouter.
  - **Claude Pro → login en Claude Code / Agent SDK:** permitido para uso individual ordinario; prohibido revenderlo como backend. OpenClaw con sesión OAuth propia puede aprovecharlo, sujeto a límite 5h + semanal.
  - **Google AI Pro → $10 credits:** es API de verdad (se descuenta a precio estándar). Modelos Flash rinden mucho con $10.
- **Regla de oro:** si tu OpenClaw seguirá en OpenRouter pay-as-you-go, la suscripción **no baja tu factura API**; solo añade valor ecosistema.

## 4. Veredicto suscripción vs API (tu caso)

- Gastas ~$20/mes en API con stack ultra-barato (Mimo 82% del volumen). Ningún plan $20 te da 140M tokens/mes vía API.
- ChatGPT Plus ($20) **duplicaría** tu gasto ($40) sin tocar la factura OpenRouter, salvo que muevas carga a Codex OAuth.
- Por tanto: **quédate en API pay-as-you-go como base**; solo añade suscripción si el valor ecosistema (chat, imagen, video, búsqueda) lo justifica dentro del tope → lo que obliga a **recortar API a ~$0–10** para no pasarte.

## 5. Recomendación: 3 escenarios con tope $20

### A. Máximo ahorro agente (recomendado) — ~$20
- **Sin suscripción.** Sigue 100% OpenRouter pay-as-you-go.
- Optimiza: fuerza Mimo/DeepSeek/Kimi baratos en `dsv4`, reserva Spark solo reasoning (ya lo haces: 81.8% Mimo 👏).
- Activa prompt-caching donde aplique (Mimo/Spark cache barato).
- Ecosistema gratis: Gemini free, ChatGPT free, Claude free para chat esporádico.

### B. Híbrido Google — ~$20
- **Google AI Pro $19.99** (4x Gemini app, 2TB, Veo/Flow, NotebookLM) + **$10 credits API incluidos**.
- Baja OpenRouter a ~$10 recortando Spark a la mitad (usa Gemini Flash vía credits para rutinario).
- Total: $19.99 + ~$0–10 API extra = $20–30 ⚠️ (ajusta para no pasarte; los $10 credits cubren ~50–100M tokens Flash).
- Mejor valor ecosistema por dólar.

### C. ChatGPT Plus + API mínimo — ~$20 (apretado)
- **ChatGPT Plus $20** (mejor ecosistema: GPT-5, imágenes, Sora/video, Codex OAuth con cupo).
- Recorta OpenRouter a <$5: mueve todo lo posible a Codex OAuth / chat, deja API solo para cron/H.E.L.E.N. autónoma.
- Riesgo: cupo Codex compartido desde dic-2026; si te pasas, pagas API extra y rompes el tope.
- Solo si usas mucho imagen/video/chat a diario.

### 🏆 Top recomendación
**Escenario A hoy** (ya estás optimizado en ~$20 API). Si quieres "sentir" una suscripción sin romper el tope, **prueba B un mes** (Google AI Pro): es la única que devuelve $10 en API real + ecosistema completo. Evita Plus + API full simultáneos ($40).

---
*Fuentes: pricing pages OpenAI/Anthropic/Google nov-2026 + OpenRouter model pages (Mimo-V2.6-Flash $0.10–0.14/$0.28; Spark-1.3-contributor $0.10/$0.20; DSV4-Flash-0731 $0.046/$0.137). Límites chat son dinámicos; cifras Thinking/Codex según release notes y help pages.*
