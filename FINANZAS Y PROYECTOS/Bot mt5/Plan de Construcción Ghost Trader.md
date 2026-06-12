# 🏗️ Plan de Construcción — Ghost Trader

> **Versión:** 2.0 — 11/06/2026
> **Propósito:** Hoja de ruta para construir el asistente de trading en lenguaje natural, desglosado por módulos
> **Basado en:** Arquitectura v2 — Deriv API nativa

---

## 🧱 MÓDULOS DEL SISTEMA

```
┌─────────────────────────────────────────────────────────┐
│                 GHOST TRADER (1 proceso Python)          │
│                                                         │
│  ┌───────────────┐  ┌────────────┐  ┌───────────────┐  │
│  │    Deriv      │  │   Data     │  │   Backtest    │  │
│  │   Connector   │  │   Engine   │  │    Engine     │  │
│  │               │  │            │  │               │  │
│  │ WebSocket     │  │  Polars    │  │ Simulación    │  │
│  │ ↔ Deriv API   │  │  RSI, EMA  │  │ vela por vela │  │
│  │ Ticks vivos   │  │  SMA, ATR  │  │ Slippage, DD  │  │
│  └───────┬───────┘  └─────┬──────┘  └───────┬───────┘  │
│          │                │                  │          │
│          ▼                ▼                  ▼          │
│  ┌───────────────┐  ┌────────────┐  ┌───────────────┐  │
│  │   Strategy    │  │    Risk    │  │   HTTP API    │  │
│  │    Engine     │  │   Engine   │  │ (localhost)   │  │
│  │               │  │            │  │               │  │
│  │ EMACross, RSI │  │ Max loss   │  │ GET /price    │  │
│  │ Dynamic JSON  │  │ Max pos    │  │ POST /order   │  │
│  │ Evaluación    │  │ Horario    │  │ GET /account  │  │
│  └───────┬───────┘  └─────┬──────┘  └───────┬───────┘  │
│          │                │                  │          │
│          └────────────────┴──────────────────┘          │
│                           │                              │
│                           ▼                              │
│              ┌──────────────────────────┐                │
│              │   OPENC LAW (Capa Interacción)            │
│              │  Skills HTTP · Telegram · LLM · TaskFlow │
│              └──────────────────────────┘                │
└──────────────────────────────────────────────────────────┘
```

---

## 📦 Módulo 1 — Deriv Connector

**Función:** Puente único entre Deriv y el sistema. WebSocket persistente.

| Sub-componente | Estado | Prioridad |
|---------------|--------|-----------|
| Conexión WebSocket a Deriv Demo | ⏳ | 🔴 |
| Suscripción a ticks (1RDN8Z3) | ⏳ | 🔴 |
| Suscripción a balance/profit | ⏳ | 🔴 |
| Dataclasses internas (models.py) | ⏳ | 🔴 |
| Auto-reconnect (backoff exponencial) | ⏳ | 🟡 |
| Parseo de mensajes JSON-RPC | ⏳ | 🔴 |

**Dependencias:** `websockets`, `orjson`

---

## 📦 Módulo 2 — Data Engine

**Función:** Cálculos financieros con Polars. Corazón analítico.

| Sub-componente | Estado | Prioridad |
|---------------|--------|-----------|
| Buffer de ticks → agrupación por intervalo | ⏳ | 🔴 |
| RSI(14) — Wilder's Smoothing | ⏳ | 🔴 |
| EMA(12) — Exponential Moving Average | ⏳ | 🔴 |
| SMA(50) — Simple Moving Average | ⏳ | 🟡 |
| ATR(14) — Average True Range | ⏳ | 🟡 |
| Volatilidad (desviación estándar de retornos) | ⏳ | 🟡 |
| Modo batch (500 velas históricas) | ⏳ | 🟡 |
| Modo streaming (por tick) | ⏳ | 🔴 |

**Dependencias:** `polars`, `numpy`

---

## 📦 Módulo 3 — Backtest Engine

**Función:** Simulación vela por vela con datos reales Deriv.

| Sub-componente | Estado | Prioridad |
|---------------|--------|-----------|
| Obtener ticks_history de Deriv | ⏳ | 🔴 |
| Simulación vela por vela | ⏳ | 🔴 |
| Slippage + comisiones | ⏳ | 🟡 |
| Spread variable | ⏳ | 🟡 |
| Métricas: Sharpe, Sortino, Profit Factor, DD | ⏳ | 🟡 |

**Dependencias:** Módulo 2 (Data Engine)

---

## 📦 Módulo 4 — Strategy Engine

**Función:** Estrategias OOP. Evalúa reglas y genera señales.

| Sub-componente | Estado | Prioridad |
|---------------|--------|-----------|
| Clase abstracta Strategy | ⏳ | 🔴 |
| EMACross (EMA_12 cruza SMA_50) | ⏳ | 🔴 |
| RSIStrategy (RSI < 30 compra, > 70 vende) | ⏳ | 🟡 |
| Dynamic (reglas JSON configurables) | ⏳ | 🟡 |
| Evaluación O(1) por tick | ⏳ | 🔴 |

