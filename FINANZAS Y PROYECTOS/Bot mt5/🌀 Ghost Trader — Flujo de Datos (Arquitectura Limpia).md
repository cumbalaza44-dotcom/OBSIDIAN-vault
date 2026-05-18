# 🌀 Ghost Trader — Flujo de Datos (Arquitectura Limpia)

> **Propósito:** Entender el sistema completo desde que entra un tick hasta que se ejecuta una orden. Sin ruido técnico de gestión de proyecto.
> **Basado en:** Arquitectura Ghost Trader v2 — Deriv API nativa

---

## 📡 1. CAPA DE ENTRADA — Deriv Connector

**Función:** Puente único entre el mundo real (Deriv) y el sistema.

```
┌─────────────────────────────────────────────────────────┐
│                    DERIV (ws.derivws.com)                │
│      WebSocket persistente — SSL — Puerto 443           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              DERIV CONNECTOR (WebSocket Client)          │
│                                                         │
│  ● Conexión única, permanente (auto-reconnect)          │
│  ● Envía mensajes JSON-RPC hacia Deriv                  │
│  ● Recibe streams de ticks, OHLC, trades, balance       │
│  ● Normaliza TODA respuesta a dataclasses internas      │
│                                                         │
│  Suscripciones activas por defecto:                     │
│  ├── ticks        → 1RDN8Z3... (índices sintéticos)     │
│  ├── balance      → cada vez que cambia                 │
│  ├── profit_table → cada trade cerrado                  │
│  └── proposal     → precio actual de símbolo            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
            Dataclasses internas (models.py)
```

### Flujo de conexión paso a paso:

```
Paso 1: Crear WebSocket a wss://ws.derivws.com/websockets/v3
Paso 2: Enviar authorize { "ticks": "1RDN8Z3" }
Paso 3: Enviar subscribe { "ticks": "1RDN8Z3" }
Paso 4: Escuchar → cada mensaje entrante se parsea a un dataclass
Paso 5: Si se cae → esperar 1s, 2s, 4s, 8s (backoff exponencial) → reconectar
Paso 6: Reconexión → reautorizar → resuscribir → continuar
```

**Salida del connector:** Eventos tipados (`Tick`, `Candle`, `OrderUpdate`, `BalanceUpdate`) que el resto del sistema consume.

---

## 🔄 2. FLUJO NORMAL — Tick → Estrategia → Decisión

Este es el camino que recorre CADA tick que entra al sistema:

```
                  ┌──────────────┐
                  │   DERIV API   │
                  └──────┬───────┘
                         │ tick{ bid: 1.0834, ask: 1.0836 }
                         ▼
            ┌─────────────────────────┐
            │    DERIV CONNECTOR       │
            │  (WebSocket → TickEvent) │
            └──────────┬──────────────┘
                       │ TickEvent(symbol="frxEURUSD", bid=1.0834, ask=1.0836, time=...)
                       ▼
            ┌─────────────────────────┐
            │     DATA ENGINE          │
            │  (Polars — cálculos puros) │
            │                           │
            │  1. Acumula tick en buffer│
            │  2. Si completa vela →     │
            │     recalcula indicadores: │
            │    ├── RSI(14)             │
            │    ├── EMA(12) / SMA / ATR │
            │    ├── Volatilidad         │
            │    └── Correlaciones       │
            └──────────┬──────────────┘
                       │ Snapshot: { rsi: 62.3, ema_12: 1.0821, ... }
                       ▼
            ┌─────────────────────────┐
            │   STRATEGY ENGINE        │
            │  (Evalúa reglas)         │
            │                           │
            │  Estrategia activa:       │
            │  "Compra si RSI < 30 y    │
            │   precio > EMA(12)"       │
            │                           │
            │  ¿Se cumple?             │
            │  ├── NO → descartar tick │
            │  └── SÍ → señal de orden │
            └──────────┬──────────────┘
                       │ OrderSignal(symbol, direction, volume, reason)
                       ▼
            ┌─────────────────────────┐
            │     RISK ENGINE          │
            │  (Último filtro — SEGURIDAD) │
            │                           │
            │  Reglas evaluadas:        │
            │  ├── ¿Pérdida diaria      │
            │  │   supera el límite?    │
            │  ├── ¿Máx posiciones      │
            │  │   alcanzado?           │
            │  ├── ¿Stop Loss definido? │
            │  ├── ¿Hora permitida?     │
            │  └── ¿Margen suficiente?  │
            │                           │
            │  ¿Todo OK?               │
            │  ├── NO → rechazar + log  │
            │  └── SÍ → aprobar orden   │
            └──────────┬──────────────┘
                       │ ApprovedOrderSignal(...)
                       ▼
            ┌─────────────────────────┐
            │    DERIV CONNECTOR       │
            │  (buy/sell → Deriv API)  │
            │                           │
            │  Envía: buy{             │
            │    symbol: "frxEURUSD",   │
            │    amount: 10,           │
            │    type: "market"        │
            │  }                       │
            └──────────┬──────────────┘
                       │ order_confirmation
                       ▼
            ┌─────────────────────────┐
            │      LOG + NOTIFICAR     │
            │  └── Telegram (OpenClaw) │
            └──────────────────────────┘
```

