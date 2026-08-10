# Investigación: Discrepancia de costos Mimo V2.5 (OpenRouter) vs DeepSeek V4 Flash (API directa)

**Fecha:** 2026-08-09
**Objetivo:** Explicar por qué Mimo V2.5 vía OpenRouter costó ~2x más que DeepSeek V4 Flash directo, a pesar de que ambos comparten >90% de cache hit y precios de lista similares.

---

## Resumen ejecutivo

La discrepancia de ~2x **no se explica por un precio de cache-read más caro** (de hecho, el cache-read de Mimo en OpenRouter es *idéntico* al de DeepSeek directo: $0.0028/M). La explicación más probable y con mayor respaldo técnico es:

> **Mimo V2.5 NO soporta cache implícito/automático en OpenRouter** (`supports_implicit_caching: false` en TODOS sus proveedores, según la API oficial de OpenRouter), y **no aparece en la documentación oficial de prompt caching de OpenRouter** como proveedor con cache automático. DeepSeek, en cambio, sí tiene cache automático ("no requiere configuración adicional"). Por lo tanto, la tasa real de cache hit de Mimo fue muy inferior al 90%+ asumido, y una fracción mucho mayor de tokens de prompt se facturó al precio completo de cache-miss ($0.14/M), elevando el costo efectivo.

---

## 1. Precio oficial de cache-read de Mimo V2.5 (Xiaomi)

**No encontré documentación oficial de precios de la API de Xiaomi/Mimo.** El sitio `mimo.xiaomi.com` es una página de marketing sin sección de precios/API (verifiqué `/`, `/api`, `/mimo-code`, `/en/mimo-code` — todos 404 o sin contenido de precios). No hay página pública de pricing de la API de Xiaomi accesible.

**Lo que sí existe es el pricing listado por OpenRouter** (que pasa a través del precio del proveedor):

**Mimo V2.5 — proveedor "Xiaomi" (el principal) en OpenRouter** (fuente: API `/api/v1/models/xiaomi/mimo-v2.5-20260422/endpoints`):
- `prompt` (cache miss): **$0.14 / M tokens**
- `completion`: **$0.28 / M tokens**
- `input_cache_read` (cache hit): **$0.0028 / M tokens** → descuento de **50x** (0.02x) sobre el prompt

**Otros proveedores de Mimo V2.5 en OpenRouter** (misma fuente) — cada uno fija su propio cache-read:
| Proveedor | prompt | completion | cache-read |
|---|---|---|---|
| Xiaomi (fp8) | $0.14/M | $0.28/M | **$0.0028/M** |
| GMICloud (fp8) | $0.14/M | $0.28/M | $0.003/M |
| Novita (fp8) | $0.168/M | $0.336/M | $0.0034/M |
| Parasail (fp8) | $0.14/M | $0.28/M | $0.05/M |
| Venice (fp8) | $0.14/M | $0.28/M | $0.05/M |
| DeepInfra (bf16) | $0.40/M | $2.00/M | $0.08/M |

**Conclusión:** El cache-read oficial de Mimo V2.5 en OpenRouter es **$0.0028/M** (proveedor Xiaomi), el mismo valor que el cache-read de DeepSeek directo.

---

## 2. ¿Cómo aplica OpenRouter el descuento de cache para Mimo/Xiaomi?

**OpenRouter NO aplica su propio pricing de cache: pasa a través del precio del proveedor.** Cita oficial (FAQ de OpenRouter):

> "We pass through the pricing of the underlying providers; there is no markup on inference pricing" — https://openrouter.ai/docs/faq
> "OpenRouter passes through the pricing of the underlying providers... so you get the same pricing you'd get from the provider directly" — https://openrouter.ai/docs/faq

Cada proveedor (Xiaomi, GMICloud, Novita, Parasail, etc.) lista su propio `input_cache_read` en la API de OpenRouter, y OpenRouter lo factura tal cual.

**Punto crítico:** la API de OpenRouter reporta para **todos** los endpoints de Mimo V2.5:

