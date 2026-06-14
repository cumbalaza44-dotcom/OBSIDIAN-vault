# 🏗️ Ghost Trader — Plan de Construcción

> **Fecha:** 13/06/2026
> **Estado:** Definición de alcance
> **Versión:** 2.0

---

## ⚠️ HALLAZGO CRÍTICO — Deriv API vs MT5

**La API de Deriv NO soporta trading tradicional (Forex CFD, Stop-Loss, Take-Profit).**

| Plataforma | Qué soporta | Trading |
|------------|-------------|---------|
| **Deriv API (WebSocket)** | Índices sintéticos, Opciones Digitales, Multipliers | Solo opciones binarias (Rise/Fall, Higher/Lower, Touch) |
| **MT5 API (Deriv)** | Gestión de cuenta (depósitos, retiros, passwords) | **NO soporta trading vía API** |
| **MT5 App (escritorio)** | Forex CFD, Índices, Commodities, Crypto | **Trading completo** (SL, TP, Pending Orders) |

### Implicaciones:

- **Para índices sintéticos** → Deriv API WebSocket directa ✅
- **Para Forex CFD** → Se necesita MT5 corriendo (app o bridge) ❌ la API no alcanza
- **Opción alternativa** → Usar Multipliers de Deriv (apalancamiento) vía API como sustituto de Forex CFD

### Preguntas pendientes con Mr. Jair:
1. ¿Qué es prioritario: Índices sintéticos (Deriv API) o Forex CFD (necesita MT5)?
2. ¿Está abierto a usar Multipliers de Deriv como alternativa a Forex CFD?
3. Si necesita Forex real, ¿quiere un bridge MT5 en el VPS?

---

## 📋 Resumen de Decisiones (Respuestas de Mr. Jair)

### 1. Símbolos
- **Prioritario:** Índices sintéticos (Volatility 75, Boom, Crash, etc.)
- **Secundario:** Forex (mayor frecuencia)
- **Baja frecuencia:** Crypto, energías, materias primas

### 2. Timeframes
- **Rango:** Tick → 4H velas
- **Alta frecuencia:** 1min - 1H (más usado)
- **Procesamiento configurable:** El usuario define periodos (10, 15, 20, 30+ velas)

### 3. Datos Históricos
- 1-2 años de histórico disponible
- Métrica principal: número de ejecuciones, no solo tiempo

### 4. Cuenta
- Inicialmente: **Demo**
- Futuro: Real ($2 USD capital, micro lots)

### 5. Indicadores
- Estándar MT5 (RSI, EMA, SMA, MACD, Bollinger, ATR, etc.)
- Configurables en periodos por el usuario
- Capacidad de identificar patrones de velas
- Análisis en lenguaje natural (OpenClaw maneja esto)

### 6. Backtesting
- Ejemplo: SMA 10 vs EMA 20 en velas de 1 minuto
- Contar cruces, identificar señales de compra/venta
- Resultados interpretados por el usuario
- Métricas: Sharpe, Sortino, Profit Factor, Max DD, Win Rate, Expectancy

### 7. Ejecución
- **Full-auto** por defecto (reglas definidas se ejecutan al pie de la letra)
- **Manual** cuando el usuario lo solicite
- **Alertas** que disparen el agente OpenClaw
- Múltiples estrategias en múltiples pares simultáneamente

### 8. Órdenes
- Todos los tipos básicos + control avanzado de posiciones
- Tipos disponibles según API/MT5

### 9. Risk Engine
- Límites configurables vía lenguaje natural (OpenClaw)
- Flotante, pérdidas, horarios — todo modificable
- Horarios de trading como requisito por estrategia
- Circuit breakers: detectar el eslabón débil

### 10. Interfaz
- **Telegram** (comandos + notificaciones)
- Posibilidad de dashboard web para datos en vivo (pendiente decidir)
- OpenClaw como capa de interacción principal

### 11. Infraestructura
- Mismo servidor que OpenClaw (Ubuntu VPS)
- 24/7 para mercados 24/7
- Auto-reconexión + safety norms en posiciones abiertas
- Monitoreo por componentes (arquitectura desacoplada)

### 12. Estrategias de Recovery
- Necesita ejemplos simples de recovery
- (Ver sección abajo)

---

## 🔄 Flujo de Construcción (6 Fases)

### FASE 1: Conexión & Datos (Semanas 1-2)
**Objetivo:** Obtener ticks en vivo y histórico de Deriv vía WebSocket

