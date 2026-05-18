# 🏗️ Arquitectura Ghost Trader

> **Versión:** 1.0 — 17/05/2026
> **Propósito:** Documentar la evolución arquitectónica del asistente de trading y definir el rumbo definitivo.

---

## 📜 Arquitectura Anterior (v1 — MT5-dependent)

### Contexto
El proyecto original (`assistentLLM-master`) se diseñó alrededor de MetaTrader 5 como fuente de datos y ejecución.

### Diagrama

```
┌── Windows ──────────────────────────────────────────┐
│  MetaTrader 5 Terminal                               │
│    ↓                                                    │
│  mt5-bridge-server.py (Flask + WebSocket)               │
│    ↓ VPN/Tailscale                                      │
├────────────────────────────────────────────────────────┤
│                    │
┌── Linux VPS ──────────────────────────────────────────┐
│  FastAPI Gateway (uvicorn)                             │
│    ↓                                                    │
│  Orchestrator (cerebro central)                         │
│    ├── LLM Service → Google Gemini                      │
│    ├── MT5 Bridge → HTTP → servidor Windows            │
│    ├── Trading Engine                                   │
│    ├── Strategy Engine                                  │
│    ├── State Manager (Redis / memoria)                  │
│    └── Tool Registry (15 tools)                        │
│                                                        │
│  OpenClaw (aparte)                                      │
│    └── Skills → wrappers HTTP                           │
└────────────────────────────────────────────────────── ───┘
```

### Problemas identificados

| Problema | Impacto |
|----------|---------|
| **Requiere Windows** | MT5 solo corre en Windows. El VPS no puede ejecutar nada sin un PC externo. |
| **Dependencia de VPN/Tailscale** | El bridge Windows → VPS necesita red privada. Punto de fallo adicional. |
| **Latencia** | Tick → MT5 → Bridge → VPS → DataEngine. Múltiples saltos. |
| **MT5 puede cerrarse** | Si se cierra la terminal o el PC se apaga, el sistema muere. |
| **Vendor lock-in MT5** | Cambiar de broker = reescribir el bridge completo. |
| **Orquestador monolítico** | 5 servicios Python con lógica duplicada. Frágil ante cambios. |
| **Gemini lock-in** | LLM hardcodeado a Google Generative AI. Sin alternativa. |
| **Backend de datos dual** | Datos simulados si MT5 no está conectado. Modo simulación poco realista. |

---

## 🆕 Arquitectura Nueva (v2 — Deriv API nativa)

### La revelación
Deriv API expone **datos brutos (ticks, velas) + ejecución (comprar, vender) + cuenta (balance, posiciones) TODO vía WebSocket desde cualquier servidor**. Sin necesidad de MT5.

### Diagrama

