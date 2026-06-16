# 🏗️ Ghost Trader — Plan de Construcción

> **Fecha:** 13/06/2026 (Plan completo al 16/06/2026)
> **Estado:** FASE 1-3 planificadas y aprobadas
> **Versión:** 2.1

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
**Objetivo:** Calcular indicadores técnicos en tiempo real sobre datos de Deriv

```
[Data Store (Polars)] → [Indicator Engine] → [Signal Generator]
```

**Regla de la FASE 2:**
- Cada indicador es una clase independiente
- Todos aceptan DataFrame de Polars como entrada
- Todos retornan Series de Polars como salida
- Configurable vía settings.toml (períodos, pesos, etc.)
- Sin dependencias de trading — solo cálculo matemático

---

#### 📁 2.1 Estructura de archivos

```
ghost_trader/
├── indicators/
│   ├── __init__.py
│   ├── base.py           # Clase abstracta BaseIndicator
│   ├── trend.py           # Indicadores de tendencia (EMA, SMA, MACD)
│   ├── momentum.py        # Indicadores de momentum (RSI, Stochastic)
│   ├── volatility.py      # Indicadores de volatilidad (Bollinger, ATR)
│   ├── volume.py          # Indicadores de volumen (OBV, VWAP)
│   └── patterns.py        # Patrones de velas
├── signals/
│   ├── __init__.py
│   ├── generator.py       # Generador de señales compuestas
│   └── models.py          # Modelos de señal (Buy, Sell, Hold)
```

---

#### 🧮 2.2 Clase Base (indicators/base.py)

```python
"""Clase abstracta para todos los indicadores."""

from abc import ABC, abstractmethod
from enum import Enum
import polars as pl


class IndicatorType(Enum):
    """Tipo de indicador."""
    TREND = "trend"
    MOMENTUM = "momentum"
    VOLATILITY = "volatility"
    VOLUME = "volume"
    PATTERN = "pattern"


class BaseIndicator(ABC):
    """Interfaz base para todos los indicadores."""

    def __init__(self, name: str, indicator_type: IndicatorType, period: int):
        self._name = name
        self._type = indicator_type
        self._period = period

    @property
    def name(self) -> str:
        return self._name

    @property
    def indicator_type(self) -> IndicatorType:
        return self._type

    @property
    def period(self) -> int:
        return self._period

    @abstractmethod
    def calculate(self, df: pl.DataFrame) -> pl.Series:
        """
        Calcula el indicador sobre un DataFrame.
        
        Args:
            df: DataFrame con columnas [open, high, low, close, volume]
        
        Returns:
            Series con los valores del indicador
        """
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(period={self._period})"
```

**Reglas:**
- Todos los indicadores heredan de BaseIndicator
- `calculate()` acepta DataFrame Polars, retorna Series Polars
- Sin efectos secundarios — solo calcula
- Nombre y período configurables

---

#### 📈 2.3 Indicadores de Tendencia (indicators/trend.py)

```python
"""Indicadores de tendencia: EMA, SMA, MACD."""

import polars as pl
from ghost_trader.indicators.base import BaseIndicator, IndicatorType


class SMA(BaseIndicator):
    """Simple Moving Average."""

    def __init__(self, period: int = 20):
        super().__init__(
            name=f"SMA_{period}",
            indicator_type=IndicatorType.TREND,
            period=period,
        )

    def calculate(self, df: pl.DataFrame) -> pl.Series:
        return df["close"].rolling_mean(window_size=self._period)


class EMA(BaseIndicator):
    """Exponential Moving Average."""

    def __init__(self, period: int = 20):
        super().__init__(
            name=f"EMA_{period}",
            indicator_type=IndicatorType.TREND,
            period=period,
        )

    def calculate(self, df: pl.DataFrame) -> pl.Series:
        return df["close"].ewm_mean(span=self._period)


class MACD(BaseIndicator):
    """Moving Average Convergence Divergence."""

    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9):
        super().__init__(
            name=f"MACD_{fast}_{slow}_{signal}",
            indicator_type=IndicatorType.TREND,
            period=slow,
        )
        self._fast = fast
        self._slow = slow
        self._signal = signal

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Retorna DataFrame con columnas: macd_line, signal_line, histogram."""
        ema_fast = df["close"].ewm_mean(span=self._fast)
        ema_slow = df["close"].ewm_mean(span=self._slow)
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm_mean(span=self._signal)
        histogram = macd_line - signal_line
        return pl.DataFrame({
            "macd_line": macd_line,
            "signal_line": signal_line,
            "histogram": histogram,
        })
```

---

#### 🔥 2.4 Indicadores de Momentum (indicators/momentum.py)