**Dependencias:** Módulo 2 (IndicatorSnapshot)

---

## 📦 Módulo 5 — Risk Engine

**Función:** Último filtro de seguridad. NO HAY BYPASS.

| Regla | Estado | Prioridad |
|-------|--------|-----------|
| Máx pérdida diaria (-2% del balance) | ⏳ | 🔴 |
| Máx posiciones abiertas (3) | ⏳ | 🔴 |
| Stop Loss obligatorio | ⏳ | 🔴 |
| Horario permitido (08:00-20:00 UTC) | ⏳ | 🟡 |
| Margen suficiente | ⏳ | 🔴 |
| Short-circuit (falla una → rechazada) | ⏳ | 🟡 |

**Regla de oro:** Risk Engine aplica a TODAS las órdenes — automáticas, manuales y por LLM.

---

## 📦 Módulo 6 — HTTP API (localhost:9001)

**Función:** Endpoints para que OpenClaw consuma.

| Endpoint | Estado | Prioridad |
|----------|--------|-----------|
| GET /price/{symbol} | ⏳ | 🔴 |
| GET /indicator/{name}/{symbol} | ⏳ | 🟡 |
| GET /candles/{symbol} | ⏳ | 🟡 |
| POST /order | ⏳ | 🔴 |
| POST /backtest | ⏳ | 🟡 |
| POST /strategy/{action} | ⏳ | 🟡 |
| GET /positions | ⏳ | 🟡 |
| GET /account | ⏳ | 🔴 |

**Dependencias:** Flask/FastAPI (liviano)

---

## 📦 Módulo 7 — OpenClaw (Capa de Interacción)

**Función:** Interface con usted vía Telegram + LLM.

| Sub-componente | Estado | Prioridad |
|---------------|--------|-----------|
| Skills HTTP thin (máx 15 líneas c/u) | ⏳ | 🟡 |
| Telegram → LLM interpreta → POST /order | ⏳ | 🔴 |
| TaskFlow (estrategias autónomas) | ⏳ | 🟡 |
| LLM intercambiable (DeepSeek → OpenAI → Claude) | ✅ | 🟢 |

---

## 🪜 ORDEN DE CONSTRUCCIÓN (Fases)

### Fase 1 — Fundación 🔴 (~2h)
Basado en el plan original de la arquitectura:

| Paso | Qué | Módulos | Tiempo |
|------|-----|---------|--------|
| 1 | Crear repo GitHub + estructura inicial | — | 15 min |
| 2 | Conexión WebSocket a Deriv Demo | M1 | 30 min |
| 3 | Tick en vivo + notificación por Telegram | M1 + M7 | 30 min |
| 4 | Data Engine básico + POST /order en demo | M2 + M6 | 1h |

**Checkpoint:** Usted ve un tick en Telegram y puede hacer una orden manual.

### Fase 2 — Núcleo Funcional 🟡 (~3h)

| Paso | Qué | Módulos | Tiempo |
|------|-----|---------|--------|
| 5 | Backtest Engine completo | M3 | 2h |
| 6 | Risk Engine operativo | M5 | 30 min |
| 7 | Strategy Engine funcional | M4 | 1h |

**Checkpoint:** Una estrategia completa ciclo cerrado (tick → indicador → evaluar → arriesgar → orden).

### Fase 3 — Integración y Optimización 🟢 (~2h)

| Paso | Qué | Módulos | Tiempo |
|------|-----|---------|--------|
| 8 | Refinamiento: logs, errores, tests | Todo | 1h |
| 9 | TaskFlow para estrategias autónomas | M7 | 30 min |
| 10 | Pruebas en mercado real (capital mínimo) | Todo | — |

**Checkpoint:** Ghost Trader ejecutando en vivo con supervisión.

---

## 📊 Estado General del Proyecto

| Módulo | Avance | Prioridad |
|--------|--------|-----------|
| M1 — Deriv Connector | 0% | 🔴 |
| M2 — Data Engine | 0% | 🔴 |
| M3 — Backtest Engine | 0% | 🟡 |
| M4 — Strategy Engine | 0% | 🔴 |
| M5 — Risk Engine | 0% | 🔴 |
| M6 — HTTP API | 0% | 🔴 |
| M7 — OpenClaw Layer | 10% | 🟡 |
| Arquitectura documentada | 100% | ✅ |
| Flujo de datos documentado | 100% | ✅ |
| Prácticas profesionales | 100% | ✅ |

---

## 📌 Tareas Inmediatas

- [ ] **⬆️ 🔴 HOY:** Backtest estrategia base con datos reales Deriv
- [ ] **⬆️ 🔴 HOY:** Definir parámetros de riesgo iniciales
- [ ] Crear repositorio GitHub + estructura
- [ ] Investigar N8N como alternativa de orquestación — *Evolución MT5.md*
- [ ] Ciclo de trabajo 🔁 — *Evolución MT5.md*

---

## 🔗 Notas Relacionadas

- [[Arquitectura Ghost Trader]]
- [[🌀 Ghost Trader — Flujo de Datos (Arquitectura Limpia)]]
- [[Evolución MT5]]
- [[Análisis assistentLLM]]