```
[Deriv WebSocket] → [Deriv Connector] → [Data Store (Polars)]
```

---

#### 📁 1.1 Scaffold del Proyecto

**Crear estructura de carpetas:**

```
ghost-trader/
├── ghost_trader/
│   ├── __init__.py          # Package marker
│   ├── config.py            # Configuración centralizada
│   ├── main.py              # Entry point
│   ├── connector/
│   │   ├── __init__.py
│   │   ├── deriv_ws.py      # Deriv WebSocket connector
│   │   └── models.py        # Data models (Tick, Candle, etc.)
│   ├── data/
│   │   ├── __init__.py
│   │   └── engine.py         # Data Engine (Polars)
│   └── utils/
│       ├── __init__.py
│       └── logging.py        # Logging configurado
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   └── __init__.py
│   └── conftest.py
├── config/
│   └── settings.toml         # Configuración por defecto
├── logs/                     # Directorio de logs
├── requirements.txt
├── pyproject.toml
└── README.md
```

**Reglas:**
- Cada archivo máximo 200 líneas
- Cada clase máxima responsabilidad (Single Responsibility)
- Sin hardcoding de valores — todo va en config/settings.toml
- Type hints en todas las funciones
- Docstrings en formato Google style

---

#### ⚙️ 1.2 Configuración Centralizada (config.py + settings.toml)

**Archivo `config/settings.toml`:**

```toml
[deriv]
app_id = 1089                    # ID de la aplicación Deriv (obtener de dashboard.deriv.com)
auth_token = ""                  # Token de autenticación (demo)
endpoint = "wss://ws.derivws.com/websockets/v3?app_id=1089"

[deriv.symbols]
# Símbolos por defecto para índices sintéticos
volatility_75 = "v75"
volatility_50 = "v50"
boom_1000 = "BOOM1000"
crash_1000 = "CRASH1000"

[data]
tick_buffer_size = 10000        # Ticks máximos en memoria
history_candles = 500           # Velas históricas a descargar
default_granularity = "1m"     # Granularidad por defecto

[heartbeat]
interval_seconds = 30           # Intervalo de ping/pong
reconnect_delay = 5             # Segundos entre reintentos
max_reconnect_attempts = 10     # Máximo de reintentos antes de fallar
```

**Archivo `ghost_trader/config.py`:**

```python
"""Configuración centralizada de Ghost Trader."""

from pathlib import Path
from dataclasses import dataclass
import tomllib


class DerivConfig:
    """Configuración de conexión a Deriv."""
    app_id: int
    auth_token: str
    endpoint: str
    symbols: dict[str, str]


class DataConfig:
    """Configuración del motor de datos."""
    tick_buffer_size: int
    history_candles: int
    default_granularity: str


class HeartbeatConfig:
    """Configuración de heartbeat y reconexión."""
    interval_seconds: int
    reconnect_delay: int
    max_reconnect_attempts: int


@dataclass
class Settings:
    """Settings maestro de Ghost Trader."""
    deriv: DerivConfig
    data: DataConfig
    heartbeat: HeartbeatConfig

    @classmethod
    def from_file(cls, path: str = "config/settings.toml") -> "Settings":
        """Carga configuración desde archivo TOML."""
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config no encontrado: {config_path}")
        with open(config_path, "rb") as f:
            raw = tomllib.load(f)
        return cls(
            deriv=DerivConfig(**raw["deriv"]),
            data=DataConfig(**raw["data"]),
            heartbeat=HeartbeatConfig(**raw["heartbeat"]),
        )
```

**Reglas:**
- Todo valor configurable DEBE estar en settings.toml
- Nunca hardcodear endpoints, tokens, símbolos en el código
- Si se necesita un valor nuevo → agregarlo primero a settings.toml

---

#### 🔌 1.3 Data Models (connector/models.py)

**Definir los modelos de datos que usará todo el sistema:**

```python
"""Modelos de datos para el conector Deriv."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class TickSource(Enum):
    """Fuente del tick."""
    LIVE = "live"
    HISTORY = "history"


@dataclass(frozen=True)
class Tick:
    """Tick individual de Deriv."""
    symbol: str
    price: float
    timestamp: int          # Unix timestamp en milisegundos
    source: TickSource

    @property
    def datetime(self) -> datetime:
        """Convierte timestamp a datetime."""
        return datetime.fromtimestamp(self.timestamp / 1000)


@dataclass(frozen=True)
class Candle:
    """Vela OHLC de Deriv."""
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    timestamp: int          # Unix timestamp en milisegundos
    granularity: str        # "1m", "5m", "1h", etc.

    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(self.timestamp / 1000)
```