```python
"""Indicadores de momentum: RSI, Stochastic."""

import polars as pl
from ghost_trader.indicators.base import BaseIndicator, IndicatorType


class RSI(BaseIndicator):
    """Relative Strength Index."""

    def __init__(self, period: int = 14):
        super().__init__(
            name=f"RSI_{period}",
            indicator_type=IndicatorType.MOMENTUM,
            period=period,
        )

    def calculate(self, df: pl.DataFrame) -> pl.Series:
        """Calcula RSI (0-100)."""
        delta = df["close"].diff()
        gain = delta.map_elements(lambda x: x if x > 0 else 0.0)
        loss = delta.map_elements(lambda x: -x if x < 0 else 0.0)
        avg_gain = gain.rolling_mean(window_size=self._period)
        avg_loss = loss.rolling_mean(window_size=self._period)
        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))
        return rsi


class Stochastic(BaseIndicator):
    """Stochastic Oscillator."""

    def __init__(self, k_period: int = 14, d_period: int = 3):
        super().__init__(
            name=f"Stoch_{k_period}_{d_period}",
            indicator_type=IndicatorType.MOMENTUM,
            period=k_period,
        )
        self._d_period = d_period

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Retorna DataFrame con %K y %D."""
        lowest_low = df["low"].rolling_min(window_size=self._period)
        highest_high = df["high"].rolling_max(window_size=self._period)
        k = 100.0 * (df["close"] - lowest_low) / (highest_high - lowest_low)
        d = k.rolling_mean(window_size=self._d_period)
        return pl.DataFrame({"percent_k": k, "percent_d": d})
```

---

#### 🌊 2.5 Indicadores de Volatilidad (indicators/volatility.py)

```python
"""Indicadores de volatilidad: Bollinger Bands, ATR."""

import polars as pl
from ghost_trader.indicators.base import BaseIndicator, IndicatorType


class BollingerBands(BaseIndicator):
    """Bollinger Bands (20, 2)."""

    def __init__(self, period: int = 20, std_dev: float = 2.0):
        super().__init__(
            name=f"BB_{period}_{std_dev}",
            indicator_type=IndicatorType.VOLATILITY,
            period=period,
        )
        self._std_dev = std_dev

    def calculate(self, df: pl.DataFrame) -> pl.DataFrame:
        """Retorna DataFrame con upper, middle, lower."""
        middle = df["close"].rolling_mean(window_size=self._period)
        std = df["close"].rolling_std(window_size=self._period)
        upper = middle + (self._std_dev * std)
        lower = middle - (self._std_dev * std)
        return pl.DataFrame({
            "bb_upper": upper,
            "bb_middle": middle,
            "bb_lower": lower,
        })


class ATR(BaseIndicator):
    """Average True Range."""

    def __init__(self, period: int = 14):
        super().__init__(
            name=f"ATR_{period}",
            indicator_type=IndicatorType.VOLATILITY,
            period=period,
        )

    def calculate(self, df: pl.DataFrame) -> pl.Series:
        """Calcula ATR."""
        high = df["high"]
        low = df["low"]
        close_prev = df["close"].shift(1)
        tr1 = high - low
        tr2 = (high - close_prev).abs()
        tr3 = (low - close_prev).abs()
        tr = tr1.max(tr2).max(tr3)
        return tr.rolling_mean(window_size=self._period)
```

---

#### 🕯️ 2.6 Patrones de Velas (indicators/patterns.py)

```python
"""Detección de patrones de velas."""

import polars as pl
from ghost_trader.indicators.base import BaseIndicator, IndicatorType


class Doji(BaseIndicator):
    """Detecta velas Doji (cuerpo pequeño vs mecha)."""

    def __init__(self, threshold: float = 0.1):
        super().__init__(
            name=f"Doji_{threshold}",
            indicator_type=IndicatorType.PATTERN,
            period=1,
        )
        self._threshold = threshold

    def calculate(self, df: pl.DataFrame) -> pl.Series:
        """Retorna 1 si es Doji, 0 si no."""
        body = (df["close"] - df["open"]).abs()
        total_range = df["high"] - df["low"]
        is_doji = (body / total_range) < self._threshold
        return is_doji.cast(pl.Int8)


class Engulfing(BaseIndicator):
    """Detecta patrones Engulfing (bullish/bearish)."""

    def __init__(self):
        super().__init__(
            name="Engulfing",
            indicator_type=IndicatorType.PATTERN,
            period=2,
        )

    def calculate(self, df: pl.DataFrame) -> pl.Series:
        """Retorna 1=bullish, -1=bearish, 0=none."""
        prev_open = df["open"].shift(1)
        prev_close = df["close"].shift(1)
        # Bullish engulfing
        bullish = (
            (prev_close < prev_open) &  # Vela anterior bajista
            (df["close"] > df["open"]) &  # Vela actual alcista
            (df["open"] <= prev_close) &  # Abre <= cierre anterior
            (df["close"] >= prev_open)    # Cierra >= apertura anterior
        )
        # Bearish engulfing
        bearish = (
            (prev_close > prev_open) &  # Vela anterior alcista
            (df["close"] < df["open"]) &  # Vela actual bajista
            (df["open"] >= prev_close) &
            (df["close"] <= prev_open)
        )
        result = pl.Series("pattern", [0] * len(df))
        result = result.with_mask(bullish, 1)
        result = result.with_mask(bearish, -1)
        return result
```