### Resumen del pipeline de datos (por tick):

| Etapa               | Entrada               | Procesamiento         | Salida                          | Costo temporal |
| ------------------- | --------------------- | --------------------- | ------------------------------- | -------------- |
| **Connector**       | JSON de Deriv         | Parseo + validación   | `TickEvent`                     | < 1ms          |
| **Data Engine**     | `TickEvent`           | Polars batch calc     | `IndicatorSnapshot`             | ~5ms           |
| **Strategy**        | `IndicatorSnapshot`   | Evaluación de reglas  | `OrderSignal` o nada            | < 1ms          |
| **Risk Engine**     | `OrderSignal`         | 5 reglas de seguridad | `ApprovedOrderSignal` o rechazo | < 1ms          |
| **Connector (out)** | `ApprovedOrderSignal` | JSON-RPC a Deriv      | Confirmation                    | ~50ms (red)    |

**Total latencia tick → orden:** ~60ms en condiciones normales.

---

## 🏛️ 3. ARQUITECTURA DE PROCESO — Vista General

```
┌──────────────────────────────────────────────────────────────┐
│                  ghost-trader (1 proceso Python)              │
│                                                              │
│  ┌────────────┐  ┌──────────┐  ┌────────────┐  ┌─────────┐  │
│  │   Deriv    │  │   Data   │  │  Strategy  │  │  Risk   │  │
│  │ Connector  │  │  Engine  │  │   Engine   │  │ Engine  │  │
│  │            │  │          │  │            │  │         │  │
│  │ WebSocket  │  │  Polars  │  │  Evalúa    │  │ Filtro  │  │
│  │ ↔ Deriv    │  │  calc    │  │  reglas    │  │ de      │  │
│  │            │  │  pd/NN   │  │  de compra │  │ seguri  │  │
│  └─────┬──────┘  └────┬─────┘  └──────┬─────┘  └────┬────┘  │
│        │              │               │             │       │
│        └──────────────┴───────────────┴─────────────┘       │
│                              │                               │
│                              ▼                               │
│              ┌──────────────────────────┐                    │
│              │   HTTP API (localhost)   │                    │
│              │   Puerto 9001            │                    │
│              │                          │                    │
│              │  Endpoints:              │                    │
│              │  GET  /price/{symbol}    │                    │
│              │  GET  /indicator/{name}  │                    │
│              │  GET  /candles/{symbol}  │                    │
│              │  POST /order             │                    │
│              │  GET  /positions         │                    │
│              │  GET  /account           │                    │
│              └──────────┬───────────────┘                    │
└─────────────────────────┼────────────────────────────────────┘
                          │ localhost:9001
                          ▼
┌──────────────────────────────────────────────────────────────┐
│                  OPENC LAW (Capa de interacción)               │
│                                                              │
│  ┌──────────────┐  ┌──────────┐  ┌──────────────────────┐   │
│  │ Skills HTTP  │  │ Telegram │  │ TaskFlow             │   │
│  │ (thin)       │  │ (Usted)  │  │ (Estrategias         │   │
│  │              │  │          │  │  autónomas)          │   │
│  └──────┬───────┘  └────┬─────┘  └──────────┬───────────┘   │
│         │               │                   │               │
│         └───────────────┴───────────────────┘               │
│                           │                                  │
│                           ▼                                  │
│                    ┌──────────────┐                          │
│                    │  LLM        │                          │
│                    │  DeepSeek    │                          │
│                    │  → OpenAI    │                          │
│                    │  → Claude    │                          │
│                    └──────────────┘                          │
└──────────────────────────────────────────────────────────────┘
```

---

## 🧱 4. MÓDULOS INTERNOS — Responsabilidades Clave

### 4.1 models.py — El Contrato

Todas las estructuras que cruzan los límites entre módulos:

```python
@dataclass
class Tick:
    symbol: str
    bid: float
    ask: float
    time: datetime

@dataclass
class Candle:
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    time: datetime

@dataclass
class IndicatorSnapshot:
    symbol: str
    rsi: float | None
    ema_12: float | None
    sma_50: float | None
    atr: float | None
    volatility: float | None

@dataclass
class OrderSignal:
    symbol: str
    direction: Literal["buy", "sell"]
    volume: float
    reason: str
    strategy: str

@dataclass
class ApprovedOrder:
    signal: OrderSignal
    risk_check_id: str
    approved_at: datetime
```

### 4.2 Data Engine — Corazón Analítico

```
Buffer de ticks → Agrupación por intervalo (1m, 5m) → Candle →
    ├── RSI(14): Wilder's Smoothing
    ├── EMA(12): Exponential Moving Average
    ├── SMA(50): Simple Moving Average
    ├── ATR(14): Average True Range
    └── Volatilidad: Desviación estándar de retornos
```