**Reglas:**
- Modelos son `frozen=True` (inmutables) — un tick no cambia después de crearse
- Propiedades de conveniencia (datetime) en el modelo, no en el conector
- Enum para tipos fijos (TickSource)
- Sin dependencias externas en models.py (solo dataclasses, datetime, enum)

---

#### 🔌 1.4 Deriv WebSocket Connector (connector/deriv_ws.py)

**Clase principal:**

```python
"""Conector WebSocket para Deriv API."""

import asyncio
import json
import logging
from typing import Callable, Awaitable

import websockets
from websockets.exceptions import ConnectionClosed

from ghost_trader.config import Settings
from ghost_trader.connector.models import Tick, Candle, TickSource

logger = logging.getLogger(__name__)


class DerivConnector:
    """Conector WebSocket persistente a Deriv API."""

    def __init__(self, settings: Settings):
        self._settings = settings
        self._ws: websockets.WebSocketClientProtocol | None = None
        self._running = False
        self._request_id = 0
        self._callbacks: dict[int, Callable] = {}

    async def connect(self) -> None:
        """Establece conexión WebSocket con Deriv."""
        url = self._settings.deriv.endpoint
        logger.info(f"Conectando a {url}...")
        self._ws = await websockets.connect(url)
        self._running = True
        logger.info("Conexión establecida.")

    async def disconnect(self) -> None:
        """Cierra conexión WebSocket."""
        self._running = False
        if self._ws:
            await self._ws.close()
            logger.info("Conexión cerrada.")

    async def _send(self, payload: dict) -> int:
        """Envía request y retorna request_id."""
        self._request_id += 1
        payload["req_id"] = self._request_id
        await self._ws.send(json.dumps(payload))
        return self._request_id

    async def _receive_loop(self) -> None:
        """Loop principal de recepción de mensajes."""
        async for message in self._ws:
            data = json.loads(message)
            req_id = data.get("req_id")
            if req_id and req_id in self._callbacks:
                await self._callbacks[req_id](data)
                del self._callbacks[req_id]
            # Tick en vivo (sin req_id)
            elif "tick" in data:
                await self._on_tick(data)

    async def _on_tick(self, data: dict) -> None:
        """Procesa tick recibido."""
        tick_data = data["tick"]
        tick = Tick(
            symbol=tick_data["symbol"],
            price=float(tick_data["quote"]),
            timestamp=tick_data["epoch"] * 1000,
            source=TickSource.LIVE,
        )n        # Callback placeholder — se conecta en FASE 2
        logger.debug(f"Tick: {tick.symbol} = {tick.price}")

    async def subscribe_ticks(self, symbol: str) -> None:
        """Se suscribe a ticks en vivo de un símbolo."""
        await self._send({"ticks": symbol, "subscribe": 1})
        logger.info(f"Suscrito a ticks: {symbol}")

    async def get_history(
        self, symbol: str, granularity: str, count: int
    ) -> list[Candle]:
        """Obtiene histórico de velas."""
        req_id = await self._send({
            "ticks_history": symbol,
            "adjust_start_time": 1,
            "count": count,
            "granularity": granularity,
            "style": "candles",
        })
        # Esperar respuesta (simplificado — en producción usar事件驱动)
        # TODO: Implementar con asyncio.Event en FASE 1 paso 5
        return []

    async def run(self) -> None:
        """Loop principal del conector."""
        await self.connect()
        try:
            await self._receive_loop()
        except ConnectionClosed:
            logger.warning("Conexión perdida. Reconectando...")
            await self._reconnect()
        finally:
            await self.disconnect()

    async def _reconnect(self) -> None:
        """Maneja reconexión automática."""
        attempts = 0
        while attempts < self._settings.heartbeat.max_reconnect_attempts:
            attempts += 1
            delay = self._settings.heartbeat.reconnect_delay
            logger.info(f"Reintento {attempts}/{self._settings.heartbeat.max_reconnect_attempts} en {delay}s...")
            await asyncio.sleep(delay)
            try:
                await self.connect()
                return
            except Exception as e:
                logger.error(f"Reintento falló: {e}")
        logger.error("Máximo de reintentos alcanzado.")
```