```
┌── Linux VPS (Hetnzer) ──────────────────────────────────┐
│                                                          │
│  ghost-trader-core (Python, service systemd)              │
│
│    ├── WebSocket → Deriv API (ticks en vivo 24/7)       │
│    ├── WebSocket → Deriv API (ejecución órdenes)        │
│    ├── WebSocket → Deriv API (cuenta + balance)         │
│    │                                                     │
│    ├── Data Engine (Polars, en memoria)                 │
│    │   └── RSI, EMA, SMA, ATR, correlaciones...         │
│    ├── Backtest Engine (datos históricos reales)         │
│    ├── Strategy Engine (estrategias autónomas)           │
│    ├── Risk Engine (reglas de operación)                 │
│    └── API HTTP localhost:9001                           │
│        ├── GET /price/{symbol}                           │
│        ├── GET /indicator/{name}/{symbol}                │
│        ├── GET /candles/{symbol}/{tf}                  │
│        ├── POST /order                                  │
│        ├── POST /backtest                               │
│        ├── POST /strategy/start                        │
│        ├── POST /strategy/stop                         │
│        ├── GET /positions                               │
│        └── GET /account                      │
│                                                          │
│  OpenClaw ─────────────────                              │
│    ├── Skills (wrappers HTTP de 10 líneas c/u)           │
│    │   ├── mt5-price → GET /price                        │
│    │   ├── mt5-rsi → GET /indicator/rsi                  │
│    │   ├── mt5-order → POST /order                      │
│    │   ├── mt5-backtest → POST /backtest                │
│    │   └── mt5-strategy → POST /strategy/*              │
│    ├── LLM (DeepSeek activo) OPENAI Claude Gemini        │
│    ├── TaskFlow (estrategias autónomas)            │
│    └── Telegram (Chat)─                        │
│                                                          │
│  (Opcional) MT5 en PC Windows solo para MONITOREO       │
│  └── ghost-trader-core publica estado → MT5 lo ve       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Lo que se elimina (vs v1)

| Componente eliminado | Razón |
|---------------------|-------|
| Servidor Windows + MT5 Bridge | Deriv API corre desde el VPS |
| Tailscale / VPN | Ya no hay comunicación Windows→VPS |
| FastAPI Gateway | OpenClaw maneja la interfaz |
| Orchestrator (500 líneas) | OpenClaw orquesta. Core solo es API. |
| State Manager (300 líneas) | Core maneja estado en memoria simple |
| LLM Service (100 líneas) | OpenClaw maneja providers LLM |
| Config Pydantic | Config en variables de entorno + openclaw.json |
| Dependencia Gemini | OpenClaw multi-provider |
| Modo simulación | Deriv da datos reales siempre |
| requirements.txt completo | Solo numpy, polars, pandas para el core |

### Lo que se conserva del proyecto original

| Lo que se conserva del proyecto original

| Componente | Nuevo rol |
|-----------|-----------|
| `data_engine.py` | Core → cálculo de indicadores |
| `analysis_tools.py` | Core → análisis dinámico |
| `backtester.py` | Core → simulación vela por vela (mejorado) |
| `strategy_engine.py` | Core → OOP strategies |
| `trading_engine.py` | Core → ejecución (adaptado a Deriv) |
| `risk_engine.py` | Core → NUEVO, reglas de operación |
| `app/tools/*.py` | Inspiración para skills OpenClaw |

---

## 📊 Comparativa v1 vs v2

| Aspecto | v1 (MT5) | v2 (Deriv) | Ganancia |
|---------|----------|------------|----------|
| **Plataforma** | Windows + Linux | Solo Linux | Sin dependencia externa |
| **Datos** | Librería MT5 nativa | WebSocket API | Más simple, multiplataforma |
| **Latencia** | VPN + bridge + MT5 → milisegundos | Directo VPS → Deriv | -80% latencia |
| **Disponibilidad** | Depende de PC encendido | 24/7 desde VPS | Siempre vivo |
| **Ejecución** | order_send() complejo | buy/sell API simple | Menos bugs |
| **Backtesting** | Simulado o con MT5 abierto | ticks_history real | Backtest legítimo |
| **LLM** | Solo Gemini | DeepSeek / OpenAI / Claude | Sin vendor lock-in |
| **Skills** | Toda la lógica en skills | Skills son wrappers thin | Actualizaciones OpenClaw no rompen nada |
| **Complejidad** | 15 archivos Python ~2000 líneas | 1 core + 6 skills thin | -70% código de infraestructura |

---

## 📐 Estructura de archivos (v2 propuesta)

```
ghost-trader/
├── core/
│   ├── main.py            ← Entry point, WebSocket Deriv, API HTTP
│   ├── deriv_connector.py ← Conexión WebSocket con Deriv
│   ├── data_engine.py     ← Cálculo de indicadores (Polars)
│   ├── backtester.py      ← Simulación vela por vela con datos reales
│   ├── strategy_engine.py ← Estrategias OOP (EMACross, Dynamic, etc.)
│   ├── risk_engine.py     ← Reglas de operación y seguridad
│   └── models.py          ← Schemas y tipos de datos
│
├── openclaw/
│   ├── skills/
│   │   ├── mt5-price.skill     → GET /price/{symbol}
│   │   ├── mt5-rsi.skill       → GET /indicator/rsi/{symbol}
│   │   ├── mt5-order.skill     → POST /order
│   │   ├── mt5-backtest.skill  → POST /backtest
│   │   └── mt5-strategy.skill  → POST /strategy/*
│   └── tasks/
│       └── strategy-monitor.task  → TaskFlow recurrente
│
├── requirements.txt        ← Solo numpy, polars, aiohttp, websockets (4-5)
├── .env                    ← DERIV_TOKEN, etc.)
└── README.md
```

---

## ⏭️ Próximos pasos

1. **Instalar dependencias** en el VPS (polars, websockets, etc.)
2. **Crear `deriv_connector.py`** → conectar WebSocket a Deriv API
3. **Tick en vivo desde Telegram** → primera prueba real
4. **POST /order → comprar en demo** → ejecución real en Deriv
5. **Backtesting con datos históricos reales**
6. **Estrategias autónomas vía TaskFlow**
7. **Risk Engine operativo**

---

*Actualizado: 17/05/2026 — Transición de arquitectura MT5 → Deriv API*
