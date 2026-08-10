# Guía práctica: Cómo se cobran los modelos de generación de imágenes en OpenRouter

> **Para:** Mr. Jair (Medellín) · **Actualizado:** 2026-08-09
> **Fuente principal:** API oficial de OpenRouter (`/api/v1/images/models` y endpoints por modelo), consultada en vivo.

---

## 1. ¿Cómo se cobran los modelos de imágenes en OpenRouter?

**Respuesta corta: NO se cobran igual que los LLMs de texto.** Aunque algunos usan "tokens", el modelo de facturación de imágenes es distinto y más variado.

OpenRouter tiene una **API de imágenes dedicada** (`/api/v1/images`) separada de la de chat. Cada modelo expone sus propias "líneas facturables" (`billable`) con una **unidad** (`unit`) y un **costo por unidad** (`cost_usd`). Las unidades que existen son **tres**:

| Unidad de cobro | Qué significa | Ejemplos |
|---|---|---|
| **`image`** (por imagen) | Pagas un precio fijo por cada imagen generada, sin importar los píxeles exactos | Qwen Image, Seedream 4.5, Recraft, Riverflow, Grok Imagine |
| **`megapixel`** (por megapíxel) | El costo escala con la resolución: más píxeles = más caro | FLUX.2 (Klein, Pro, Flex, Max) |
| **`token`** (por token) | El texto del prompt se cobra como tokens, y la imagen generada se factura como un número fijo de "tokens de salida" | OpenAI GPT Image, Google Nano Banana (Gemini), Microsoft MAI |

**Diferencia clave con los LLMs de texto:** En un LLM de texto pagas **por token** (prompt + completion) y el costo varía con la longitud. En imágenes, la mayoría de modelos tienen un **cargo fijo por imagen** (`output_image`) que es la parte dominante del costo, más un cargo pequeño por el texto del prompt y por cada imagen de referencia que subas. El costo por imagen **no depende de "cuántas palabras" describan la imagen**, sino de la resolución y (en algunos) de la calidad elegida.

> **Fuente:** Documentación oficial de la API de imágenes — `https://openrouter.ai/docs/guides/overview/multimodal/image-generation.md` y `https://openrouter.ai/api/v1/images/models`

---

## 2. Catálogo de modelos de imágenes en OpenRouter (precios verificados)

Precios tomados **en vivo** del endpoint oficial `/api/v1/images/models/<modelo>/endpoints` (agosto 2026). Son precios por imagen generada (o por megapíxel/token según el modelo). Los precios pueden cambiar; verifica siempre en la API.

### 🔹 Alta calidad / gama alta

| Modelo | Unidad de cobro | Precio | Resolución máx. | Uso típico |
|---|---|---|---|---|
| **OpenAI GPT Image 2** (`openai/gpt-image-2`) | token (imagen = 0.00003/tok) | ≈ $0.13 por imagen 1536×864 "high" (ejemplo oficial) | hasta 4K según calidad | Mejor calidad general, edición, texto en imagen |
| **Google Nano Banana Pro** (`google/gemini-3-pro-image`) | token (imagen = 0.00012/tok) | ≈ $0.12 por imagen | 1K–4K | Calidad Pro, edición con contexto |
| **Google Nano Banana 2** (`google/gemini-3.1-flash-image`) | token (imagen = 0.00006/tok) | ≈ $0.06 por imagen | 512–4K | Excelente equilibrio calidad/velocidad |
| **FLUX.2 Max** (`black-forest-labs/flux.2-max`) | megapíxel | $0.07 / megapíxel | alta (escala por MP) | Máxima fidelidad, detalles finos |
| **Recraft V4.1 Pro** (`recraft/recraft-v4.1-pro`) | imagen | $0.21 / imagen | alta | Diseño, ilustración, branding |
| **Riverflow V2.5 Pro** (`sourceful/riverflow-v2.5-pro`) | imagen | $0.13 (1K) / $0.15 (2K) / $0.17 (4K) | 1K–4K | Producto comercial, 4K |

### 🟢 Económicos / rápidos