---

#### ⚡ 2.7 Signal Generator (signals/generator.py)

```python
"""Generador de señales compuestas a partir de indicadores."""

from enum import Enum
from dataclasses import dataclass
import polars as pl
from ghost_trader.indicators.base import BaseIndicator


class SignalType(Enum):
    """Tipo de señal."""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"


@dataclass(frozen=True)
class Signal:
    """Señal de trading."""
    signal_type: SignalType
    symbol: str
    strength: float      # 0.0 - 1.0
    reason: str
    indicators_used: tuple[str, ...]


class SignalGenerator:
    """Genera señales compuestas a partir de múltiples indicadores."""

    def __init__(self, indicators: list[BaseIndicator]):
        self._indicators = indicators

    def generate(self, df: pl.DataFrame, symbol: str) -> Signal:
        """Genera señal basada en todos los indicadores configurados."""
        buy_score = 0.0
        sell_score = 0.0
        reasons = []
        indicator_names = []

        for indicator in self._indicators:
            result = indicator.calculate(df)
            signal = self._evaluate_indicator(indicator, result)
            if signal == SignalType.BUY:
                buy_score += 1.0
                reasons.append(f"{indicator.name}: BUY")
            elif signal == SignalType.SELL:
                sell_score += 1.0
                reasons.append(f"{indicator.name}: SELL")
            indicator_names.append(indicator.name)

        total = buy_score + sell_score
        if total == 0:
            return Signal(SignalType.HOLD, symbol, 0.0, "Sin señales", tuple(indicator_names))

        if buy_score > sell_score:
            strength = buy_score / len(self._indicators)
            return Signal(SignalType.BUY, symbol, strength, "; ".join(reasons), tuple(indicator_names))
        elif sell_score > buy_score:
            strength = sell_score / len(self._indicators)
            return Signal(SignalType.SELL, symbol, strength, "; ".join(reasons), tuple(indicator_names))
        else:
            return Signal(SignalType.HOLD, symbol, 0.0, "Señales mixtas", tuple(indicator_names))

    def _evaluate_indicator(self, indicator, result) -> SignalType:
        """Evalúa un indicador individual y retorna señal."""
        from ghost_trader.indicators.momentum import RSI
        from ghost_trader.indicators.trend import EMA, SMA
        if isinstance(indicator, RSI):
            last_rsi = result[-1]
            if last_rsi < 30:
                return SignalType.BUY
            elif last_rsi > 70:
                return SignalType.SELL
        elif isinstance(indicator, (EMA, SMA)):
            # Implementar lógica de cruce
            pass
        return SignalType.HOLD
```

---

#### 🧪 2.8 Tests de la FASE 2

```python
# tests/unit/test_indicators.py
import polars as pl
from ghost_trader.indicators.trend import SMA, EMA, MACD
from ghost_trader.indicators.momentum import RSI
from ghost_trader.indicators.volatility import BollingerBands, ATR

def create_test_df(n: int = 100) -> pl.DataFrame:
    """Crea DataFrame de prueba con precios simulados."""
    import random
    random.seed(42)
    prices = [100.0]
    for _ in range(n - 1):
        prices.append(prices[-1] * (1 + random.uniform(-0.02, 0.02)))
    return pl.DataFrame({
        "open": prices,
        "high": [p * 1.01 for p in prices],
        "low": [p * 0.99 for p in prices],
        "close": prices,
        "volume": [1000] * n,
    })

def test_sma():
    df = create_test_df()
    sma = SMA(period=20)
    result = sma.calculate(df)
    assert len(result) == len(df)
    assert result[-1] is not None

def test_ema():
    df = create_test_df()
    ema = EMA(period=20)
    result = ema.calculate(df)
    assert len(result) == len(df)

def test_rsi():
    df = create_test_df()
    rsi = RSI(period=14)
    result = rsi.calculate(df)
    assert len(result) == len(df)
    assert result[-1] >= 0 and result[-1] <= 100

def test_bollinger():
    df = create_test_df()
    bb = BollingerBands(period=20)
    result = bb.calculate(df)
    assert "bb_upper" in result.columns
    assert "bb_middle" in result.columns
    assert "bb_lower" in result.columns

def test_atr():
    df = create_test_df()
    atr = ATR(period=14)
    result = atr.calculate(df)
    assert len(result) == len(df)
    assert result[-1] > 0  # ATR siempre positivo
```

---

#### 📋 2.9 Checklist de Aprobación FASE 2

- [ ] Clase BaseIndicator abstracta funcionando
- [ ] SMA, EMA, MACD calculando correctamente
- [ ] RSI, Stochastic calculando correctamente
- [ ] BollingerBands, ATR calculando correctamente
- [ ] Patrones Doji y Engulfing detectando correctamente
- [ ] SignalGenerator generando señales compuestas
- [ ] Todos los tests pasan (`pytest tests/unit/ -v`)
- [ ] Sin hardcoding — períodos configurables desde settings.toml
- [ ] Performance: cálculo de 1000 velas < 100ms
- [ ] Documentación de cada indicador (qué mide, cuándo usar)