```
"supports_implicit_caching": false
```

(verificado en los 6 proveedores: Xiaomi, Parasail, Venice, GMICloud, Novita, DeepInfra).

Esto significa que **Mimo V2.5 no tiene cache automático/implícito en OpenRouter**. El cache solo se activaría si el cliente envía marcadores explícitos (`cache_control` / `prompt_cache_breakpoint`) — y aun así, Mimo no aparece en la documentación de prompt caching de OpenRouter como proveedor soportado.

**Contraste con DeepSeek:** la documentación oficial de prompt caching de OpenRouter lista a DeepSeek explícitamente:

> "## DeepSeek ... Prompt caching with DeepSeek is automated and does not require any additional configuration." — https://openrouter.ai/docs/guides/best-practices/prompt-caching.md

La misma página define el multiplicador `DEEPSEEK_CACHE_READ_MULTIPLIER = '0.1'` y NO contiene ninguna sección para Xiaomi/MiMo. Los proveedores documentados son: OpenAI, Grok, Moonshot, Groq, Alibaba Qwen, Anthropic, DeepSeek, Z.AI, Google Gemini. **Xiaomi/MiMo no está en la lista.**

---

## 3. Documentación oficial sobre pricing de cache y cache retention

**OpenRouter (sí existe):**
- Guía de prompt caching: https://openrouter.ai/docs/guides/best-practices/prompt-caching.md
  - Explica los multiplicadores por proveedor, sticky routing, campos `cached_tokens` / `cache_write_tokens`, y qué proveedores tienen cache automático.
  - **No menciona Xiaomi/MiMo.**
- FAQ (pricing passthrough): https://openrouter.ai/docs/faq
- Modelo Mimo V2.5 (pricing + endpoints): https://openrouter.ai/xiaomi/mimo-v2.5

**Xiaomi/Mimo (NO encontré):**
- No hay página pública de pricing de la API de Xiaomi/Mimo accesible.
- `mimo.xiaomi.com` es solo marketing (sin precios ni docs de API).
- No encontré nota oficial de Xiaomi sobre el pricing de cache de Mimo.

**DeepSeek (sí, para referencia):**
- Pricing oficial directo: https://api-docs.deepseek.com/quick_start/pricing
  - Cache hit: **$0.0028/M**, cache miss: **$0.14/M**, output: **$0.28/M** (confirma los números del contexto).

---

## 4. ¿Por qué el cache hit del 90%+ no se traduce en el mismo ahorro?

**Respuesta corta:** porque el 90%+ de cache hit es real para DeepSeek (cache automático) pero **no se materializó para Mimo** (sin cache implícito). La premisa de que "ambos comparten >90% de cache hit" es probablemente incorrecta para Mimo.

**Análisis técnico:**

1. **DeepSeek directo:** tiene cache automático. El proveedor aplica el precio de cache-read ($0.0028/M) a los tokens cacheados de forma transparente. Con ~90% de hit, el costo efectivo baja a ~$0.0177/M. ✅

2. **Mimo vía OpenRouter:** `supports_implicit_caching: false` en todos los proveedores. Si las requests no incluyeron marcadores de cache explícitos (`cache_control`), **no hubo cache hit real** y los tokens de prompt se cobraron al precio completo de cache-miss ($0.14/M). Aunque OpenRouter *lista* un `input_cache_read` de $0.0028/M, ese precio solo se aplica si el cache realmente se activa.

3. **Verificación matemática:** Si Mimo hubiera tenido 90% de cache hit con cache-read a $0.0028/M, su costo efectivo habría sido cercano al de DeepSeek (~$0.018/M), NO $0.0332/M. El hecho de que costara ~2x indica que la **tasa real de cache hit de Mimo fue mucho menor** (o que el descuento de cache no se aplicó), de modo que una proporción mayor de tokens de prompt se facturó a $0.14/M.

4. **Causa del malentendido:** Es probable que el campo `cached_tokens` / la métrica de "cache hit" se interpretara como >90% para ambos, pero en Mimo el cache no se estaba aplicando de forma efectiva (o el sticky routing no estaba activo por no usar `session_id`, o no se enviaron `cache_control` breakpoints).

