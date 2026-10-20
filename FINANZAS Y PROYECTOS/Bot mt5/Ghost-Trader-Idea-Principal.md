# Ghost Trader — Idea Principal

> **Fecha:** 20/10/2026 · **Propósito:** Resumen canónico de la idea principal de Ghost Trader + investigación del "modelo JEV" y cómo integrarlo.

---

## 🧠 Idea Principal de Ghost Trader

**Qué es:** Un bot de trading algorítmico personal que opera **índices sintéticos de Deriv** (p.ej. `1RDN8Z3`) vía **WebSocket directo a la API de Deriv**, sin intermediarios ni MetaTrader.

**El problema que resuelve:** El trading algorítmico retail sigue amarrado a MetaTrader (servidores Windows, VPN, licencias caras, latencia). Los traders manuales pierden por ejecución tardía y emociones. Ghost Trader elimina eso.

**La solución:** Un solo proceso **Python 24/7 en VPS Ubuntu**, controlado por IA desde **Telegram** en lenguaje natural. Corre solo, sin ventanas.

### Arquitectura (v2 — Deriv API nativa, "Arquitectura Limpia")

Un solo proceso Python con pipeline por tick (latencia tick→orden ~60ms):

```
Deriv API → Deriv Connector (WebSocket JSON-RPC, auto-reconnect, backoff exp.)
        → Data Engine (Polars, buffer de ticks → velas → RSI/EMA/SMA/ATR/volatilidad)
        → Strategy Engine (reglas: EMA Crossover, RSI Reversal; O(1) por snapshot)
        → Risk Engine (filtro de seguridad SIEMPRE, sin bypass)
        → Deriv Connector (buy/sell)
        → Log + Notificación Telegram (via OpenClaw)
```

- **Data Engine:** cálculos vectorizados en Polars. Modos *batch* (500 velas históricas) y *streaming* (por tick).
- **Strategy Engine:** clases `Strategy` abstractas (EMACross, RSIStrategy) → `OrderSignal`.
- **Risk Engine:** único punto de aprobación (regla de oro). Reglas: límite pérdida diaria (-2%), máx posiciones (3), Stop Loss obligatorio, horario permitido (08:00–20:00 UTC), margen suficiente.
- **HTTP API local** en puerto 9001 (price, indicators, candles, order, positions, account) → consumida por OpenClaw.
- **Capa de interacción:** Skills HTTP + Telegram + TaskFlow → LLM (DeepSeek → OpenAI → Claude).
- **Modos:** Real-time, Backtest (métricas Sharpe, Sortino, Profit Factor, Max DD), Manual (Telegram).
- **Métricas y calidad:** CUENTA DEMO primero, real después con micro lots; tests 80%+; CI/CD.
- **Mapa de archivos:** `core/main.py`, `deriv_connector.py`, `data_engine.py`, `strategy_engine.py`, `risk_engine.py`, `backtester.py`, `models.py`, `tests/`, `openclaw/skills/`.

### Estado actual

- Proyecto **PAUSADO** según `mision.md` (prioridad actual: estudio DataCenter/DC; Ghost Trader como segundo bloque noche).
- Notas existentes: `Ghost-Trader-Elevator-Pitch.md`, `Ghost-Trader-EVOLUCION Construccion-v2.2.md`, `🌀 Ghost Trader — Flujo de Datos (Arquitectura Limpia).md`, `Ghost-Trader-Plan-Construccion-v2.2.md` (raíz del vault).

### Componentes

1. Conector Deriv (WebSocket)
2. Data Engine (Polars + indicadores)
3. Strategy Engine (estrategias modulares)
4. Risk Engine (seguridad)
5. HTTP API + OpenClaw (Telegram, TaskFlow, LLM)

---

## 🤖 Modelo JEV

**Qué es:** **Jev** es un **modelo de red neuronal ultra-rápida** creado por **TypeSafe AI** (distribución también vía OpenRouter "Alpha Decisions" / API Directa de TypeSafe). No es un LLM que genera texto lento: **analiza order book, gráficos y noticias en 70–300 ms** y devuelve una **respuesta matemática estricta: Buy / Sell / Hold** con **probabilidades y un score de confianza**.

**Cómo funciona:**
- Entrada: datos de mercado (precios, indicadores, fundamentales, order book, noticias/redes).
- Proceso: inferencia neuronal en ms → decisión estructurada (acción + probabilidades + notas de calidad de datos).
- Salida: `{ acción: buy|sell|hold, probabilidades[], confidence, evidencia }`.
- Se integra por API (cloud) o modelo local; mismo contrato.