**Si algún punto falla → NO avanzar a FASE 3.**

---

**Entregable FASE 2:**
- Motor de indicadores completo (6 indicadores + 2 patrones)
- SignalGenerator para señales compuestas
- Tests pasando al 100%
- Configuración de períodos vía settings.toml

### FASE 3: Strategy Engine & Backtesting (Semanas 5-6) ✅ PLANIFICADA
**Objetivo:** Definir estrategias de trading como clases OOP, simularlas con datos históricos reales, y validar su rentabilidad antes de poner dinero real.

```
[Señales FASE 2] → [Strategy Engine] → [Trade Proposals]
[Datos Históricos] → [Backtest Engine] → [Métricas de rendimiento]
```

#### 📁 3.1 Estructura de archivos

```
ghost_trader/
├── strategy/
│   ├── __init__.py
│   ├── base.py              # Clase abstracta Strategy
│   ├── ema_cross.py         # Estrategia piloto: EMA Crossover
│   ├── rsi_reversal.py      # Estrategia: RSI Overbought/Oversold
│   ├── registry.py          # Registro de estrategias disponibles
│   └── models.py            # Modelos: TradeProposal, TradeAction
├── backtest/
│   ├── __init__.py
│   ├── engine.py            # Motor de backtesting
│   ├── metrics.py           # Cálculo de métricas (Sharpe, Sortino, etc.)
│   └── report.py            # Generación de reportes (JSON/CSV)
```

#### 🎯 3.2 Clase Abstracta Strategy (strategy/base.py)

```python
"""Clase abstracta para todas las estrategias de trading."""

from abc import ABC, abstractmethod
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import polars as pl


class TradeAction(Enum):
    """Acción de trading propuesta."""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    CLOSE = "close"


@dataclass(frozen=True)
class TradeProposal:
    """Propuesta de trade generada por una estrategia."""
    action: TradeAction
    symbol: str
    price: float
    timestamp: datetime
    strength: float              # 0.0 - 1.0 (qué tan fuerte es la señal)
    reason: str                  # Explicación legible
    metadata: dict = field(default_factory=dict)  # Datos extra


class Strategy(ABC):
    """Interfaz base para todas las estrategias."""

    def __init__(self, name: str, symbols: list[str], timeframe: str = "1m"):
        self._name = name
        self._symbols = symbols
        self._timeframe = timeframe
        self._position: dict[str, float] = {}  # symbol → cantidad abierta

    @property
    def name(self) -> str:
        return self._name

    @property
    def symbols(self) -> list[str]:
        return self._symbols

    @property
    def timeframe(self) -> str:
        return self._timeframe

    @abstractmethod
    def evaluate(self, df: pl.DataFrame, symbol: str) -> TradeProposal:
        """
        Evalúa el mercado y retorna una propuesta de trade.
        
        Args:
            df: DataFrame con OHLCV + indicadores pre-calculados
            symbol: Símbolo actual evaluado
            
        Returns:
            TradeProposal con la acción recomendada
        """
        ...

    @abstractmethod
    def required_indicators(self) -> list[str]:
        """
        Retorna lista de indicadores que necesita esta estrategia.
        Ejemplo: ["EMA_20", "EMA_50", "RSI_14"]
        """
        ...

    def has_position(self, symbol: str) -> bool:
        """Verifica si hay posición abierta en un símbolo."""
        return self._position.get(symbol, 0) > 0

    def open_position(self, symbol: str, size: float) -> None:
        """Registra apertura de posición."""
        self._position[symbol] = size

    def close_position(self, symbol: str) -> None:
        """Registra cierre de posición."""
        self._position[symbol] = 0

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(symbols={self._symbols}, tf={self._timeframe})"
```

**Reglas:**
- Cada estrategia es una clase independiente que hereda de `Strategy`
- `evaluate()` es la función principal — recibe datos, retorna propuesta
- `required_indicators()` dice al sistema qué indicadores calcular antes
- Las posiciones se rastrean internamente (para lógica de cierre)
- Sin efectos secundarios en evaluate — solo analiza y propone

#### 📈 3.3 Estrategia Piloto: EMA Crossover (strategy/ema_cross.py)