**Nota importante sobre DeepSeek vía OpenRouter:** el cache-read de DeepSeek V4 Flash en OpenRouter (p. ej. proveedor DeepInfra) es **$0.018/M** (0.2x del prompt), NO $0.0028/M como en la API directa. El $0.0028/M es el precio *directo* de DeepSeek. Esto refuerza que cada proveedor fija su propio cache-read y que la comparación correcta del contexto (DeepSeek directo vs Mimo vía OpenRouter) mezcla dos canales distintos.

---

## Conclusión

**No hay una aclaración oficial definitiva de Xiaomi** sobre el pricing de cache de Mimo (no existe documentación pública accesible). Sin embargo, la **evidencia de OpenRouter es clara y suficiente** para explicar la discrepancia:

1. **El cache-read de Mimo en OpenRouter NO es más caro** — es $0.0028/M (proveedor Xiaomi), idéntico al de DeepSeek directo.
2. **El problema es que Mimo no tiene cache automático en OpenRouter** (`supports_implicit_caching: false` en todos sus proveedores; Mimo ausente de la doc de prompt caching de OpenRouter).
3. **DeepSeek sí tiene cache automático** ("no requiere configuración adicional" — doc oficial de OpenRouter), por lo que su 90%+ de hit se traduce en ahorro real.
4. **Conclusión práctica:** el 90%+ de cache hit asumido para Mimo probablemente no se materializó. Para Mimo vía OpenRouter hay que **activar el cache explícitamente** (marcadores `cache_control` / `prompt_cache_breakpoint`, y usar `session_id` para sticky routing) — o el costo efectivo se queda en ~$0.0332/M en vez de ~$0.018/M.

---

## Fuentes citadas

| Afirmación | Fuente (URL) |
|---|---|
| Pricing Mimo V2.5 (prompt $0.14/M, cache-read $0.0028/M, `supports_implicit_caching: false`) | https://openrouter.ai/api/v1/models/xiaomi/mimo-v2.5-20260422/endpoints |
| Pricing DeepSeek V4 Flash (cache-read $0.018/M en OpenRouter) | https://openrouter.ai/api/v1/models/deepseek/deepseek-v4-flash-20260731/endpoints |
| DeepSeek cache automático; multiplicadores por proveedor; sin sección Xiaomi | https://openrouter.ai/docs/guides/best-practices/prompt-caching.md |
| OpenRouter pasa a través del pricing del proveedor (sin markup) | https://openrouter.ai/docs/faq |
| Pricing oficial DeepSeek directo (cache hit $0.0028/M) | https://api-docs.deepseek.com/quick_start/pricing |
| Página del modelo Mimo V2.5 en OpenRouter | https://openrouter.ai/xiaomi/mimo-v2.5 |
| Sitio oficial Xiaomi Mimo (sin pricing/API público) | https://mimo.xiaomi.com/ |

## Limitaciones / honestidad

- **No encontré documentación oficial de precios de la API de Xiaomi/Mimo.** El cache-read "oficial" de Mimo que reporto ($0.0028/M) proviene del listado de OpenRouter (proveedor Xiaomi), no de Xiaomi directamente.
- **No pude confirmar el desglose exacto de tokens/costos** de la prueba real del usuario (solo tengo los totales: 8.77M tokens / $0.291 para Mimo; 11.891M / $0.21 para DeepSeek). La explicación de la baja tasa real de cache hit de Mimo es la más plausible dados los datos, pero no puedo verificar el valor exacto de `cached_tokens` en esa sesión concreta.
- El flag `supports_implicit_caching: false` también aparece en los endpoints de DeepSeek V4 Flash de OpenRouter (p. ej. DeepInfra), lo que sugiere que OpenRouter marca el cache implícito de forma conservadora; sin embargo, la doc oficial de OpenRouter sí declara el cache de DeepSeek como automático, mientras que para Mimo no hay declaración equivalente.