### Interpretaciones plausibles encontradas

| Interpretación | Fuente | Encaja con Ghost Trader |
|---|---|---|
| **Jev = red neuronal TypeSafe AI** (Buy/Sell/Hold + confidence) — la interpretación dominante y consistente | GitHub `Jev-trading/Jev-trading`, jevdirectory.org | ✅ Muy bien: es exactamente un "modelo JEV" de trading para alimentar un Strategy Engine |
| **Jev-trading** (app desktop no-code) que envuelve a Jev | GitHub releases | Parcial: es la misma tecnología, pero no necesitamos su GUI |
| **Jev Trading** (servicio local TypeScript de señales de bolsa) | github.com/EthanAlgoX/jev-trading | ✅ Compatible: produce Buy/Sell/Hold + probabilidades vía API HTTP local |

**Nota:** dentro del vault, "JEV" solo aparece como `jev-router` (otra cosa, shadow mode de red) y en una nota de lectura sobre Gavrilo Princip (Sarajevo, no relacionado). No hay un "modelo JEV" ya anotado en el workspace.

---

## 🔧 Formas de incluir el modelo JEV en el funcionamiento

### 1. Estrategia JEV en el Strategy Engine (recomendada)
Añadir una clase `JEVStrategy(Strategy)` en `strategy_engine.py`. En lugar de reglas manuales, el snapshot de indicadores + datos de mercado se envía a Jev (API cloud/local); Jev devuelve `{buy/sell/hold, confidence}`. Filtrar por el umbral de confianza configurable (p.ej. `confidence >= 0.9`) y solo entonces emitir `OrderSignal`. Encaja 100% con la arquitectura limpia (tocas solo `strategy_engine.py`).

### 2. Jev como confirmador/checkpoint antes del Risk Engine
El Risk Engine sigue siendo el guardián final (regla de oro, sin bypass), pero añadir un paso intermedio "JEV confirmation": la señal de una estrategia clásica (ej. RSI) solo se aprueba si Jev coincide. Reduce falsas señales sin abandonar la seguridad.

### 3. Análisis de sentimiento de noticias (módulo Jev sentiment)
Usar Jev/jev.tg para parsear feeds RSS, Telegram y X (ej. "si X menciona DOGE y Jev evalúa sentimiento 4/5 → señal"). Reutilizable para operar índices sintéticos sensibles a eventos. Latencia < 1s.

### 4. Backtester con Jev
En modo Backtest, pasar velas históricas por Jev en vez de reglas deterministas, y comparar métricas (Winrate, P&L, Max DD, Profit Factor, Sharpe) de "JEV puro", "estrategias clásicas" y "híbrido". Validar antes de riesgo real.

### 5. Jev como señal independiente vía HTTP (superposición a otro módulo)
Levantar una instancia local (p.ej. `jev-trading` en `127.0.0.1:3000` o `jevtools` en localhost REST) y que Ghost Trader la consulte por HTTP para señal "Hold/No-trade" en modo manual o semi-manual, manteniendo Risk Engine siempre presente.

---

## 📚 Fuentes

**Archivos leídos (vault):**
- `FINANZAS Y PROYECTOS/Bot mt5/Ghost-Trader-Elevator-Pitch.md`
- `FINANZAS Y PROYECTOS/Bot mt5/🌀 Ghost Trader — Flujo de Datos (Arquitectura Limpia).md`
- `FINANZAS Y PROYECTOS/Bot mt5/Ghost-Trader-EVOLUCION Construccion-v2.2.md`
- `Ghost-Trader-Plan-Construccion-v2.2.md` (raíz)
- `mision.md` (estado: pausado, prioridad DC)

**URLs / web_search (modelo JEV):**
- https://github.com/Jev-trading/Jev-trading (app desktop no-code, red neuronal Jev de TypeSafe AI, Buy/Sell/Hold 70–300ms)
- https://www.jevdirectory.org/resources/jev-trading-jev-trading
- https://www.jevdirectory.org/resources/jev-trading (Jev Trading: servicio local TypeScript de señales Buy/Sell/Hold + probabilidades)
- https://github.com/EthanAlgoX/jev-trading (quickstart)
- https://www.jevdirectory.org/resources (directorio de recursos del modelo Jev; referencias a jevtools, kairos, jev.tg)

---
*Nota creada por subagente OpenClaw. Investigación de "modelo JEV" hecha en web (TypeSafe AI / OpenRouter). Verificación adicional sugerida antes de implementar: acceso a API Jev y documentación oficial TypeSafe.*