```python
"""Estrategia piloto: EMA Crossover (cruce de medias móviles exponenciales)."""

import polars as pl
from ghost_trader.strategy.base import Strategy, TradeProposal, TradeAction
from datetime import datetime


class EMACross(Strategy):
    """
    Estrategia de cruce EMA.
    
    Señal BUY:  EMA rápida cruza POR ENCIMA de EMA lenta (tendencia alcista)
    Señal SELL: EMA rápida cruza POR DEBAJO de EMA lenta (tendencia bajista)
    
    Configurable:
    - fast_period: período de EMA rápida (default 20)
    - slow_period: período de EMA lenta (default 50)
    - confirmation_bars: velas de confirmación (default 1)
    """

    def __init__(
        self,
        symbols: list[str],
        fast_period: int = 20,
        slow_period: int = 50,
        confirmation_bars: int = 1,
        timeframe: str = "1m",
    ):
        super().__init__(
            name=f"EMACross_{fast_period}_{slow_period}",
            symbols=symbols,
            timeframe=timeframe,
        )
        self._fast_period = fast_period
        self._slow_period = slow_period
        self._confirmation_bars = confirmation_bars

    def required_indicators(self) -> list[str]:
        return [f"EMA_{self._fast_period}", f"EMA_{self._slow_period}"]

    def evaluate(self, df: pl.DataFrame, symbol: str) -> TradeProposal:
        """Evalúa cruce de EMAs y retorna propuesta."""
        if len(df) < self._slow_period + self._confirmation_bars:
            return TradeProposal(
                action=TradeAction.HOLD,
                symbol=symbol,
                price=df["close"][-1],
                timestamp=datetime.now(),
                strength=0.0,
                reason="Datos insuficientes",
            )

        ema_fast = df["close"].ewm_mean(span=self._fast_period)
        ema_slow = df["close"].ewm_mean(span=self._slow_period)

        # Detectar cruce en las últimas N velas
        current_fast = ema_fast[-1]
        current_slow = ema_slow[-1]
        prev_fast = ema_fast[-1 - self._confirmation_bars]
        prev_slow = ema_slow[-1 - self._confirmation_bars]

        crossed_up = prev_fast <= prev_slow and current_fast > current_slow
        crossed_down = prev_fast >= prev_slow and current_fast < current_slow

        current_price = df["close"][-1]

        # Calcular fuerza de la señal (diferencia normalizada)
        diff = abs(current_fast - current_slow) / current_slow
        strength = min(diff * 100, 1.0)  # Normalizar a 0-1

        if crossed_up and not self.has_position(symbol):
            return TradeProposal(
                action=TradeAction.BUY,
                symbol=symbol,
                price=current_price,
                timestamp=datetime.now(),
                strength=strength,
                reason=f"EMA {self._fast_period} cruza por encima de EMA {self._slow_period}",
                metadata={"ema_fast": current_fast, "ema_slow": current_slow},
            )
        elif crossed_down and self.has_position(symbol):
            return TradeProposal(
                action=TradeAction.CLOSE,
                symbol=symbol,
                price=current_price,
                timestamp=datetime.now(),
                strength=strength,
                reason=f"EMA {self._fast_period} cruza por debajo de EMA {self._slow_period}",
                metadata={"ema_fast": current_fast, "ema_slow": current_slow},
            )
        else:
            return TradeProposal(
                action=TradeAction.HOLD,
                symbol=symbol,
                price=current_price,
                timestamp=datetime.now(),
                strength=0.0,
                reason="Sin cruce detectado",
            )
```

#### 🔄 3.4 Registro de Estrategias (strategy/registry.py)

```python
"""Registro central de estrategias disponibles."""

from ghost_trader.strategy.base import Strategy
from ghost_trader.strategy.ema_cross import EMACross


class StrategyRegistry:
    """Registry para gestionar estrategias disponibles."""

    _strategies: dict[str, type[Strategy]] = {}

    @classmethod
    def register(cls, name: str, strategy_class: type[Strategy]) -> None:
        """Registra una estrategia nueva."""
        cls._strategies[name] = strategy_class

    @classmethod
    def get(cls, name: str) -> type[Strategy] | None:
        """Obtiene una estrategia por nombre."""
        return cls._strategies.get(name)

    @classmethod
    def list_all(cls) -> list[str]:
        """Lista todas las estrategias registradas."""
        return list(cls._strategies.keys())

    @classmethod
    def create(cls, name: str, **kwargs) -> Strategy:
        """Crea una instancia de una estrategia."""
        strategy_class = cls._strategies.get(name)
        if not strategy_class:
            raise ValueError(f"Estrategia no encontrada: {name}")
        return strategy_class(**kwargs)


# Auto-registrar estrategias al importar
StrategyRegistry.register("ema_cross", EMACross)
```

#### 🧪 3.5 Motor de Backtesting (backtest/engine.py)