| Modelo | Unidad de cobro | Precio | Resolución máx. | Uso típico |
|---|---|---|---|---|
| **GPT Image 1 Mini** (`openai/gpt-image-1-mini`) | token (imagen = 0.000008/tok) | ≈ $0.008 / imagen | media | Prototipos, bocetos rápidos |
| **GPT-5 Image Mini** (`openai/gpt-5-image-mini`) | token (imagen = 0.000008/tok) | ≈ $0.008 / imagen | media | Generación económica con buen texto |
| **Nano Banana 2 Lite** (`google/gemini-3.1-flash-lite-image`) | token (imagen = 0.00003/tok) | ≈ $0.03 / imagen | 1K | Pipelines de alto volumen |
| **Nano Banana (2.5)** (`google/gemini-2.5-flash-image`) | token (imagen = 0.00003/tok) | ≈ $0.03 / imagen | media | Generación y edición económica |
| **FLUX.2 Klein 4B** (`black-forest-labs/flux.2-klein-4b`) | megapíxel | $0.014 / megapíxel | media | El más barato de FLUX, rápido |
| **FLUX.2 Pro** (`black-forest-labs/flux.2-pro`) | megapíxel | $0.03 / megapíxel | alta | Bueno y accesible |
| **Qwen Image 3** (`qwen/qwen-image-3`) | imagen | $0.03 (1K y 2K) | 1K–2K | Muy económico, buena calidad |
| **Seedream 4.5** (`bytedance-seed/seedream-4.5`) | imagen | $0.04 / imagen | 1K–4K | Texto en imagen, económico |
| **Grok Imagine** (`x-ai/grok-imagine-image-quality`) | imagen | $0.05 (1K) / $0.07 (2K) | 1K–2K | Imagen + texto, buen precio |
| **Riverflow V2.5 Fast** (`sourceful/riverflow-v2.5-fast`) | imagen | $0.019 (1K) / $0.021 (2K) | 1K–2K | Rápido y barato |
| **Recraft V4.1** (`recraft/recraft-v4.1`) | imagen | $0.035 / imagen | media | Diseño económico |

### 🖌️ Edición de imágenes (image-to-image)

| Modelo | Unidad | Precio | Uso típico |
|---|---|---|---|
| **GPT Image 2 / GPT-5 Image** | token | ver arriba | Edición con instrucciones en lenguaje natural |
| **Nano Banana Pro / 2** | token | ver arriba | Edición con contexto multimodal |
| **FLUX.2 Flex** (`black-forest-labs/flux.2-flex`) | megapíxel | $0.06/MP (input y output) | Edición; cobra imagen de entrada + salida |
| **Qwen Image 3 Pro** | imagen | $0.04 (1K) / $0.075 (2K) + $0.003 por imagen de entrada | Edición con referencia |
| **Recraft V4.1 Vector** (`recraft/recraft-v4.1-vector`) | imagen | $0.08 / imagen | Vectorización (SVG) |

> **Nota honesta:** Los modelos **Krea 2** (`krea/krea-2-*`) aparecen en el catálogo pero su precio **no está publicado** en el endpoint oficial de precios (array vacío). No invento su costo; consulta la página del modelo en OpenRouter antes de usarlos.

> **Fuente:** `https://openrouter.ai/api/v1/images/models` (catálogo) y `.../endpoints` (precios por proveedor). Ejemplo oficial de GPT Image 2 a $0.13: `https://openrouter.ai/docs/guides/overview/multimodal/image-generation.md`

---

## 3. Cómo interpretar el precio

### ¿Qué significa el "precio por imagen"?
Es el cargo por **cada imagen que generas** (campo `output_image`). Si pides `n` imágenes en una llamada, pagas `n × precio`. La mayoría de modelos permiten hasta 10 imágenes por llamada.

### ¿Varía con la resolución?
**Depende del modelo:**
- **Por imagen (fija):** modelos como Seedream o Qwen cobran lo mismo en 1K, pero algunos tienen **tiers por resolución** (ej. Riverflow: 1K=$0.13, 2K=$0.15, 4K=$0.17; Grok: 1K=$0.05, 2K=$0.07).
- **Por megapíxel (FLUX):** el costo **escala directamente** con la resolución. Una imagen 4K (≈8.3 MP) cuesta ~4× más que una 1K (≈1 MP).
- **Por token (OpenAI/Google):** el cargo de imagen es fijo, pero **la resolución y la calidad** cambian cuántos "tokens de salida" consume la imagen. Por eso GPT Image 2 en "high" cuesta más que en "low".

### Factores que suben el costo
1. **Resolución más alta** (1K → 2K → 4K) — sobre todo en modelos por megapíxel y por tiers.
2. **Calidad** (`quality: low/medium/high`) — afecta a OpenAI GPT Image; "high" consume más tokens.
3. **Edición vs generación** — editar cobra la **imagen de entrada** (`input_image` o `input_reference`) además de la salida. Ej. FLUX.2 Flex cobra $0.06/MP de entrada + $0.06/MP de salida; Riverflow cobra $0.20 por imagen de referencia.
4. **Cantidad (`n`)** — cada imagen extra se cobra por separado.
5. **Formato/vectores** — los modelos vectoriales (Recraft Vector) cobran más por imagen.

### Ejemplo concreto: 10 imágenes