**Reglas del conector:**
- El conector SOLO conecta y obtiene datos — NO ejecuta órdenes (eso es FASE 4)
- Callbacks flexibles — se conectan después, no están hardcodeados
- Reconexión automática con límite de intentos
- Logging en cada evento importante (connect, disconnect, tick, error)
- Todo asíncrono (async/await) — nunca bloquear el event loop

---

#### 📦 1.5 Data Engine (data/engine.py)

**Motor de almacenamiento con Polars:**

```python
"""Motor de datos — almacenamiento y gestión con Polars."""

import polars as pl
from ghost_trader.connector.models import Tick, Candle
from ghost_trader.config import Settings


class DataEngine:
    """Almacena y gestiona datos de mercado."""

    def __init__(self, settings: Settings):
        self._max_ticks = settings.data.tick_buffer_size
        self._tick_buffer: list[Tick] = []
        self._candles: dict[str, pl.DataFrame] = {}  # symbol → DataFrame

    def add_tick(self, tick: Tick) -> None:
        """Agrega un tick al buffer."""
        self._tick_buffer.append(tick)
        if len(self._tick_buffer) > self._max_ticks:
            self._tick_buffer = self._tick_buffer[-self._max_ticks:]

    def ticks_to_dataframe(self, symbol: str | None = None) -> pl.DataFrame:
        """Convierte ticks a DataFrame de Polars."""
        if not self._tick_buffer:
            return pl.DataFrame()
        ticks = self._tick_buffer
        if symbol:
            ticks = [t for t in ticks if t.symbol == symbol]
        return pl.DataFrame({
            "symbol": [t.symbol for t in ticks],
            "price": [t.price for t in ticks],
            "timestamp": [t.timestamp for t in ticks],
        })

    def add_candles(self, symbol: str, candles: list[Candle]) -> None:
        """Almacena velas para un símbolo."""
        if not candles:
            return
        df = pl.DataFrame({
            "open": [c.open for c in candles],
            "high": [c.high for c in candles],
            "low": [c.low for c in candles],
            "close": [c.close for c in candles],
            "volume": [c.volume for c in candles],
            "timestamp": [c.timestamp for c in candles],
        })
        self._candles[symbol] = df

    def get_candles(self, symbol: str) -> pl.DataFrame:
        """Retorna velas de un símbolo."""
        return self._candles.get(symbol, pl.DataFrame())
```

**Reglas del Data Engine:**
- Buffer circular de ticks (no crece infinitamente)
- Un DataFrame por símbolo (no mezclar)
- Conversión a Polars para cálculos vectorizados (ultra rápido)
- Sin lógica de indicadores aquí — solo almacenamiento

---

#### 🧪 1.6 Tests de la FASE 1

**Tests unitarios mínimos:**

```python
# tests/unit/test_models.py
from ghost_trader.connector.models import Tick, Candle, TickSource

def test_tick_creation():
    tick = Tick(symbol="v75", price=1234.56, timestamp=1718316000000, source=TickSource.LIVE)
    assert tick.symbol == "v75"
    assert tick.price == 1234.56
    assert tick.source == TickSource.LIVE

def test_tick_is_frozen():
    tick = Tick(symbol="v75", price=1.0, timestamp=0, source=TickSource.LIVE)
    try:
        tick.price = 2.0
        assert False, "Debería ser inmutable"
    except AttributeError:
        pass

# tests/unit/test_data_engine.py
from ghost_trader.data.engine import DataEngine
from ghost_trader.config import Settings

def test_data_engine_buffer_limit():
    settings = Settings.from_file()
    engine = DataEngine(settings)
    # Agregar más ticks que el límite
    for i in range(settings.data.tick_buffer_size + 100):
        engine.add_tick(Tick(symbol="v75", price=float(i), timestamp=i, source=TickSource.LIVE))
    df = engine.ticks_to_dataframe()
    assert len(df) == settings.data.tick_buffer_size
```

**Reglas de testing:**
- Cada modelo tiene al menos 1 test
- DataEngine tiene test de buffer límite
- Tests corren sin red (unitarios puros)
- `pytest tests/unit/ -v` debe pasar al 100%

---

#### 📋 1.7 Checklist de Aprobación FASE 1

Antes de pasar a FASE 2, verificar:

- [ ] Estructura de carpetas creada correctamente
- [ ] `config/settings.toml` con todos los valores configurables
- [ ] `config.py` carga configuración desde TOML
- [ ] `models.py` con Tick y Candle (frozen, type hints)
- [ ] `deriv_ws.py` conecta a Deriv, suscribe ticks, reconecta
- [ ] `data/engine.py` almacena ticks y velas en Polars
- [ ] Todos los tests pasan (`pytest tests/ -v`)
- [ ] Sin hardcoding — todo configurable desde settings.toml
- [ ] Logging configurado (DEBUG en dev, INFO en prod)
- [ ] README.md con instrucciones de instalación y uso