```python
"""Motor de backtesting — simulación vela por vela con datos reales."""

from dataclasses import dataclass, field
from datetime import datetime
import polars as pl
from ghost_trader.strategy.base import Strategy, TradeProposal, TradeAction
from ghost_trader.backtest.metrics import calculate_metrics


@dataclass
class BacktestTrade:
    """Trade ejecutado en el backtest."""
    entry_time: datetime
    exit_time: datetime | None
    symbol: str
    action: str            # "buy" / "sell"
    entry_price: float
    exit_price: float | None
    pnl: float | None
    reason_entry: str
    reason_exit: str | None


@dataclass
class BacktestResult:
    """Resultado completo del backtest."""
    strategy_name: str
    symbol: str
    timeframe: str
    start_date: datetime
    end_date: datetime
    total_trades: int
    winning_trades: int
    losing_trades: int
    trades: list[BacktestTrade]
    equity_curve: list[float]
    metrics: dict          # Sharpe, Sortino, etc.


class BacktestEngine:
    """Motor de backtesting vela por vela."""

    def __init__(
        self,
        initial_balance: float = 10000.0,
        commission_pct: float = 0.001,    # 0.1% por trade
        slippage_pct: float = 0.0005,     # 0.05% slippage
        position_size_pct: float = 0.02,  # 2% del balance por trade
    ):
        self._initial_balance = initial_balance
        self._commission_pct = commission_pct
        self._slippage_pct = slippage_pct
        self._position_size_pct = position_size_pct

    def run(
        self,
        strategy: Strategy,
        df: pl.DataFrame,
        symbol: str,
    ) -> BacktestResult:
        """Ejecuta backtest completo de una estrategia."""
        balance = self._initial_balance
        equity_curve = [balance]
        trades: list[BacktestTrade] = []
        current_trade: BacktestTrade | None = None

        # Ventana mínima para indicadores
        lookback = max(strategy.required_indicators(), key=len) if strategy.required_indicators() else "20"
        min_bars = int(lookback.split("_")[-1]) if "_" in lookback else 50

        for i in range(min_bars, len(df)):
            # Slice de datos hasta el punto actual (sin lookahead)
            window = df.slice(0, i + 1)
            current_bar = df.row(i, named=True)

            # Evaluar estrategia
            proposal = strategy.evaluate(window, symbol)

            # Ejecutar propuesta
            if proposal.action == TradeAction.BUY and current_trade is None:
                # Abrir posición LONG
                entry_price = current_bar["close"] * (1 + self._slippage_pct)
                position_size = balance * self._position_size_pct
                commission = position_size * self._commission_pct

                current_trade = BacktestTrade(
                    entry_time=current_bar["timestamp"],
                    exit_time=None,
                    symbol=symbol,
                    action="buy",
                    entry_price=entry_price,
                    exit_price=None,
                    pnl=None,
                    reason_entry=proposal.reason,
                    reason_exit=None,
                )
                strategy.open_position(symbol, position_size)
                balance -= commission

            elif proposal.action == TradeAction.CLOSE and current_trade is not None:
                # Cerrar posición
                exit_price = current_bar["close"] * (1 - self._slippage_pct)
                commission = (exit_price * abs(current_trade.entry_price)) * self._commission_pct

                pnl = (exit_price - current_trade.entry_price) / current_trade.entry_price
                pnl_amount = pnl * (balance * self._position_size_pct)

                current_trade.exit_time = current_bar["timestamp"]
                current_trade.exit_price = exit_price
                current_trade.pnl = pnl_amount - commission
                current_trade.reason_exit = proposal.reason

                trades.append(current_trade)
                balance += pnl_amount - commission
                equity_curve.append(balance)

                strategy.close_position(symbol)
                current_trade = None

        # Cerrar posición abierta al final
        if current_trade is not None:
            last_bar = df.row(-1, named=True)
            exit_price = last_bar["close"]
            pnl = (exit_price - current_trade.entry_price) / current_trade.entry_price
            pnl_amount = pnl * (balance * self._position_size_pct)

            current_trade.exit_time = last_bar["timestamp"]
            current_trade.exit_price = exit_price
            current_trade.pnl = pnl_amount
            current_trade.reason_exit = "Fin del backtest"
            trades.append(current_trade)
            balance += pnl_amount
            equity_curve.append(balance)

        # Calcular métricas
        winning = [t for t in trades if t.pnl and t.pnl > 0]
        losing = [t for t in trades if t.pnl and t.pnl <= 0]

        metrics = calculate_metrics(
            trades=trades,
            equity_curve=equity_curve,
            initial_balance=self._initial_balance,
        )

        return BacktestResult(
            strategy_name=strategy.name,
            symbol=symbol,
            timeframe=strategy.timeframe,
            start_date=df["timestamp"][0],
            end_date=df["timestamp"][-1],
            total_trades=len(trades),
            winning_trades=len(winning),
            losing_trades=len(losing),
            trades=trades,
            equity_curve=equity_curve,
            metrics=metrics,
        )
```

#### 📊 3.6 Métricas de Rendimiento (backtest/metrics.py)