| Modelo | Resolución estándar (1K) | Resolución alta (4K) |
|---|---|---|
| **GPT Image 2** | ~10 × $0.13 = **$1.30** (calidad alta) | más por resolución/calidad |
| **Nano Banana 2** | ~10 × $0.06 = **$0.60** | ~10 × $0.06 (fijo por token, varía poco) |
| **FLUX.2 Pro** (por MP) | ~10 × $0.03 ≈ **$0.30** (1MP c/u) | ~10 × $0.25 ≈ **$2.50** (8.3MP c/u) |
| **Qwen Image 3** | 10 × $0.03 = **$0.30** | no soporta 4K (máx 2K) |
| **Seedream 4.5** | 10 × $0.04 = **$0.40** | 10 × $0.04 = **$0.40** (fijo) |
| **Riverflow V2.5 Fast** | 10 × $0.019 = **$0.19** | no soporta 4K |
| **GPT Image 1 Mini** | ~10 × $0.008 = **$0.08** | — |

*Cifras aproximadas basadas en los precios oficiales por unidad. El costo real de los modelos "por token" depende de la resolución/calidad exacta que consuma la imagen.*

---

## 4. Comparación práctica y recomendaciones

### Tabla resumen (costo por imagen aprox., 1K)

| Modelo | Costo/imagen | Calidad | Velocidad | Mejor para |
|---|---|---|---|---|
| GPT Image 1 Mini | ~$0.008 | Media | Rápida | Prototipos, pruebas |
| Qwen Image 3 | $0.03 | Buena | Rápida | Generación económica |
| Nano Banana 2 | ~$0.06 | Alta | Rápida | **Mejor equilibrio general** |
| Seedream 4.5 | $0.04 | Alta | Media | Texto en imagen barato |
| FLUX.2 Pro | $0.03/MP | Alta | Media | Calidad por megapíxel flexible |
| GPT Image 2 | ~$0.13 | Excelente | Lenta (94s) | **Calidad máxima** |
| Nano Banana Pro | ~$0.12 | Excelente | Media | Calidad Pro + edición |
| FLUX.2 Max | $0.07/MP | Excelente | Media | Detalles finos |
| Recraft V4.1 Pro | $0.21 | Excelente | Media | Diseño/branding |

### Recomendación por caso de uso

- **Generación rápida y económica** → **GPT Image 1 Mini** (~$0.008) o **Qwen Image 3** ($0.03). Si necesitas mucho volumen, **Nano Banana 2 Lite** (~$0.03) o **Riverflow V2.5 Fast** ($0.019).
- **Calidad alta (una imagen que importa)** → **GPT Image 2** (~$0.13) o **Nano Banana Pro** (~$0.12). Para fotorealismo fino, **FLUX.2 Max**.
- **Edición de imágenes existentes** → **GPT Image 2 / GPT-5 Image** o **Nano Banana Pro** (mejor entendimiento de contexto). Si el precio importa, **Nano Banana 2** (~$0.06). Ojo: la edición cobra la imagen de entrada extra.
- **Texto dentro de la imagen (logos, carteles)** → **Seedream 4.5** ($0.04) o **Grok Imagine** ($0.05) — ambos fuertes en texto.
- **Diseño/ilustración/branding** → **Recraft** (especializado en diseño y vectores).
- **Vectorización** → **Recraft V4 Vector** ($0.08).

### Consejos para no pagar de más
1. Empieza con **1 imagen** y resolución **1K**; sube resolución/calidad solo si la necesitas.
2. Para iterar ideas, usa el modelo **mini/económico**; guarda el caro para la versión final.
3. En modelos **por megapíxel** (FLUX), la resolución multiplica el costo: no pidas 4K si no lo necesitas.
4. La **edición** cobra la imagen de entrada: reutiliza una sola referencia en vez de subir varias.
5. Verifica precios en vivo con `curl https://openrouter.ai/api/v1/images/models` — los precios cambian.

---

## Fuentes
- Catálogo de modelos de imágenes (API): `https://openrouter.ai/api/v1/images/models`
- Precios por modelo (API): `https://openrouter.ai/api/v1/images/models/<modelo>/endpoints`
- Documentación de la API de imágenes: `https://openrouter.ai/docs/guides/overview/multimodal/image-generation.md`
- Referencia de endpoints de imágenes: `https://openrouter.ai/docs/client-sdks/typescript/sdks/images/README.md`
- Página de modelos filtrada por salida de imagen: `https://openrouter.ai/models?output_modalities=image`

> **Honestidad sobre cobertura:** Los precios de **Krea 2** no están publicados en la API (los omití). Los precios de modelos "por token" (OpenAI/Google) son aproximaciones basadas en el cargo por token de imagen; el costo exacto depende de la resolución/calidad que consuma cada imagen. Todo lo demás proviene de datos oficiales consultados en vivo el 2026-08-09.
