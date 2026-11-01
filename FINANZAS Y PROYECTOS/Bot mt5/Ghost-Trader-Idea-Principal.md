---
created: 2026-10-20
updated: 2026-11-01
tags: [ghost-trader, trading, bot, moc]
estado: pausado
type: moc
---

# 🤖 Ghost Trader — Idea Principal (MOC)

> **MOC** — Mapa de conocimiento del proyecto Ghost Trader.

## 🔗 Enlaces rápidos

- [[Ghost-Trader-Elevator-Pitch]] — Pitch resumido
- [[Ghost-Trader-EVOLUCION Construccion-v2.2]] — Evolución del proyecto
- [[🌀 Ghost Trader — Flujo de Datos (Arquitectura Limpia)]] — Arquitectura v2
- [[Ghost-Trader-Plan-Construccion-v2.2]] — Plan de construcción (raíz vault)
- [[mision.md]] — Estado en 💰 PROYECTOS

## ✅ Siguiente acción

- [ ] Prototipo funcional (pausado — prioridad DataCenter)
- [ ] Retomar después de Fase 1 DC

---

**Fecha:** 20/10/2026 · **Propósito:** Resumen canónico de la idea principal de Ghost Trader + investigación del "modelo JEV".

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

---

## 🤖 Modelo JEV

**Qué es:** **Jev** es un **modelo de red neuronal ultra-rápida** creado por **TypeSafe AI** (distribución vía OpenRouter "Alpha Decisions" / API Directa de TypeSafe). No es un LLM que genera texto lento: **analiza order book, gráficos y noticias en 70–300 ms** y devuelve una **respuesta matemática estricta: Buy / Sell / Hold** con **probabilidades y un score de confianza**.

**Cómo funciona:**
- Entrada: datos de mercado (precios, indicadores, fundamentales, order book, noticias/redes).
- Proceso: inferencia neuronal en ms → decisión estructurada (acción + probabilidades + notas de calidad de datos).
- Salida: `{ acción: buy|sell|hold, probabilidades[], confidence, evidencia }`.
- Se integra por API (cloud) o modelo local; mismo contrato.

---

*Estado: pausado · Última edición: 2026-11-01*