```python
"""Cálculo de métricas de rendimiento para backtesting."""

import math
from ghost_trader.backtest.engine import BacktestTrade


def calculate_metrics(
    trades: list[BacktestTrade],
    equity_curve: list[float],
    initial_balance: float,
) -> dict:
    """Calcula todas las métricas de rendimiento."""
    if not trades:
        return {"error": "No hay trades para analizar"}

    pnls = [t.pnl for t in trades if t.pnl is not None]
    returns = [(e - initial_balance) / initial_balance for e in equity_curve[1:]]

    return {
        # Retorno total
        "total_return_pct": _total_return(equity_curve, initial_balance),
        "annualized_return_pct": _annualized_return(equity_curve, initial_balance, trades),

        # Métricas de riesgo
        "sharpe_ratio": _sharpe_ratio(returns),
        "sortino_ratio": _sortino_ratio(returns),
        "max_drawdown_pct": _max_drawdown(equity_curve),
        "max_drawdown_duration": _max_drawdown_duration(equity_curve),

        # Win/Loss
        "win_rate_pct": _win_rate(trades),
        "profit_factor": _profit_factor(pnls),
        "expectancy": _expectancy(pnls),
        "avg_win": _avg_win(pnls),
        "avg_loss": _avg_loss(pnls),
        "payoff_ratio": _payoff_ratio(pnls),

        # Operaciones
        "total_trades": len(trades),
        "winning_trades": len([p for p in pnls if p > 0]),
        "losing_trades": len([p for p in pnls if p <= 0]),
        "avg_trade_pnl": sum(pnls) / len(pnls) if pnls else 0,
    }


def _total_return(equity: list[float], initial: float) -> float:
    return ((equity[-1] - initial) / initial) * 100


def _annualized_return(equity: list[float], initial: float, trades: list[BacktestTrade]) -> float:
    if len(trades) < 2:
        return 0.0
    days = (trades[-1].exit_time - trades[0].entry_time).days
    if days <= 0:
        return 0.0
    total_ret = equity[-1] / initial
    return ((total_ret ** (365 / days)) - 1) * 100


def _sharpe_ratio(returns: list[float], risk_free_rate: float = 0.0) -> float:
    if not returns or len(returns) < 2:
        return 0.0
    avg_ret = sum(returns) / len(returns)
    variance = sum((r - avg_ret) ** 2 for r in returns) / (len(returns) - 1)
    std_dev = math.sqrt(variance) if variance > 0 else 0.001
    return (avg_ret - risk_free_rate) / std_dev


def _sortino_ratio(returns: list[float], risk_free_rate: float = 0.0) -> float:
    if not returns:
        return 0.0
    avg_ret = sum(returns) / len(returns)
    downside = [r for r in returns if r < 0]
    if not downside:
        return float('inf') if avg_ret > risk_free_rate else 0.0
    downside_var = sum(r ** 2 for r in downside) / len(downside)
    downside_std = math.sqrt(downside_var) if downside_var > 0 else 0.001
    return (avg_ret - risk_free_rate) / downside_std


def _max_drawdown(equity: list[float]) -> float:
    if not equity:
        return 0.0
    peak = equity[0]
    max_dd = 0.0
    for e in equity:
        if e > peak:
            peak = e
        dd = (peak - e) / peak
        if dd > max_dd:
            max_dd = dd
    return max_dd * 100


def _max_drawdown_duration(equity: list[float]) -> int:
    if not equity:
        return 0
    peak = equity[0]
    duration = 0
    max_duration = 0
    for e in equity:
        if e >= peak:
            peak = e
            duration = 0
        else:
            duration += 1
            max_duration = max(max_duration, duration)
    return max_duration


def _win_rate(trades: list[BacktestTrade]) -> float:
    if not trades:
        return 0.0
    winning = len([t for t in trades if t.pnl and t.pnl > 0])
    return (winning / len(trades)) * 100


def _profit_factor(pnls: list[float]) -> float:
    if not pnls:
        return 0.0
    gross_profit = sum(p for p in pnls if p > 0)
    gross_loss = abs(sum(p for p in pnls if p < 0))
    return gross_profit / gross_loss if gross_loss > 0 else float('inf')


def _expectancy(pnls: list[float]) -> float:
    if not pnls:
        return 0.0
    return sum(pnls) / len(pnls)


def _avg_win(pnls: list[float]) -> float:
    wins = [p for p in pnls if p > 0]
    return sum(wins) / len(wins) if wins else 0.0


def _avg_loss(pnls: list[float]) -> float:
    losses = [p for p in pnls if p < 0]
    return sum(losses) / len(losses) if losses else 0.0


def _payoff_ratio(pnls: list[float]) -> float:
    aw = _avg_win(pnls)
    al = abs(_avg_loss(pnls))
    return aw / al if al > 0 else float('inf')
```

#### 📄 3.7 Exportación de Reportes (backtest/report.py)