Opera en **dos modos**:
- **Batch:** Al cargar, procesa 500 velas históricas (Polars vectorizado)
- **Streaming:** Por cada tick, actualiza la vela en curso y solo el indicador necesario

### 4.3 Strategy Engine — Cerebro

```python
class Strategy(ABC):
    """Toda estrategia hereda de aquí."""
    
    @abstractmethod
    def evaluate(self, snapshot: IndicatorSnapshot) -> OrderSignal | None:
        """Recibe indicadores, devuelve señal o nada."""
        pass

class EMACross(Strategy):
    """Compra cuando EMA_12 cruza arriba de SMA_50."""
    
    def evaluate(self, snapshot):
        if snapshot.ema_12 > snapshot.sma_50 and prev_ema <= prev_sma:
            return OrderSignal(buy, reason="EMA crossover")
        return None

class RSIStrategy(Strategy):
    """Compra si RSI < 30, vende si RSI > 70."""
    ...
```

**Evaluación por tick:** O(1) — solo mira el snapshot actual vs el anterior.

### 4.4 Risk Engine — Guardián

Reglas evaluadas en cadena (short-circuit: falla una, se rechaza):

```
1. Límite de pérdida diaria       → max_daily_loss = -2% del balance
2. Máximo de posiciones abiertas   → max_positions = 3
3. Stop Loss obligatorio           → toda orden requiere SL
4. Horario permitido               → solo entre 08:00 - 20:00 UTC
5. Margen suficiente               → balance - margen > 0
```

---

## 📊 5. MODOS DE OPERACIÓN

### Modo Real-time (default)
```
Tick → Connector → DataEngine → StrategyEngine → RiskEngine → Orden
                              ↕
                    HTTP API (lectura para OpenClaw)
```

### Modo Backtest
```
CSV/API histórica → DataEngine (batch) → StrategyEngine → 
  → Simulación de órdenes con slippage → Métricas
```

### Modo Manual (usted via Telegram)
```
Telegram → OpenClaw → LLM interpreta → POST /order → RiskEngine → Deriv
```

---

## 🔐 6. SEGURIDAD — No se salta ni una

```
                  ┌─────────────────────┐
                  │  TELEGRAM (Usted)    │
                  └─────────┬───────────┘
                            │ "compra 10 EURUSD"
                            ▼
                  ┌─────────────────────┐
                  │   LLM interpreta     │
                  └─────────┬───────────┘
                            │ OrderSignal
                            ▼
                  ┌─────────────────────┐
                  │    RISK ENGINE       │ ← NO HAY BYPASS
                  │  (mismas reglas)    │
                  └─────────┬───────────┘
                            │
                    ┌───────┴───────┐
                    │               │
                    ▼               ▼
                  Aprobada      Rechazada
                    │               │
                    ▼               ▼
                 Deriv API    Log + "No puedo, 
                              señor. Razón: ..."
```

**Principio:** Risk Engine es el único punto de aprobación de órdenes. Ni el LLM, ni usted, ni una estrategia automática pueden saltárselo.

---

## ⚙️ 7. MAPA DE ARCHIVOS (para estudio)

```
ghost-trader/
│
├── core/                     # ✅ Código que importa
│   ├── main.py               # Entry point — conecta todo
│   ├── deriv_connector.py    # WebSocket con Deriv
│   ├── data_engine.py        # Indicadores en Polars
│   ├── strategy_engine.py    # Evaluación de estrategias
│   ├── risk_engine.py        # Seguridad y validación
│   ├── backtester.py         # Simulación histórica
│   └── models.py             # Dataclasses (el idioma común)
│
├── tests/                    # 🧪 Calidad garantizada
│   ├── unit/                 # Tests rápidos, sin red
│   ├── integration/          # Tests con Deriv demo real
│   └── conftest.py           # Fixtures compartidos
│
├── openclaw/skills/          # 🔌 Wrappers HTTP para OpenClaw
│
└── pyproject.toml            # Configuración del proyecto
```

**Orden de lectura recomendado:**
1. `models.py` — el lenguaje del sistema
2. `deriv_connector.py` — cómo entra la data
3. `data_engine.py` — cómo se transforma
4. `strategy_engine.py` — cómo se decide
5. `risk_engine.py` — cómo se protege
6. `main.py` — cómo se ensambla

---

## 🧠 8. REGLA DE ORO

> **Cada módulo hace UNA cosa y solo UNA.**
> 
> Si mañana cambias de broker, tocas solo `deriv_connector.py`.
> Si cambias de estrategia, tocas solo `strategy_engine.py`.
> Si quieres más seguridad, tocas solo `risk_engine.py`.
> 
> **El sistema es como un reloj suizo:** engranajes independientes que encajan perfectamente.

---

*Basado en la arquitectura v2 — Deriv API nativa — 18/05/2026*