**Si algún punto falla → NO avanzar a FASE 2.**

---

**Entregable FASE 1:**
- Script que conecta a Deriv, obtiene ticks en vivo y los almacena en Polars
- Tests pasando al 100%
- Configuración centralizada y documentada

### FASE 2: Data Engine — Indicadores (Semanas 3-4)
**Objetivo:** Calcular indicadores en tiempo real

```
[Data Store] → [Indicator Engine] → [Signals]
```

- [ ] Indicadores core: RSI, EMA, SMA, MACD, Bollinger, ATR
- [ ] Modo batch (histórico) + streaming (ticks vivos)
- [ ] Configuración de periodos por usuario
- [ ] Patrones de velas (doji, hammer, engulfing, etc.)
- [ ] API de indicadores (endpoint para consultar valores)

**Entregable:** Motor de indicadores que procesa datos en vivo y retorna valores.

### FASE 3: Strategy Engine & Backtesting (Semanas 5-6)
**Objetivo:** Definir, probar y validar estrategias

```
[Signals] → [Strategy Engine] → [Trade Proposals]
[Historical Data] → [Backtest Engine] → [Metrics]
```

- [ ] Framework OOP para estrategias (clase abstracta Strategy)
- [ ] Estrategia piloto: SMA/EMA crossover
- [ ] Backtest engine: simulación vela por vela
- [ ] Métricas: Sharpe, Sortino, Profit Factor, Max DD, Win Rate
- [ ] Exportación de resultados (JSON/CSV)
- [ ] Validación: mínimo N trades, período mínimo

**Entregable:** Estrategia piloto + backtesting con métricas.

### FASE 4: Risk Engine & Execution (Semanas 7-8)
**Objetivo:** Ejecutar órdenes de forma segura

```
[Trade Proposals] → [Risk Engine] → [Order Executor] → [Deriv API]
```

- [ ] Reglas de risk: max loss, max positions, require SL
- [ ] Position sizing: fixed lot / % balance / micro lots
- [ ] Order executor: buy, sell, cancel, update
- [ ] Circuit breakers: detección de anomalías
- [ ] Safety norms para posiciones abiertas
- [ ] Logging de todas las ejecuciones

**Entregable:** Sistema completo de ejecución con risk management.

### FASE 5: Interfaz & OpenClaw Integration (Semanas 9-10)
**Objetivo:** Control vía Telegram + notificaciones

```
[User Telegram] → [OpenClaw] → [Ghost Trader API] → [Core]
[Ghost Trader] → [OpenClaw] → [User Telegram]
```

- [ ] HTTP API (localhost:9001) para OpenClaw
- [ ] Endpoints: /price, /indicator, /candles, /order, /backtest, /strategy
- [ ] Skills HTTP thin (máx 15 líneas c/u)
- [ ] Notificaciones: cada trade, alertas, resumen diario
- [ ] Control: start/stop estrategias, listar posiciones
- [ ] Lenguaje natural: "¿Cuántas veces se cruzan SMA 10 y EMA 20?"

**Entregable:** Sistema controlable vía Telegram con notificaciones.

### FASE 6: Optimización & Production (Semanas 11-12)
**Objetivo:** Hardening, tests, despliegue

- [ ] Tests unitarios + integración (80% coverage)
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Ruff + Mypy + Pytest
- [ ] Documentación completa
- [ ] Monitoreo: logs, health checks, alerts
- [ ] Paper trading period
- [ ] Despliegue production (systemd service)

**Entregable:** Sistema productivo, testead, documentado.

---

## 📊 Estrategias de Recovery (Ejemplos Simples)

### Recovery 1: Martingala Ligera
```
Si pérdida → siguiente trade = 1.5x posición anterior
Si ganancia → volver a posición base
Límite: máximo 3 martingalas consecutivas
```

### Recovery 2: Recovery por Porcentaje
```
Si drawdown > 5% → reducir tamaño posición 50%
Si drawdown > 10% → pausar estrategia, alertar usuario
Si recovery a < 3% → restaurar posición normal
```