```python
"""Generación de reportes de backtesting."""

import json
import csv
from pathlib import Path
from ghost_trader.backtest.engine import BacktestResult


def export_json(result: BacktestResult, path: str) -> None:
    """Exporta resultado a JSON."""
    data = {
        "strategy": result.strategy_name,
        "symbol": result.symbol,
        "timeframe": result.timeframe,
        "period": f"{result.start_date} → {result.end_date}",
        "summary": {
            "total_trades": result.total_trades,
            "winning_trades": result.winning_trades,
            "losing_trades": result.losing_trades,
            "win_rate_pct": result.metrics.get("win_rate_pct", 0),
            "total_return_pct": result.metrics.get("total_return_pct", 0),
            "sharpe_ratio": result.metrics.get("sharpe_ratio", 0),
            "max_drawdown_pct": result.metrics.get("max_drawdown_pct", 0),
            "profit_factor": result.metrics.get("profit_factor", 0),
        },
        "metrics": result.metrics,
        "trades": [
            {
                "entry_time": str(t.entry_time),
                "exit_time": str(t.exit_time),
                "action": t.action,
                "entry_price": t.entry_price,
                "exit_price": t.exit_price,
                "pnl": t.pnl,
                "reason_entry": t.reason_entry,
                "reason_exit": t.reason_exit,
            }
            for t in result.trades
        ],
    }
    Path(path).write_text(json.dumps(data, indent=2, default=str))


def export_csv(result: BacktestResult, path: str) -> None:
    """Exporta trades a CSV."""
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "entry_time", "exit_time", "action", "symbol",
            "entry_price", "exit_price", "pnl", "reason_entry", "reason_exit"
        ])
        for t in result.trades:
            writer.writerow([
                t.entry_time, t.exit_time, t.action, t.symbol,
                t.entry_price, t.exit_price, t.pnl, t.reason_entry, t.reason_exit,
            ])
```

#### 🧪 3.8 Tests de la FASE 3

```python
# tests/unit/test_strategy.py
import polars as pl
from ghost_trader.strategy.base import TradeAction
from ghost_trader.strategy.ema_cross import EMACross

def create_test_df(n: int = 200) -> pl.DataFrame:
    """DataFrame con tendencia alcista simulada."""
    import random
    random.seed(42)
    prices = [100.0]
    for _ in range(n - 1):
        prices.append(prices[-1] * (1 + random.uniform(0.0001, 0.003)))
    return pl.DataFrame({
        "open": prices,
        "high": [p * 1.005 for p in prices],
        "low": [p * 0.995 for p in prices],
        "close": prices,
        "volume": [1000] * n,
    })

def test_ema_cross_hold():
    """Sin cruce → HOLD."""
    df = create_test_df()
    strategy = EMACross(symbols=["v75"], fast_period=20, slow_period=50)
    proposal = strategy.evaluate(df, "v75")
    assert proposal.action == TradeAction.HOLD

def test_ema_cross_required_indicators():
    strategy = EMACross(symbols=["v75"], fast_period=20, slow_period=50)
    indicators = strategy.required_indicators()
    assert "EMA_20" in indicators
    assert "EMA_50" in indicators


# tests/unit/test_backtest.py
from ghost_trader.backtest.engine import BacktestEngine
from ghost_trader.strategy.ema_cross import EMACross

def test_backtest_runs():
    """Backtest completa sin errores."""
    df = create_test_df(500)
    strategy = EMACross(symbols=["v75"], fast_period=10, slow_period=30)
    engine = BacktestEngine(initial_balance=10000.0)
    result = engine.run(strategy, df, "v75")
    assert result.strategy_name == strategy.name
    assert result.symbol == "v75"
    assert len(result.equity_curve) > 0

def test_backtest_metrics():
    """Métricas se calculan correctamente."""
    df = create_test_df(500)
    strategy = EMACross(symbols=["v75"], fast_period=10, slow_period=30)
    engine = BacktestEngine()
    result = engine.run(strategy, df, "v75")
    assert "sharpe_ratio" in result.metrics
    assert "max_drawdown_pct" in result.metrics
    assert "win_rate_pct" in result.metrics


# tests/unit/test_metrics.py
from ghost_trader.backtest.metrics import calculate_metrics
from ghost_trader.backtest.engine import BacktestTrade
from datetime import datetime

def test_metrics_empty_trades():
    metrics = calculate_metrics([], [10000], 10000)
    assert "error" in metrics

def test_metrics_with_trades():
    trades = [
        BacktestTrade(datetime(2026,1,1), datetime(2026,1,2), "v75", "buy", 100, 105, 50, "entry", "exit"),
        BacktestTrade(datetime(2026,1,3), datetime(2026,1,4), "v75", "buy", 105, 103, -30, "entry", "exit"),
    ]
    equity = [10000, 10050, 10020]
    metrics = calculate_metrics(trades, equity, 10000)
    assert metrics["total_trades"] == 2
    assert metrics["win_rate_pct"] == 50.0
```

#### 📋 3.9 Checklist de Aprobación FASE 3

- [ ] Clase abstracta Strategy funcionando
- [ ] EMACross implementada y evaluando correctamente
- [ ] StrategyRegistry registrando y listando estrategias
- [ ] BacktestEngine simulando vela por vela (sin lookahead)
- [ ] Métricas calculándose: Sharpe, Sortino, Max DD, Win Rate, Profit Factor
- [ ] Exportación JSON y CSV funcionando
- [ ] Tests unitarios pasando al 100%
- [ ] Comisión y slippage aplicados en cada trade
- [ ] Position sizing configurable (% del balance)
- [ ] Documentación de métricas (qué significa cada una)

**Si algún punto falla → NO avanzar a FASE 4.**

**Entregable FASE 3:**
- Estrategia EMACross completa y probada
- Motor de backtesting con datos históricos reales
- Reporte con métricas de rendimiento
- Validación de que la estrategia es rentable en histórico

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