### Recovery 3: Grid Recovery
```
Al abrir posición perdedora → abrir posiciones en niveles
Cada 20 pips hacia abajo → nueva posición (tamaño decreciente)
Take-profit colectivo que cubra todas las posiciones
Límite: máximo 5 niveles de grid
```

### Recovery 4: Hedge Temporal
```
Si posición va en contra > 30 pips → abrir hedge opuesto
Cuando mercado se estabiliza → cerrar hedge + posición original
Loss minimized vs dejar correr
```

---

## 🛠️ Stack Técnico

| Componente | Tecnología |
|------------|------------|
| Lenguaje | Python 3.11+ |
| WebSocket | websockets / aiohttp |
| Datos | Polars (DataFrames) |
| API HTTP | FastAPI |
| Base de datos | SQLite (state) + Polars (data) |
| Testing | Pytest + coverage |
| Linting | Ruff + Mypy |
| Deployment | systemd (Ubuntu VPS) |
| Comunicación | OpenClaw Telegram |

---

## 📁 Estructura del Proyecto

```
ghost-trader/
├── ghost_trader/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── config.py             # Settings
│   ├── connector/
│   │   ├── __init__.py
│   │   ├── deriv_ws.py      # Deriv WebSocket connector
│   │   └── models.py        # Data models
│   ├── data/
│   │   ├── __init__.py
│   │   ├── engine.py         # Data Engine (Polars)
│   │   └── indicators.py     # Indicator calculations
│   ├── strategy/
│   │   ├── __init__.py
│   │   ├── base.py           # Abstract Strategy class
│   │   ├── ema_cross.py      # EMA Crossover
│   │   └── registry.py       # Strategy registry
│   ├── backtest/
│   │   ├── __init__.py
│   │   └── engine.py         # Backtest engine
│   ├── risk/
│   │   ├── __init__.py
│   │   └── engine.py         # Risk Engine
│   ├── execution/
│   │   ├── __init__.py
│   │   └── executor.py       # Order executor
│   └── api/
│       ├── __init__.py
│       └── server.py         # FastAPI HTTP server
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── docs/
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## ❓ Preguntas Pendientes para Mr. Jair

1. **Deriv API vs MT5:** ¿Qué es prioritario? ¿Índices sintéticos (Deriv API directa) o Forex CFD (necesita MT5 bridge)?
2. **Multipliers:** ¿Está abierto a usar Multipliers de Deriv como alternativa a Forex CFD?
3. **Capital:** $2 USD confirmado como capital inicial?
4. **Timeline:** ¿12 semanas es aceptable para MVP funcional?
5. **Dashboard web:** ¿Lo necesitamos en la FASE 5 o lo dejamos para después?
6. **Estrategia piloto:** ¿SMA/EMA crossover es aceptable como primera estrategia?
7. **Recovery:** ¿Cuál de las 4 estrategias de recovery prefiere para empezar?

---

## 📌 PUNTO DE CONTROL — Broker Alternativo (13/06/2026)

> **Estado:** Referencia futura. No está en el alcance actual.
> **Prioridad:** Baja — Resolver cuando Ghost Trader esté funcional.

### Situación actual
- **Broker primario:** Deriv (API WebSocket)
- **Mercados:** Índices sintéticos + Multipliers
- **Limitación:** No soporta Forex CFD tradicional vía API

### Opción futura: OANDA
- **API REST v20** — Sin dependencia de MT5
- **Mínimo $1** — Escalable con capital pequeño
- **Forex real** — EUR/USD, GBP/JPY, etc. con spreads bajos
- **Python:** `oandapyV20` (librería oficial)
- **Regulado:** FCA, ASIC, CFTC

### Cuándo considerar este cambio
1. Cuando Ghost Trader esté funcional con Deriv
2. Cuando se necesite operar Forex CFD real (no Multipliers)
3. Cuando el capital lo permita ($10+ mínimo recomendado para OANDA)
4. Cuando se quiera diversificar mercados más allá de índices sintéticos

### Arquitectura preparada para el cambio
El core de Ghost Trader ya está diseñado de forma desacoplada:
- `connector/deriv_ws.py` → Conector Deriv
- `connector/oanda_rest.py` → (Futuro) Conector OANDA
- `data/engine.py` → Acepta datos de múltiples fuentes
- `execution/executor.py` → Ejecuta vía el conector correcto

El cambio de broker sería agregar un conector nuevo, no reescribir el core.

### Nota personal
"Cambiar de broker es algo poco previsto aún, pero es importante tenerlo documentado para cuando llegue el momento."
— Mr. Jair, 13/06/2026
