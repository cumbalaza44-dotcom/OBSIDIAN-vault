# 🏗️ Ghost Trader — Plan de Construcción

> **Fecha original:** 13/06/2026 (Plan completo al 16/06/2026)
> **Fecha revisión:** 17/08/2026
> **Estado:** FASE 1-3 construidas ✅ · FASE 4-6 planificadas en detalle
> **Versión:** 2.3 (FASE 4-6 detalladas)

---

## 📝 Bitácora de Correcciones (v2.1 → v2.3)

| # | Corrección | Severidad |
|---|------------|-----------|
| 1 | Símbolos de Deriv corregidos: `v75`/`v50` → `R_75`/`R_50` (nombres reales del API) | 🔴 Crítica |
| 2 | Se añadió el paso `authorize` al conector (faltaba enviar el `auth_token`) | 🔴 Crítica |
| 3 | `@dataclass` agregado a `DerivConfig`, `DataConfig`, `HeartbeatConfig` (sin él, `**raw` explota) | 🔴 Crítica |
| 4 | Typo `)n` en `_on_tick` de `deriv_ws.py` (error de sintaxis) | 🔴 Crítica |
| 5 | Granularidad: Deriv usa **segundos enteros**, no strings. Se añadió `GRANULARITY_MAP` | 🔴 Crítica |
| 6 | Reconexión: `run()` desconectaba tras reconectar. Ahora `_reconnect()` restaura autorización + suscripciones y el loop continúa | 🟠 Importante |
| 7 | Timestamps en **UTC** (`timezone.utc`) en vez de hora local | 🟠 Importante |
| 8 | `Engulfing`: `with_mask` no existe así en Polars → `pl.when().then().otherwise()` | 🟠 Importante |
| 9 | `ATR`: `tr1.max(tr2)` no es max elemental → `pl.max_horizontal()` | 🟠 Importante |
| 10 | `RSI`: vectorizado con `clip()` + manejo de división por cero (`fill_nan`) | 🟠 Importante |
| 11 | `BaseIndicator.calculate`: firma acepta `pl.DataFrame \| pl.Series` (MACD/Stochastic/BB retornan DataFrame) | 🟠 Importante |
| 12 | Estrategias: `datetime.now()` → timestamp de la vela (backtest determinista) | 🟠 Importante |
| 13 | Backtest: `min_bars()` propio de cada estrategia (antes inferido frágil de strings) | 🟠 Importante |
| 14 | Backtest: position sizing consistente + comisión correcta (sin doble cobro) | 🟠 Importante |
| 15 | `requirements.txt` y `pyproject.toml` definidos con **polars pineado** (API cambia mucho entre versiones) | 🟢 Menor |
| 16 | `settings.toml`: secciones `[indicators]` y `[strategies]` añadidas (FASE 2 decía configurable pero no existían) | 🟢 Menor |
| 17 | Tests: `create_test_df` movido a `tests/conftest.py` como fixture compartido | 🟢 Menor |
| 18 | Texto chino accidental (`事件驱动`) corregido | 🟢 Menor |
| 19 | **FASE 4-6 detalladas** (arquitectura, código, settings, tests y checklist — antes solo eran objetivos) | 🟢 Menor |
| 20 | FASE 4 aclara que Deriv opera **contratos** (opciones digitales / multipliers), no órdenes SL/TP tradicionales; el Risk Engine es broker-agnóstico | 🟢 Menor |

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

### FASE 1: Conexión & Datos (Semanas 1-2) ✅ CONSTRUIDA
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
│   └── conftest.py           # Fixtures compartidos
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
auth_token = ""                  # Token de autenticación (cuenta demo)
endpoint = "wss://ws.derivws.com/websockets/v3?app_id=1089"

[deriv.symbols]
# Símbolos REALES de Deriv (índices sintéticos)
# Volatility: R_10, R_25, R_50, R_75, R_100
# Volatility 1s (alta frecuencia): 1HZ10V, 1HZ25V, 1HZ50V, 1HZ75V, 1HZ100V...
# Boom/Crash: BOOM300/500/1000, CRASH300/500/1000
volatility_75 = "R_75"
volatility_50 = "R_50"
volatility_75_1s = "1HZ75V"
boom_1000 = "BOOM1000"
crash_1000 = "CRASH1000"

[data]
tick_buffer_size = 10000        # Ticks máximos en memoria
history_candles = 500           # Velas históricas a descargar
default_granularity = "1m"      # Granularidad por defecto
timezone = "UTC"                # Zona horaria para timestamps
# Deriv usa granularidad en SEGUNDOS (no strings)
granularities = { "1m" = 60, "5m" = 300, "15m" = 900, "30m" = 1800, "1h" = 3600, "4h" = 14400 }

[heartbeat]
interval_seconds = 30           # Intervalo de ping/pong
reconnect_delay = 5             # Segundos entre reintentos
max_reconnect_attempts = 10     # Máximo de reintentos antes de fallar

[indicators]
# Períodos por defecto de los indicadores (FASE 2) — todos configurables
sma_period = 20
ema_period = 20
macd_fast = 12
macd_slow = 26
macd_signal = 9
rsi_period = 14
stoch_k_period = 14
stoch_d_period = 3
bollinger_period = 20
bollinger_std_dev = 2.0
atr_period = 14

[strategies]
# Estrategias activas y su configuración (FASE 3)
active = ["ema_cross"]

[strategies.ema_cross]
symbols = ["R_75"]
timeframe = "1m"
fast_period = 20
slow_period = 50
confirmation_bars = 1
```

**Archivo `ghost_trader/config.py`:**

```python
"""Configuración centralizada de Ghost Trader."""

from pathlib import Path
from dataclasses import dataclass, field
import tomllib


@dataclass(frozen=True)
class DerivConfig:
    """Configuración de conexión a Deriv."""
    app_id: int
    auth_token: str
    endpoint: str
    symbols: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class DataConfig:
    """Configuración del motor de datos."""
    tick_buffer_size: int = 10000
    history_candles: int = 500
    default_granularity: str = "1m"
    timezone: str = "UTC"
    granularities: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class HeartbeatConfig:
    """Configuración de heartbeat y reconexión."""
    interval_seconds: int = 30
    reconnect_delay: int = 5
    max_reconnect_attempts: int = 10


@dataclass(frozen=True)
class Settings:
    """Settings maestro de Ghost Trader."""
    deriv: DerivConfig
    data: DataConfig
    heartbeat: HeartbeatConfig
    indicators: dict[str, object] = field(default_factory=dict)
    strategies: dict[str, object] = field(default_factory=dict)

    @classmethod
    def from_file(cls, path: str = "config/settings.toml") -> "Settings":
        """Carga configuración desde archivo TOML."""
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config no encontrado: {config_path}")
        with open(config_path, "rb") as f:
            raw = tomllib.load(f)
        return cls(
            deriv=DerivConfig(**raw.get("deriv", {})),
            data=DataConfig(**raw.get("data", {})),
            heartbeat=HeartbeatConfig(**raw.get("heartbeat", {})),
            indicators=raw.get("indicators", {}),
            strategies=raw.get("strategies", {}),
        )
```

**Reglas:**
- Todo valor configurable DEBE estar en settings.toml
- Nunca hardcodear endpoints, tokens, símbolos en el código
- Si se necesita un valor nuevo → agregarlo primero a settings.toml
- Los defaults en constructores son solo fallbacks; settings.toml siempre manda

---

#### 🔌 1.3 Data Models (connector/models.py)

**Definir los modelos de datos que usará todo el sistema:**

```python
"""Modelos de datos para el conector Deriv."""

from dataclasses import dataclass
from datetime import datetime, timezone
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
        """Convierte timestamp a datetime (UTC)."""
        return datetime.fromtimestamp(self.timestamp / 1000, tz=timezone.utc)


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
        """Convierte timestamp a datetime (UTC)."""
        return datetime.fromtimestamp(self.timestamp / 1000, tz=timezone.utc)
```

**Reglas:**
- Modelos son `frozen=True` (inmutables) — un tick no cambia después de crearse
- Propiedades de conveniencia (datetime) en el modelo, no en el conector
- Enum para tipos fijos (TickSource)
- Sin dependencias externas en models.py (solo dataclasses, datetime, enum)
- Timestamps siempre en **UTC**

---

#### 🔌 1.4 Deriv WebSocket Connector (connector/deriv_ws.py)

**Clase principal:**

```python
"""Conector WebSocket para Deriv API."""

import asyncio
import json
import logging
from typing import Awaitable, Callable

import websockets
from websockets.exceptions import ConnectionClosed

from ghost_trader.config import Settings
from ghost_trader.connector.models import Tick, Candle, TickSource

logger = logging.getLogger(__name__)

# Deriv API usa granularidad en segundos enteros (no strings)
GRANULARITY_MAP = {
    "1m": 60, "5m": 300, "15m": 900, "30m": 1800,
    "1h": 3600, "4h": 14400,
}


def _to_deriv_granularity(granularity: str | int) -> int:
    """Convierte granularidad humana a segundos de Deriv."""
    if isinstance(granularity, int):
        return granularity
    if granularity not in GRANULARITY_MAP:
        raise ValueError(f"Granularidad no soportada: {granularity}")
    return GRANULARITY_MAP[granularity]


class DerivConnector:
    """Conector WebSocket persistente a Deriv API."""

    def __init__(self, settings: Settings):
        self._settings = settings
        self._ws = None
        self._running = False
        self._request_id = 0
        self._pending: dict[int, asyncio.Future] = {}
        self._subscribed_symbols: set[str] = set()
        self._on_tick_callback: Callable[[Tick], Awaitable[None]] | None = None

    async def connect(self) -> None:
        """Establece conexión, autoriza y restaura suscripciones."""
        url = self._settings.deriv.endpoint
        logger.info(f"Conectando a {url}...")
        self._ws = await websockets.connect(url)
        self._running = True
        await self._authorize()
        for symbol in self._subscribed_symbols:
            await self.subscribe_ticks(symbol)
        logger.info("Conexión establecida y suscripciones restauradas.")

    async def _authorize(self) -> None:
        """Envía el auth_token de Deriv (obligatorio antes de operar)."""
        token = self._settings.deriv.auth_token
        if not token:
            logger.warning("auth_token vacío en settings.toml — conexión sin autorizar.")
            return
        response = await self.request({"authorize": token})
        if "error" in response:
            raise ConnectionError(f"Authorize rechazado: {response['error']}")
        logger.info("Token autorizado.")

    async def disconnect(self) -> None:
        """Cierra la conexión WebSocket si existe."""
        if self._ws:
            await self._ws.close()
            self._ws = None
            logger.info("Conexión cerrada.")

    def stop(self) -> None:
        """Solicita detener el loop principal."""
        self._running = False

    async def _send(self, payload: dict) -> int:
        """Envía request, registra future y retorna req_id."""
        self._request_id += 1
        payload["req_id"] = self._request_id
        loop = asyncio.get_running_loop()
        self._pending[self._request_id] = loop.create_future()
        await self._ws.send(json.dumps(payload))
        return self._request_id

    async def request(self, payload: dict, timeout: float = 10.0) -> dict:
        """Envía un request y espera su respuesta (por req_id)."""
        req_id = await self._send(payload)
        try:
            return await asyncio.wait_for(self._pending[req_id], timeout=timeout)
        finally:
            self._pending.pop(req_id, None)

    async def _receive_loop(self) -> None:
        """Loop principal de recepción de mensajes."""
        async for message in self._ws:
            data = json.loads(message)
            req_id = data.get("req_id")
            if req_id and req_id in self._pending:
                future = self._pending[req_id]
                if not future.done():
                    future.set_result(data)
            elif "tick" in data:
                await self._on_tick(data)

    async def _on_tick(self, data: dict) -> None:
        """Procesa tick recibido."""
        tick_data = data["tick"]
        tick = Tick(
            symbol=tick_data["symbol"],
            price=float(tick_data["quote"]),
            timestamp=int(tick_data["epoch"]) * 1000,
            source=TickSource.LIVE,
        )
        if self._on_tick_callback:
            await self._on_tick_callback(tick)
        else:
            logger.debug(f"Tick: {tick.symbol} = {tick.price}")

    def on_tick(self, callback: Callable[[Tick], Awaitable[None]]) -> None:
        """Conecta un callback que recibe cada tick (se usa en FASE 2)."""
        self._on_tick_callback = callback

    async def subscribe_ticks(self, symbol: str) -> None:
        """Se suscribe a ticks en vivo de un símbolo."""
        await self._send({"ticks": symbol, "subscribe": 1})
        self._subscribed_symbols.add(symbol)
        logger.info(f"Suscrito a ticks: {symbol}")

    async def get_history(
        self, symbol: str, granularity: str | int, count: int
    ) -> list[Candle]:
        """Obtiene histórico de velas (espera la respuesta completa)."""
        response = await self.request({
            "ticks_history": symbol,
            "adjust_start_time": 1,
            "count": count,
            "granularity": _to_deriv_granularity(granularity),
            "style": "candles",
        })
        if "error" in response:
            logger.error(f"Histórico falló: {response['error']}")
            return []
        return [
            Candle(
                symbol=symbol,
                open=float(c["open"]),
                high=float(c["high"]),
                low=float(c["low"]),
                close=float(c["close"]),
                volume=int(c.get("volume", 0)),
                timestamp=int(c["epoch"]) * 1000,
                granularity=str(granularity),
            )
            for c in response["candles"]
        ]

    async def run(self) -> None:
        """Loop principal del conector (con reconexión automática)."""
        while self._running:
            try:
                await self.connect()
                await self._receive_loop()
            except (ConnectionClosed, OSError) as exc:
                logger.warning(f"Conexión perdida: {exc}. Reconectando...")
                await self._reconnect()
            except asyncio.CancelledError:
                break
            finally:
                await self.disconnect()

    async def _reconnect(self) -> None:
        """Reintenta conectar; connect() restaura autorización + suscripciones."""
        attempts = 0
        max_attempts = self._settings.heartbeat.max_reconnect_attempts
        while attempts < max_attempts:
            attempts += 1
            delay = self._settings.heartbeat.reconnect_delay
            logger.info(f"Reintento {attempts}/{max_attempts} en {delay}s...")
            await asyncio.sleep(delay)
            try:
                await self.connect()
                return
            except Exception as exc:
                logger.error(f"Reintento falló: {exc}")
        logger.error("Máximo de reintentos alcanzado.")
        self._running = False
```

**Reglas del conector:**
- El conector SOLO conecta y obtiene datos — NO ejecuta órdenes (eso es FASE 4)
- `authorize` es el primer paso obligatorio tras conectar
- Callbacks flexibles (`.on_tick()`) — se conectan después, no están hardcodeados
- Reconexión automática con límite de intentos; restaura suscripciones al reconectar
- Logging en cada evento importante (connect, authorize, disconnect, tick, error)
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

    def get_ticks(self, symbol: str | None = None) -> list[Tick]:
        """Retorna copia de los ticks del buffer (opcional filtrado por símbolo)."""
        ticks = self._tick_buffer
        if symbol:
            ticks = [t for t in ticks if t.symbol == symbol]
        return list(ticks)

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
# tests/conftest.py (fixtures compartidos)
import polars as pl
import pytest


@pytest.fixture
def uptrend_df() -> pl.DataFrame:
    """DataFrame con tendencia alcista simulada (precios crecientes)."""
    import random
    random.seed(42)
    prices = [100.0]
    for _ in range(199):
        prices.append(prices[-1] * (1 + random.uniform(0.0001, 0.003)))
    return pl.DataFrame({
        "open": prices,
        "high": [p * 1.005 for p in prices],
        "low": [p * 0.995 for p in prices],
        "close": prices,
        "volume": [1000] * 200,
        "timestamp": list(range(200)),
    })
```

```python
# tests/unit/test_models.py
from ghost_trader.connector.models import Tick, Candle, TickSource

def test_tick_creation():
    tick = Tick(symbol="R_75", price=1234.56, timestamp=1718316000000, source=TickSource.LIVE)
    assert tick.symbol == "R_75"
    assert tick.price == 1234.56
    assert tick.source == TickSource.LIVE

def test_tick_is_frozen():
    tick = Tick(symbol="R_75", price=1.0, timestamp=0, source=TickSource.LIVE)
    try:
        tick.price = 2.0
        assert False, "Debería ser inmutable"
    except AttributeError:
        pass

def test_tick_datetime_is_utc():
    tick = Tick(symbol="R_75", price=1.0, timestamp=1718316000000, source=TickSource.LIVE)
    assert tick.datetime.tzinfo is not None  # timezone-aware (UTC)

def test_candle_creation():
    candle = Candle(
        symbol="R_75", open=1.0, high=1.1, low=0.9, close=1.05,
        volume=100, timestamp=1718316000000, granularity="1m",
    )
    assert candle.granularity == "1m"
    assert candle.datetime.tzinfo is not None
```

```python
# tests/unit/test_config.py
from ghost_trader.config import Settings

def test_settings_loads_deriv_symbols():
    settings = Settings.from_file()
    assert settings.deriv.symbols["volatility_75"] == "R_75"
    assert settings.deriv.symbols["boom_1000"] == "BOOM1000"

def test_settings_indicators_present():
    settings = Settings.from_file()
    assert settings.indicators["rsi_period"] == 14
```

```python
# tests/unit/test_data_engine.py
from ghost_trader.data.engine import DataEngine
from ghost_trader.config import Settings
from ghost_trader.connector.models import Tick, TickSource

def test_data_engine_buffer_limit():
    settings = Settings.from_file()
    engine = DataEngine(settings)
    # Agregar más ticks que el límite
    for i in range(settings.data.tick_buffer_size + 100):
        engine.add_tick(Tick(symbol="R_75", price=float(i), timestamp=i, source=TickSource.LIVE))
    df = engine.ticks_to_dataframe()
    assert len(df) == settings.data.tick_buffer_size

def test_data_engine_ticks_filter_by_symbol():
    settings = Settings.from_file()
    engine = DataEngine(settings)
    engine.add_tick(Tick(symbol="R_75", price=1.0, timestamp=0, source=TickSource.LIVE))
    engine.add_tick(Tick(symbol="R_50", price=2.0, timestamp=1, source=TickSource.LIVE))
    ticks = engine.get_ticks(symbol="R_75")
    assert len(ticks) == 1
    assert ticks[0].symbol == "R_75"
```

**Reglas de testing:**
- Cada modelo tiene al menos 1 test
- DataEngine tiene test de buffer límite
- Tests corren sin red (unitarios puros)
- `pytest tests/unit/ -v` debe pasar al 100%
- Los tests de config requieren `config/settings.toml` presente

---

#### 📦 1.7 Dependencias (requirements.txt + pyproject.toml)

**`requirements.txt`:**

```
# Core
polars>=1.0
websockets>=12.0

# Testing
pytest>=8.0
pytest-asyncio>=0.23
```

> **Importante:** Pinear polars (`polars>=1.0`) — su API cambió mucho entre versiones (`.ewm_mean`, `.map_elements`, `.rolling_mean` son de polars 1.x). No usar polars < 1.0.

**`pyproject.toml`:**

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "ghost-trader"
version = "0.1.0"
description = "Trading bot para Deriv API"
requires-python = ">=3.11"
dependencies = [
    "polars>=1.0",
    "websockets>=12.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-asyncio>=0.23",
    "ruff>=0.4",
    "mypy>=1.10",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
```

---

#### 📋 1.8 Checklist de Aprobación FASE 1

Antes de pasar a FASE 2, verificar:

- [ ] Estructura de carpetas creada correctamente
- [ ] `config/settings.toml` con todos los valores configurables
- [ ] `config.py` carga configuración desde TOML (`@dataclass` en todas las configs)
- [ ] `models.py` con Tick y Candle (frozen, type hints, timestamps UTC)
- [ ] `deriv_ws.py` conecta, **autoriza token**, suscribe ticks, reconecta y restaura suscripciones
- [ ] Granularidad convertida a segundos antes de llamar a Deriv
- [ ] `data/engine.py` almacena ticks y velas en Polars
- [ ] Todos los tests pasan (`pytest tests/ -v`)
- [ ] Sin hardcoding — todo configurable desde settings.toml
- [ ] Logging configurado (DEBUG en dev, INFO en prod)
- [ ] README.md con instrucciones de instalación y uso

**Si algún punto falla → NO avanzar a FASE 2.**

---

**Entregable FASE 1:**
- Script que conecta a Deriv, autoriza, obtiene ticks en vivo y los almacena en Polars
- Tests pasando al 100%
- Configuración centralizada y documentada

### FASE 2: Data Engine — Indicadores (Semanas 3-4) ✅ CONSTRUIDA
**Objetivo:** Calcular indicadores técnicos en tiempo real sobre datos de Deriv

```
[Data Store (Polars)] → [Indicator Engine] → [Signal Generator]
```

**Regla de la FASE 2:**
- Cada indicador es una clase independiente
- Todos aceptan DataFrame de Polars como entrada
- Todos retornan Series **o DataFrame** de Polars como salida (según el indicador)
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
    def calculate(self, df: pl.DataFrame) -> pl.DataFrame | pl.Series:
        """
        Calcula el indicador sobre un DataFrame.

        Args:
            df: DataFrame con columnas [open, high, low, close, volume]

        Returns:
            Series o DataFrame con los valores del indicador
        """
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(period={self._period})"
```

**Reglas:**
- Todos los indicadores heredan de BaseIndicator
- `calculate()` acepta DataFrame Polars, retorna Series o DataFrame Polars
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
        """Calcula RSI (0-100). Vectorizado con clip, sin división por cero."""
        delta = df["close"].diff()
        gain = delta.clip(lower_bound=0.0)
        loss = (-delta).clip(lower_bound=0.0)
        avg_gain = gain.rolling_mean(window_size=self._period)
        avg_loss = loss.rolling_mean(window_size=self._period)
        rs = avg_gain / avg_loss
        rsi = 100.0 - (100.0 / (1.0 + rs))
        # 0/0 → NaN → neutral (50); avg_loss=0 → rs=inf → RSI=100
        return rsi.fill_nan(50.0)


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
        """Calcula ATR usando max_horizontal (max elemental entre series)."""
        high = df["high"]
        low = df["low"]
        close_prev = df["close"].shift(1)
        tr1 = high - low
        tr2 = (high - close_prev).abs()
        tr3 = (low - close_prev).abs()
        tr = pl.max_horizontal(tr1, tr2, tr3).fill_null(tr1)
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
        return (
            pl.when(is_doji.fill_nan(False))
            .then(1)
            .otherwise(0)
            .cast(pl.Int8)
        )


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
        return (
            pl.when(bullish)
            .then(1)
            .when(bearish)
            .then(-1)
            .otherwise(0)
            .cast(pl.Int8)
        )
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
            # TODO: Implementar lógica de cruce en FASE 3 (ver EMACross)
            pass
        return SignalType.HOLD
```

> **Nota:** La lógica de cruce de medias (EMA/SMA) se implementa en la estrategia `EMACross` de FASE 3. El `SignalGenerator` queda preparado para reutilizarla.

---

#### 🧪 2.8 Tests de la FASE 2

```python
# tests/unit/test_indicators.py
import polars as pl
from ghost_trader.indicators.trend import SMA, EMA, MACD
from ghost_trader.indicators.momentum import RSI, Stochastic
from ghost_trader.indicators.volatility import BollingerBands, ATR
from ghost_trader.indicators.patterns import Doji, Engulfing


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
        "timestamp": list(range(n)),
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


def test_macd():
    df = create_test_df()
    macd = MACD(fast=12, slow=26, signal=9)
    result = macd.calculate(df)
    assert "macd_line" in result.columns
    assert "signal_line" in result.columns
    assert "histogram" in result.columns


def test_rsi():
    df = create_test_df()
    rsi = RSI(period=14)
    result = rsi.calculate(df)
    assert len(result) == len(df)
    assert result[-1] >= 0 and result[-1] <= 100


def test_rsi_no_losses():
    """RSI = 100 cuando nunca hay pérdidas (sin división por cero)."""
    df = pl.DataFrame({
        "open": [1.0] * 50,
        "high": [1.01] * 50,
        "low": [0.99] * 50,
        "close": [1.0 + i * 0.01 for i in range(50)],
        "volume": [1000] * 50,
        "timestamp": list(range(50)),
    })
    rsi = RSI(period=14)
    result = rsi.calculate(df)
    assert result[-1] == 100.0


def test_stochastic():
    df = create_test_df()
    stoch = Stochastic(k_period=14, d_period=3)
    result = stoch.calculate(df)
    assert "percent_k" in result.columns
    assert "percent_d" in result.columns


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


def test_doji():
    df = create_test_df()
    doji = Doji()
    result = doji.calculate(df)
    assert len(result) == len(df)


def test_engulfing():
    df = create_test_df()
    engulf = Engulfing()
    result = engulf.calculate(df)
    assert len(result) == len(df)
```

---

#### 📋 2.9 Checklist de Aprobación FASE 2

- [ ] Clase BaseIndicator abstracta funcionando
- [ ] SMA, EMA, MACD calculando correctamente
- [ ] RSI, Stochastic calculando correctamente (RSI sin división por cero)
- [ ] BollingerBands, ATR calculando correctamente (ATR con max_horizontal)
- [ ] Patrones Doji y Engulfing detectando correctamente (con pl.when)
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

### FASE 3: Strategy Engine & Backtesting (Semanas 5-6) ✅ CONSTRUIDA
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

    @abstractmethod
    def min_bars(self) -> int:
        """
        Velas mínimas necesarias antes de poder evaluar.
        El backtest usa este valor para saber desde dónde iterar.
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
- `min_bars()` dice al backtest desde qué vela puede evaluar
- Las posiciones se rastrean internamente (para lógica de cierre)
- Sin efectos secundarios en evaluate — solo analiza y propone
- **El timestamp de la propuesta SIEMPRE sale de los datos, nunca de `datetime.now()`**

#### 📈 3.3 Estrategia Piloto: EMA Crossover (strategy/ema_cross.py)

```python
"""Estrategia piloto: EMA Crossover (cruce de medias móviles exponenciales)."""

from datetime import datetime, timezone

import polars as pl
from ghost_trader.strategy.base import Strategy, TradeProposal, TradeAction


def _bar_datetime(df: pl.DataFrame) -> datetime:
    """Timestamp de la última vela como datetime UTC."""
    return datetime.fromtimestamp(df["timestamp"][-1] / 1000, tz=timezone.utc)


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

    def min_bars(self) -> int:
        return self._slow_period + self._confirmation_bars + 1

    def evaluate(self, df: pl.DataFrame, symbol: str) -> TradeProposal:
        """Evalúa cruce de EMAs y retorna propuesta."""
        if len(df) < self.min_bars():
            return TradeProposal(
                action=TradeAction.HOLD,
                symbol=symbol,
                price=df["close"][-1],
                timestamp=_bar_datetime(df),
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
                timestamp=_bar_datetime(df),
                strength=strength,
                reason=f"EMA {self._fast_period} cruza por encima de EMA {self._slow_period}",
                metadata={"ema_fast": current_fast, "ema_slow": current_slow},
            )
        elif crossed_down and self.has_position(symbol):
            return TradeProposal(
                action=TradeAction.CLOSE,
                symbol=symbol,
                price=current_price,
                timestamp=_bar_datetime(df),
                strength=strength,
                reason=f"EMA {self._fast_period} cruza por debajo de EMA {self._slow_period}",
                metadata={"ema_fast": current_fast, "ema_slow": current_slow},
            )
        else:
            return TradeProposal(
                action=TradeAction.HOLD,
                symbol=symbol,
                price=current_price,
                timestamp=_bar_datetime(df),
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

from dataclasses import dataclass
from datetime import datetime, timezone

import polars as pl
from ghost_trader.strategy.base import Strategy, TradeProposal, TradeAction
from ghost_trader.backtest.metrics import calculate_metrics


def _to_dt(timestamp: int) -> datetime:
    """Convierte timestamp en ms a datetime UTC."""
    return datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)


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
        position_notional = 0.0

        min_bars = strategy.min_bars()
        for i in range(min_bars, len(df)):
            # Slice de datos hasta el punto actual (sin lookahead)
            window = df.slice(0, i + 1)
            current_bar = df.row(i, named=True)
            bar_ts = _to_dt(current_bar["timestamp"])

            # Evaluar estrategia
            proposal = strategy.evaluate(window, symbol)

            # Ejecutar propuesta
            if proposal.action == TradeAction.BUY and current_trade is None:
                # Abrir posición LONG (notional fijado al abrir)
                entry_price = current_bar["close"] * (1 + self._slippage_pct)
                position_notional = balance * self._position_size_pct
                commission = position_notional * self._commission_pct

                current_trade = BacktestTrade(
                    entry_time=bar_ts,
                    exit_time=None,
                    symbol=symbol,
                    action="buy",
                    entry_price=entry_price,
                    exit_price=None,
                    pnl=None,
                    reason_entry=proposal.reason,
                    reason_exit=None,
                )
                strategy.open_position(symbol, position_notional)
                balance -= commission  # comisión se descuenta al abrir

            elif proposal.action == TradeAction.CLOSE and current_trade is not None:
                # Cerrar posición
                exit_price = current_bar["close"] * (1 - self._slippage_pct)
                commission = position_notional * self._commission_pct
                pnl_ratio = (exit_price - current_trade.entry_price) / current_trade.entry_price
                pnl_amount = position_notional * pnl_ratio - commission

                current_trade.exit_time = bar_ts
                current_trade.exit_price = exit_price
                current_trade.pnl = pnl_amount
                current_trade.reason_exit = proposal.reason

                trades.append(current_trade)
                balance += position_notional * (1 + pnl_ratio)  # bruto; comisión ya restada en pnl_amount
                equity_curve.append(balance)

                strategy.close_position(symbol)
                current_trade = None
                position_notional = 0.0

        # Cerrar posición abierta al final
        if current_trade is not None:
            last_bar = df.row(-1, named=True)
            bar_ts = _to_dt(last_bar["timestamp"])
            exit_price = last_bar["close"]
            commission = position_notional * self._commission_pct
            pnl_ratio = (exit_price - current_trade.entry_price) / current_trade.entry_price
            pnl_amount = position_notional * pnl_ratio - commission

            current_trade.exit_time = bar_ts
            current_trade.exit_price = exit_price
            current_trade.pnl = pnl_amount
            current_trade.reason_exit = "Fin del backtest"
            trades.append(current_trade)
            balance += position_notional * (1 + pnl_ratio)
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
            start_date=_to_dt(df["timestamp"][0]),
            end_date=_to_dt(df["timestamp"][-1]),
            total_trades=len(trades),
            winning_trades=len(winning),
            losing_trades=len(losing),
            trades=trades,
            equity_curve=equity_curve,
            metrics=metrics,
        )
```

> **Correcciones aplicadas al backtest:**
> - `min_bars` viene de `strategy.min_bars()` (no de parsear strings)
> - Timestamps desde los datos (`_to_dt`), determinista y reproducible
> - Position sizing consistente: notional se fija al abrir y se usa al cerrar
> - Comisión única por lado (al abrir y al cerrar), sin doble cobro

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


def test_ema_cross_hold(uptrend_df):
    """Sin cruce → HOLD."""
    strategy = EMACross(symbols=["R_75"], fast_period=20, slow_period=50)
    proposal = strategy.evaluate(uptrend_df, "R_75")
    assert proposal.action == TradeAction.HOLD


def test_ema_cross_required_indicators():
    strategy = EMACross(symbols=["R_75"], fast_period=20, slow_period=50)
    indicators = strategy.required_indicators()
    assert "EMA_20" in indicators
    assert "EMA_50" in indicators


def test_ema_cross_min_bars():
    strategy = EMACross(symbols=["R_75"], fast_period=20, slow_period=50)
    assert strategy.min_bars() == 52  # slow + confirmation + 1


def test_ema_cross_timestamp_from_data(uptrend_df):
    """El timestamp de la propuesta sale de los datos, no de datetime.now()."""
    strategy = EMACross(symbols=["R_75"], fast_period=20, slow_period=50)
    proposal = strategy.evaluate(uptrend_df, "R_75")
    assert proposal.timestamp == strategy.evaluate(uptrend_df, "R_75").timestamp


# tests/unit/test_backtest.py
import polars as pl
from ghost_trader.backtest.engine import BacktestEngine
from ghost_trader.strategy.ema_cross import EMACross


def test_backtest_runs(uptrend_df):
    """Backtest completa sin errores."""
    strategy = EMACross(symbols=["R_75"], fast_period=10, slow_period=30)
    engine = BacktestEngine(initial_balance=10000.0)
    result = engine.run(strategy, uptrend_df, "R_75")
    assert result.strategy_name == strategy.name
    assert result.symbol == "R_75"
    assert len(result.equity_curve) > 0


def test_backtest_metrics(uptrend_df):
    """Métricas se calculan correctamente."""
    strategy = EMACross(symbols=["R_75"], fast_period=10, slow_period=30)
    engine = BacktestEngine()
    result = engine.run(strategy, uptrend_df, "R_75")
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
        BacktestTrade(datetime(2026,1,1), datetime(2026,1,2), "R_75", "buy", 100, 105, 50, "entry", "exit"),
        BacktestTrade(datetime(2026,1,3), datetime(2026,1,4), "R_75", "buy", 105, 103, -30, "entry", "exit"),
    ]
    equity = [10000, 10050, 10020]
    metrics = calculate_metrics(trades, equity, 10000)
    assert metrics["total_trades"] == 2
    assert metrics["win_rate_pct"] == 50.0
```

> **Nota sobre los tests:** `uptrend_df` es el fixture definido en `tests/conftest.py`. Los `datetime` en `test_metrics_with_trades` son naive (sin tz) — las métricas solo calculan diferencias, así que funcionan; para determinismo total usa UTC.

#### 📋 3.9 Checklist de Aprobación FASE 3

- [ ] Clase abstracta Strategy funcionando (incluye `min_bars()`)
- [ ] EMACross implementada y evaluando correctamente (timestamps desde datos)
- [ ] StrategyRegistry registrando y listando estrategias
- [ ] BacktestEngine simulando vela por vela (sin lookahead, `min_bars` correcto)
- [ ] Métricas calculándose: Sharpe, Sortino, Max DD, Win Rate, Profit Factor
- [ ] Exportación JSON y CSV funcionando
- [ ] Tests unitarios pasando al 100%
- [ ] Comisión y slippage aplicados en cada trade (sin doble cobro de comisión)
- [ ] Position sizing configurable (% del balance, notional fijado al abrir)
- [ ] Documentación de métricas (qué significa cada una)

**Si algún punto falla → NO avanzar a FASE 4.**

**Entregable FASE 3:**
- Estrategia EMACross completa y probada
- Motor de backtesting con datos históricos reales
- Reporte con métricas de rendimiento
- Validación de que la estrategia es rentable en histórico

### FASE 4: Risk Engine & Execution (Semanas 7-8)
**Objetivo:** Validar cada propuesta de trade contra reglas de riesgo antes de ejecutar, y ejecutar órdenes de forma segura vía la API de Deriv.

```
[Trade Proposals] → [Risk Engine] → [Order Executor] → [Deriv API]
                        ↓
                [Portfolio State] + [Execution Log (SQLite)]
```

> **⚠️ Nota de diseño (Deriv):** Deriv API no opera SL/TP tradicional. Ejecuta **contratos**:
> - **Opciones digitales:** `CALL`/`PUT` (Rise/Fall), Touch, etc. — resultado binario al expirar
> - **Multipliers:** `MULTUP`/`MULTDOWN` — apalancamiento con SL/TP **sí soportados**
>
> El **Risk Engine es broker-agnóstico** (valida propuestas). Solo el `DerivExecutor` traduce a contratos.

#### 📁 4.1 Estructura de archivos

```
ghost_trader/
├── risk/
│   ├── __init__.py
│   ├── models.py          # RiskDecision, PortfolioState
│   ├── rules.py           # Reglas: MaxLoss, MaxPositions, MaxPositionSize, TradingHours, CircuitBreaker
│   └── engine.py          # RiskEngine — aplica todas las reglas
├── execution/
│   ├── __init__.py
│   ├── models.py          # Order, OrderType, OrderStatus
│   ├── base.py            # AbstractExecutor (protocolo)
│   ├── deriv_executor.py  # Traduce órdenes a la API de Deriv
│   └── log.py             # Registro de ejecuciones (SQLite)
```

#### ⚙️ 4.2 Configuración (`settings.toml` + `config.py`)

**`config/settings.toml` (secciones nuevas):**

```toml
[risk]
max_daily_loss_pct = 2.0        # Límite de pérdida diaria (% del balance)
max_open_positions = 3          # Máximo de posiciones abiertas simultáneas
max_position_size_pct = 2.0     # Tamaño máximo de posición (% del balance)
require_sl = false              # Exigir stop-loss (solo soportado en Multipliers)
circuit_breaker_loss_streak = 3 # Parar tras N pérdidas consecutivas
cooldown_minutes = 30           # Espera tras disparar un circuit breaker
trading_hours = ["00:00-24:00"] # Horarios permitidos (HH:MM-HH:MM, hora UTC)

[execution]
mode = "paper"                  # paper | demo | live
default_contract_type = "CALL"  # CALL/PUT (Rise/Fall) | MULTUP/MULTDOWN (Multipliers)
duration = 5                    # Duración del contrato
duration_unit = "m"             # t=ticks, s=seg, m=min, h=horas, d=días
currency = "USD"
```

**`ghost_trader/config.py` (clases nuevas):**

```python
@dataclass(frozen=True)
class RiskConfig:
    """Configuración del Risk Engine."""
    max_daily_loss_pct: float = 2.0
    max_open_positions: int = 3
    max_position_size_pct: float = 2.0
    require_sl: bool = False
    circuit_breaker_loss_streak: int = 3
    cooldown_minutes: int = 30
    trading_hours: tuple[str, ...] = ("00:00-24:00",)


@dataclass(frozen=True)
class ExecutionConfig:
    """Configuración de ejecución."""
    mode: str = "paper"  # paper | demo | live
    default_contract_type: str = "CALL"
    duration: int = 5
    duration_unit: str = "m"
    currency: str = "USD"


@dataclass(frozen=True)
class Settings:
    """Settings maestro de Ghost Trader."""
    deriv: DerivConfig
    data: DataConfig
    heartbeat: HeartbeatConfig
    risk: RiskConfig = field(default_factory=RiskConfig)
    execution: ExecutionConfig = field(default_factory=ExecutionConfig)
    indicators: dict[str, object] = field(default_factory=dict)
    strategies: dict[str, object] = field(default_factory=dict)

    @classmethod
    def from_file(cls, path: str = "config/settings.toml") -> "Settings":
        """Carga configuración desde archivo TOML."""
        config_path = Path(path)
        if not config_path.exists():
            raise FileNotFoundError(f"Config no encontrado: {config_path}")
        with open(config_path, "rb") as f:
            raw = tomllib.load(f)
        return cls(
            deriv=DerivConfig(**raw.get("deriv", {})),
            data=DataConfig(**raw.get("data", {})),
            heartbeat=HeartbeatConfig(**raw.get("heartbeat", {})),
            risk=RiskConfig(**raw.get("risk", {})),
            execution=ExecutionConfig(**raw.get("execution", {})),
            indicators=raw.get("indicators", {}),
            strategies=raw.get("strategies", {}),
        )
```

#### 🛡️ 4.3 Modelos de Riesgo (risk/models.py)

```python
"""Modelos del Risk Engine."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class RiskDecision:
    """Decisión del Risk Engine sobre una propuesta."""
    approved: bool
    reasons: tuple[str, ...] = ()   # motivos de rechazo o advertencias
    action: str = "approve"         # approve | reject | pause


@dataclass
class PortfolioState:
    """Estado agregado de la cuenta para evaluar riesgo."""
    balance: float
    equity: float
    daily_start_balance: float
    open_positions: list[dict] = field(default_factory=list)
    consecutive_losses: int = 0
    paused_until: datetime | None = None

    @property
    def daily_pnl_pct(self) -> float:
        """Pérdida/ganancia diaria en % del balance inicial del día."""
        if self.daily_start_balance <= 0:
            return 0.0
        return ((self.balance - self.daily_start_balance) / self.daily_start_balance) * 100
```

#### 📏 4.4 Reglas de Riesgo (risk/rules.py)

```python
"""Reglas de riesgo. Cada regla es independiente y testable."""

from dataclasses import dataclass
from datetime import datetime, timezone

from ghost_trader.risk.models import PortfolioState, RiskDecision
from ghost_trader.strategy.base import TradeProposal


@dataclass(frozen=True)
class RuleResult:
    """Resultado de evaluar una regla."""
    passed: bool
    reason: str = ""


class BaseRule:
    """Base para reglas de riesgo."""

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def evaluate(self, proposal: TradeProposal, portfolio: PortfolioState) -> RuleResult:
        """Evalúa la regla. Devuelve passed=True si la propuesta es aceptable."""
        raise NotImplementedError


class MaxDailyLossRule(BaseRule):
    """Rechaza si la pérdida diaria ya superó el límite configurado."""

    def __init__(self, max_daily_loss_pct: float):
        super().__init__("max_daily_loss")
        self._max_daily_loss_pct = max_daily_loss_pct

    def evaluate(self, proposal, portfolio) -> RuleResult:
        if portfolio.daily_pnl_pct <= -abs(self._max_daily_loss_pct):
            return RuleResult(False, f"Pérdida diaria {portfolio.daily_pnl_pct:.2f}% alcanzó el límite")
        return RuleResult(True)


class MaxPositionsRule(BaseRule):
    """Rechaza si ya hay demasiadas posiciones abiertas."""

    def __init__(self, max_open_positions: int):
        super().__init__("max_positions")
        self._max_open_positions = max_open_positions

    def evaluate(self, proposal, portfolio) -> RuleResult:
        if len(portfolio.open_positions) >= self._max_open_positions:
            return RuleResult(False, f"Ya hay {len(portfolio.open_positions)} posiciones abiertas")
        return RuleResult(True)


class MaxPositionSizeRule(BaseRule):
    """Rechaza si el tamaño de la propuesta supera el % permitido del balance."""

    def __init__(self, max_position_size_pct: float):
        super().__init__("max_position_size")
        self._max_position_size_pct = max_position_size_pct

    def evaluate(self, proposal, portfolio) -> RuleResult:
        max_amount = portfolio.equity * (self._max_position_size_pct / 100.0)
        amount = proposal.metadata.get("amount", 0.0)
        if amount > max_amount:
            return RuleResult(False, f"Tamaño {amount:.2f} supera el máximo {max_amount:.2f}")
        return RuleResult(True)


class TradingHoursRule(BaseRule):
    """Rechaza si la hora actual está fuera de los horarios configurados."""

    def __init__(self, trading_hours: tuple[str, ...], tz=timezone.utc):
        super().__init__("trading_hours")
        self._trading_hours = trading_hours
        self._tz = tz

    def evaluate(self, proposal, portfolio) -> RuleResult:
        now = datetime.now(self._tz).strftime("%H:%M")
        for window in self._trading_hours:
            start, end = window.split("-")
            if start <= now <= end:
                return RuleResult(True)
        return RuleResult(False, f"Hora {now} fuera de los horarios de trading")


class CircuitBreakerRule(BaseRule):
    """Pausa el sistema tras N pérdidas consecutivas (eslabón débil)."""

    def __init__(self, loss_streak: int, cooldown_minutes: int):
        super().__init__("circuit_breaker")
        self._loss_streak = loss_streak
        self._cooldown_minutes = cooldown_minutes

    def evaluate(self, proposal, portfolio) -> RuleResult:
        if portfolio.paused_until and datetime.now(timezone.utc) < portfolio.paused_until:
            return RuleResult(False, f"Sistema en pausa hasta {portfolio.paused_until}")
        if portfolio.consecutive_losses >= self._loss_streak:
            return RuleResult(False, f"{portfolio.consecutive_losses} pérdidas consecutivas → circuit breaker")
        return RuleResult(True)


class RequireSLRule(BaseRule):
    """Exige stop-loss en propuestas de Multipliers si está configurado."""

    def __init__(self, require_sl: bool):
        super().__init__("require_sl")
        self._require_sl = require_sl

    def evaluate(self, proposal, portfolio) -> RuleResult:
        if not self._require_sl:
            return RuleResult(True)
        if proposal.metadata.get("stop_loss") is None:
            return RuleResult(False, "Esta propuesta requiere stop-loss")
        return RuleResult(True)
```

#### 🧠 4.5 Risk Engine (risk/engine.py)

```python
"""Risk Engine — aplica todas las reglas a una propuesta."""

from ghost_trader.risk.models import PortfolioState, RiskDecision
from ghost_trader.risk.rules import BaseRule
from ghost_trader.strategy.base import TradeProposal


class RiskEngine:
    """Valida propuestas contra un conjunto de reglas."""

    def __init__(self, rules: list[BaseRule]):
        self._rules = rules

    def evaluate(
        self, proposal: TradeProposal, portfolio: PortfolioState
    ) -> RiskDecision:
        """Aplica todas las reglas; basta una falla para rechazar."""
        failures: list[str] = []
        for rule in self._rules:
            result = rule.evaluate(proposal, portfolio)
            if not result.passed:
                failures.append(f"{rule.name}: {result.reason}")
        if failures:
            return RiskDecision(approved=False, reasons=tuple(failures), action="reject")
        return RiskDecision(approved=True, reasons=(), action="approve")

    @property
    def rules(self) -> list[BaseRule]:
        return self._rules
```

#### 📦 4.6 Modelos de Ejecución (execution/models.py)

```python
"""Modelos de órdenes de ejecución."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class OrderType(Enum):
    """Tipo de operación sobre un contrato."""
    BUY = "buy"        # abrir contrato (CALL/PUT/Multiplier)
    SELL = "sell"      # cerrar contrato antes de expiración
    CANCEL = "cancel"  # cancelar propuesta pendiente


class OrderStatus(Enum):
    """Ciclo de vida de una orden."""
    PENDING = "pending"
    SUBMITTED = "submitted"
    FILLED = "filled"
    REJECTED = "rejected"
    CANCELLED = "cancelled"
    CLOSED = "closed"


@dataclass
class Order:
    """Orden de ejecución registrada."""
    order_id: str
    symbol: str
    order_type: OrderType
    status: OrderStatus
    amount: float
    created_at: datetime
    metadata: dict = field(default_factory=dict)
    filled_at: datetime | None = None
    filled_price: float | None = None
```

#### 🔌 4.7 Executor (execution/base.py + deriv_executor.py)

```python
# execution/base.py
"""Protocolo del executor de órdenes."""

from typing import Protocol, Any

from ghost_trader.execution.models import Order


class AbstractExecutor(Protocol):
    """Interfaz que todo executor debe implementar."""

    async def buy(self, symbol: str, amount: float, **kwargs) -> Order:
        """Abre un contrato (compra)."""
        ...

    async def sell(self, order_id: str, price: float | None = None) -> Order:
        """Cierra un contrato antes de expiración."""
        ...

    async def cancel(self, order_id: str) -> Order:
        """Cancela una propuesta pendiente."""
        ...
```

```python
# execution/deriv_executor.py
"""Executor específico para Deriv API (traduce a contratos)."""

import uuid
from datetime import datetime, timezone

from ghost_trader.connector.deriv_ws import DerivConnector
from ghost_trader.execution.models import Order, OrderStatus, OrderType


class DerivExecutor:
    """Traduce órdenes genéricas a llamadas de la API de Deriv."""

    def __init__(self, connector: DerivConnector, settings):
        self._connector = connector
        self._settings = settings

    async def buy(self, symbol: str, amount: float, **kwargs) -> Order:
        """Crea una propuesta de contrato y la compra."""
        contract_type = kwargs.get("contract_type", self._settings.execution.default_contract_type)
        order = Order(
            order_id=str(uuid.uuid4()),
            symbol=symbol,
            order_type=OrderType.BUY,
            status=OrderStatus.SUBMITTED,
            amount=amount,
            created_at=datetime.now(timezone.utc),
            metadata=kwargs,
        )

        # 1. Pedir propuesta de contrato
        proposal = await self._connector.request({
            "proposal_open_contract": 1,
            "contract_type": contract_type,
            "symbol": symbol,
            "amount": amount,
            "duration": kwargs.get("duration", self._settings.execution.duration),
            "duration_unit": kwargs.get("duration_unit", self._settings.execution.duration_unit),
            "basis": "stake",
            "currency": self._settings.execution.currency,
            "stop_loss": kwargs.get("stop_loss"),     # solo Multipliers
            "take_profit": kwargs.get("take_profit"),  # solo Multipliers
        })
        if "error" in proposal:
            order.status = OrderStatus.REJECTED
            return order

        proposal_id = proposal["proposal_open_contract"]["id"]

        # 2. Comprar la propuesta
        buy = await self._connector.request({"buy": proposal_id, "price": amount})
        if "error" in buy:
            order.status = OrderStatus.REJECTED
            return order

        order.status = OrderStatus.FILLED
        order.filled_price = float(buy["buy"]["executed_price"])
        order.filled_at = datetime.now(timezone.utc)
        order.metadata["contract_id"] = buy["buy"]["contract_id"]
        return order

    async def sell(self, order_id: str, price: float | None = None) -> Order:
        """Cierra un contrato abierto (sell)."""
        contract_id = ...  # obtenido del Order en el log
        response = await self._connector.request({"sell": contract_id, "price": price})
        return Order(...)

    async def cancel(self, order_id: str) -> Order:
        """Cancela una propuesta pendiente."""
        proposal_id = ...
        response = await self._connector.request({"cancel": proposal_id})
        return Order(...)
```

#### 🗄️ 4.8 Registro de Ejecuciones (execution/log.py)

```python
"""Registro persistente de ejecuciones en SQLite."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from ghost_trader.execution.models import Order


class ExecutionLog:
    """Guarda cada orden ejecutada para auditoría y trazabilidad."""

    def __init__(self, db_path: str = "logs/executions.db"):
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                symbol TEXT NOT NULL,
                order_type TEXT NOT NULL,
                status TEXT NOT NULL,
                amount REAL NOT NULL,
                created_at TEXT NOT NULL,
                filled_price REAL,
                metadata TEXT
            )
            """
        )
        self._conn.commit()

    def record(self, order: Order) -> None:
        """Inserta o actualiza la orden."""
        self._conn.execute(
            """
            INSERT OR REPLACE INTO orders
            (order_id, symbol, order_type, status, amount, created_at, filled_price, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                order.order_id,
                order.symbol,
                order.order_type.value,
                order.status.value,
                order.amount,
                order.created_at.isoformat(),
                order.filled_price,
                str(order.metadata),
            ),
        )
        self._conn.commit()

    def recent(self, limit: int = 20) -> list[Order]:
        """Retorna las últimas N órdenes registradas."""
        rows = self._conn.execute(
            "SELECT order_id, symbol, order_type, status, amount, created_at, filled_price, metadata "
            "FROM orders ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [self._row_to_order(r) for r in rows]

    @staticmethod
    def _row_to_order(row) -> Order:
        return Order(
            order_id=row[0],
            symbol=row[1],
            order_type=OrderType(row[2]),
            status=OrderStatus(row[3]),
            amount=row[4],
            created_at=datetime.fromisoformat(row[5]),
            filled_price=row[6],
            metadata={},
        )

    def close(self) -> None:
        self._conn.close()
```

#### 🧪 4.9 Tests de la FASE 4

```python
# tests/unit/test_risk_rules.py
from datetime import datetime, timezone
from ghost_trader.risk.models import PortfolioState
from ghost_trader.risk.rules import (
    MaxDailyLossRule, MaxPositionsRule, MaxPositionSizeRule,
    TradingHoursRule, CircuitBreakerRule, RequireSLRule,
)
from ghost_trader.strategy.base import TradeProposal, TradeAction

def make_proposal(**meta):
    return TradeProposal(
        action=TradeAction.BUY, symbol="R_75", price=100.0,
        timestamp=datetime.now(timezone.utc), strength=0.5,
        reason="test", metadata=meta,
    )

def test_max_daily_loss_rejects():
    rule = MaxDailyLossRule(max_daily_loss_pct=2.0)
    portfolio = PortfolioState(balance=9500, equity=9500, daily_start_balance=10000)  # -5%
    result = rule.evaluate(make_proposal(), portfolio)
    assert not result.passed

def test_max_daily_loss_passes():
    rule = MaxDailyLossRule(max_daily_loss_pct=2.0)
    portfolio = PortfolioState(balance=9950, equity=9950, daily_start_balance=10000)  # -0.5%
    result = rule.evaluate(make_proposal(), portfolio)
    assert result.passed

def test_max_positions_rejects():
    rule = MaxPositionsRule(max_open_positions=3)
    portfolio = PortfolioState(balance=10000, equity=10000, daily_start_balance=10000,
                               open_positions=[{}, {}, {}])
    assert not rule.evaluate(make_proposal(), portfolio).passed

def test_max_position_size_rejects():
    rule = MaxPositionSizeRule(max_position_size_pct=2.0)
    portfolio = PortfolioState(balance=10000, equity=10000, daily_start_balance=10000)
    # 5% de 10000 = 500 > 200 permitido
    assert not rule.evaluate(make_proposal(amount=500), portfolio).passed

def test_circuit_breaker_pauses():
    rule = CircuitBreakerRule(loss_streak=3, cooldown_minutes=30)
    portfolio = PortfolioState(balance=9000, equity=9000, daily_start_balance=10000,
                               consecutive_losses=3)
    assert not rule.evaluate(make_proposal(), portfolio).passed

def test_require_sl():
    rule = RequireSLRule(require_sl=True)
    portfolio = PortfolioState(balance=10000, equity=10000, daily_start_balance=10000)
    assert not rule.evaluate(make_proposal(), portfolio).passed  # sin stop_loss
    assert rule.evaluate(make_proposal(stop_loss=90), portfolio).passed
```

```python
# tests/unit/test_risk_engine.py
from datetime import datetime, timezone
from ghost_trader.risk.engine import RiskEngine
from ghost_trader.risk.models import PortfolioState
from ghost_trader.risk.rules import MaxPositionsRule, MaxPositionSizeRule
from ghost_trader.strategy.base import TradeProposal, TradeAction

def test_engine_approves_when_all_pass():
    engine = RiskEngine([MaxPositionsRule(3)])
    portfolio = PortfolioState(balance=10000, equity=10000, daily_start_balance=10000)
    proposal = TradeProposal(TradeAction.BUY, "R_75", 100.0, datetime.now(timezone.utc), 0.5, "x")
    decision = engine.evaluate(proposal, portfolio)
    assert decision.approved
    assert decision.action == "approve"

def test_engine_rejects_when_one_fails():
    engine = RiskEngine([MaxPositionsRule(1), MaxPositionSizeRule(2.0)])
    portfolio = PortfolioState(balance=10000, equity=10000, daily_start_balance=10000,
                               open_positions=[{"x": 1}])
    proposal = TradeProposal(TradeAction.BUY, "R_75", 100.0, datetime.now(timezone.utc), 0.5, "x",
                             metadata={"amount": 100})
    decision = engine.evaluate(proposal, portfolio)
    assert not decision.approved
    assert any("max_positions" in r for r in decision.reasons)
```

```python
# tests/unit/test_execution_log.py
import pytest
from ghost_trader.execution.log import ExecutionLog
from ghost_trader.execution.models import Order, OrderStatus, OrderType
from datetime import datetime, timezone

def test_execution_log_roundtrip(tmp_path):
    log = ExecutionLog(str(tmp_path / "test.db"))
    order = Order(
        order_id="abc-123", symbol="R_75", order_type=OrderType.BUY,
        status=OrderStatus.FILLED, amount=10.0,
        created_at=datetime.now(timezone.utc), filled_price=100.0,
    )
    log.record(order)
    recent = log.recent()
    assert len(recent) == 1
    assert recent[0].order_id == "abc-123"
    assert recent[0].status == OrderStatus.FILLED
    log.close()
```

#### 📋 4.10 Checklist de Aprobación FASE 4

- [ ] RiskEngine aplica todas las reglas; una falla → rechazo
- [ ] Reglas: MaxLoss, MaxPositions, MaxPositionSize, TradingHours, CircuitBreaker, RequireSL
- [ ] Circuit breaker detecta pérdidas consecutivas y pausa con cooldown
- [ ] DerivExecutor traduce BUY/SELL/CANCEL a la API (proposal_open_contract → buy)
- [ ] Modo `paper` por defecto — nunca ejecutar real sin autorización explícita
- [ ] ExecutionLog registra cada orden en SQLite (auditoría)
- [ ] Todas las ejecuciones quedan en log
- [ ] Tests unitarios pasando al 100%
- [ ] `settings.toml`: secciones `[risk]` y `[execution]` completas

**Si algún punto falla → NO avanzar a FASE 5.**

**Entregable FASE 4:**
- Risk Engine completo y testeado (reglas independientes)
- Order Executor para Deriv (contratos CALL/PUT/Multipliers)
- Execution Log en SQLite
- Validación de seguridad previa a cualquier ejecución real

### FASE 5: Interfaz & OpenClaw Integration (Semanas 9-10)
**Objetivo:** Control vía Telegram + notificaciones usando OpenClaw como capa de interacción.

```
[User Telegram] → [OpenClaw] → [Ghost Trader API] → [Core]
[Ghost Trader] → [OpenClaw] → [User Telegram]
```

#### 📁 5.1 Estructura de archivos

```
ghost_trader/
├── api/
│   ├── __init__.py
│   ├── server.py           # FastAPI app + montaje de routers
│   ├── dependencies.py     # Estado compartido (DI)
│   └── routes/
│       ├── __init__.py
│       ├── price.py        # GET /price/{symbol}
│       ├── candles.py      # GET /candles/{symbol}
│       ├── indicators.py   # GET /indicator
│       ├── orders.py       # POST /order · GET /orders
│       ├── backtest.py     # POST /backtest
│       └── strategy.py     # POST /strategy/start · /strategy/stop
└── notifications/
    ├── __init__.py
    └── notifier.py         # Envía notificaciones a OpenClaw/Telegram
```

#### ⚙️ 5.2 Configuración (`settings.toml` + `config.py`)

```toml
[api]
host = "127.0.0.1"              # Solo local — OpenClaw accede vía loopback
port = 9001

[notifications]
openclaw_webhook = ""           # URL del skill/endpoint de OpenClaw (opcional)
enabled = true                  # Activar notificaciones
```

```python
@dataclass(frozen=True)
class ApiConfig:
    """Configuración del servidor HTTP."""
    host: str = "127.0.0.1"
    port: int = 9001


@dataclass(frozen=True)
class NotificationsConfig:
    """Configuración de notificaciones."""
    openclaw_webhook: str = ""
    enabled: bool = True
```

> Se añaden `api: ApiConfig` y `notifications: NotificationsConfig` a `Settings` (mismo patrón que FASE 4).

#### 🚀 5.3 Servidor HTTP (api/server.py)

```python
"""Servidor FastAPI de Ghost Trader."""

from fastapi import FastAPI

from ghost_trader.api.routes import price, candles, indicators, orders, backtest, strategy


def create_app() -> FastAPI:
    """Crea la aplicación FastAPI con todos los routers."""
    app = FastAPI(title="Ghost Trader", version="0.3.0")

    app.include_router(price.router)
    app.include_router(candles.router)
    app.include_router(indicators.router)
    app.include_router(orders.router)
    app.include_router(backtest.router)
    app.include_router(strategy.router)

    @app.get("/health")
    async def health():
        """Health check para monitoreo (FASE 6)."""
        return {"status": "ok"}

    return app
```

#### 🔌 5.4 Endpoints (api/routes/)

```python
# api/routes/price.py — "¿A cuánto está R_75?"
"""Ruta de precios en vivo."""

from fastapi import APIRouter, HTTPException

from ghost_trader.api.dependencies import get_engine

router = APIRouter(prefix="/price", tags=["price"])


@router.get("/{symbol}")
async def get_price(symbol: str):
    """Devuelve el último precio conocido de un símbolo."""
    engine = get_engine()
    df = engine.ticks_to_dataframe(symbol=symbol)
    if df.is_empty():
        raise HTTPException(status_code=404, detail=f"Sin datos para {symbol}")
    last = df.row(-1, named=True)
    return {"symbol": symbol, "price": last["price"], "timestamp": last["timestamp"]}
```

```python
# api/routes/candles.py — velas OHLC
@router.get("/{symbol}")
async def get_candles(symbol: str, limit: int = 100):
    engine = get_engine()
    df = engine.get_candles(symbol).tail(limit)
    return df.to_dicts()
```

```python
# api/routes/indicators.py — valores de indicadores
@router.get("/")
async def get_indicator(symbol: str, name: str):
    engine = get_engine()
    df = engine.get_candles(symbol)
    indicator = build_indicators(Settings.from_file()).find(name)  # helper
    ...
    return {"indicator": name, "values": values}
```

```python
# api/routes/orders.py — consultar y enviar órdenes
@router.get("/")
async def list_orders(limit: int = 20):
    return execution_log.recent(limit)

@router.post("/")
async def place_order(payload: dict):
    # 1. Construir propuesta → 2. RiskEngine.evaluate → 3. DerivExecutor.buy
    decision = risk_engine.evaluate(proposal, portfolio)
    if not decision.approved:
        raise HTTPException(status_code=400, detail=decision.reasons)
    order = await executor.buy(payload["symbol"], payload["amount"])
    execution_log.record(order)
    return order
```

```python
# api/routes/backtest.py — correr un backtest y devolver métricas
@router.post("/")
async def run_backtest(payload: dict):
    df = get_candles_from_history(payload["symbol"], payload["granularity"], payload["count"])
    strategy = StrategyRegistry.create(payload["strategy"], symbols=[payload["symbol"]], **payload.get("params", {}))
    engine = BacktestEngine()
    result = engine.run(strategy, df, payload["symbol"])
    return {"summary": result.metrics}
```

```python
# api/routes/strategy.py — control de estrategias
@router.post("/start")
async def start_strategy(payload: dict):
    strategy = StrategyRegistry.create(payload["strategy"], symbols=payload["symbols"])
    scheduler.add(strategy)
    return {"started": strategy.name}

@router.post("/stop")
async def stop_strategy(payload: dict):
    scheduler.remove(payload["strategy"])
    return {"stopped": payload["strategy"]}
```

#### 🔔 5.5 Notificador (notifications/notifier.py)

```python
"""Notificador — envía mensajes a OpenClaw/Telegram."""

import httpx
import logging

logger = logging.getLogger(__name__)


class Notifier:
    """Capa de notificaciones. Envía por webhook cuando está configurado."""

    def __init__(self, settings):
        self._webhook = settings.notifications.openclaw_webhook
        self._enabled = settings.notifications.enabled

    def send(self, topic: str, message: str) -> None:
        """Envía una notificación (trade, alerta, resumen diario)."""
        if not self._enabled:
            return
        logger.info(f"[{topic}] {message}")
        if not self._webhook:
            return
        try:
            httpx.post(self._webhook, json={"topic": topic, "message": message}, timeout=5)
        except Exception as exc:  # noqa: BLE001 — no debe romper el flujo
            logger.error(f"No se pudo notificar: {exc}")
```

**Topics sugeridos:** `trade_filled`, `trade_closed`, `alert`, `daily_summary`, `system`.

#### 🧰 5.6 Skills HTTP para OpenClaw (≤15 líneas)

```yaml
# .opencode/skills/ghost_price.md
# Precio en vivo de un símbolo de Deriv
---
nombre: ghost_price
descripcion: Consulta el último precio de un símbolo
parametros:
  symbol: R_75
---
curl -s "http://127.0.0.1:9001/price/{symbol}"
```

```yaml
# .opencode/skills/ghost_backtest.md
# Ejecuta un backtest y resume métricas
---
nombre: ghost_backtest
descripcion: Backtest de una estrategia sobre un símbolo
parametros:
  strategy: ema_cross
  symbol: R_75
  granularity: 1m
  count: 2000
---
curl -s -X POST "http://127.0.0.1:9001/backtest" \
  -H "Content-Type: application/json" \
  -d "{\"strategy\":\"{strategy}\",\"symbol\":\"{symbol}\",\"granularity\":\"{granularity}\",\"count\":{count}}"
```

> Con estos skills, la pregunta natural del usuario — *"¿Cuántas veces se cruzan SMA 10 y EMA 20?"* — se responde encadenando `/backtest` + análisis en lenguaje natural de las métricas.

#### 🧪 5.7 Tests de la FASE 5

```python
# tests/integration/test_api.py
from fastapi.testclient import TestClient
from ghost_trader.api.server import create_app

client = TestClient(create_app())

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_price_unknown_symbol_404():
    response = client.get("/price/NOEXISTE")
    assert response.status_code == 404
```

#### 📋 5.8 Checklist de Aprobación FASE 5

- [ ] API HTTP en `127.0.0.1:9001` con endpoints: /price, /candles, /indicator, /order, /backtest, /strategy, /health
- [ ] Skills HTTP thin (≤15 líneas) para OpenClaw
- [ ] Notificador envía: cada trade, alertas, resumen diario
- [ ] Control: start/stop estrategias, listar posiciones
- [ ] Orden solo se ejecuta si RiskEngine aprueba
- [ ] Tests de la API pasando
- [ ] `settings.toml`: secciones `[api]` y `[notifications]`

**Si algún punto falla → NO avanzar a FASE 6.**

**Entregable FASE 5:**
- Sistema controlable vía Telegram con notificaciones
- OpenClaw como capa de interacción principal (lenguaje natural)

### FASE 6: Optimización & Production (Semanas 11-12)
**Objetivo:** Hardening, calidad, CI/CD y despliegue en el Ubuntu VPS.

```
[Desarrollo] → [CI (lint+type+test+coverage)] → [Paper trading] → [Production (systemd)]
```

#### 📁 6.1 Estructura de archivos

```
.github/
└── workflows/
    └── ci.yml                  # CI pipeline (GitHub Actions)
deploy/
├── ghost-trader.service        # Unit de systemd
├── deploy.sh                   # Script de despliegue
└── .env.example                # Variables de entorno
scripts/
├── healthcheck.py              # Verificación de salud del servicio
└── daily_summary.py            # Resumen diario (opcional)
```

#### ⚙️ 6.2 Calidad de Código

**`pyproject.toml` (targets definitivos):**

```toml
[tool.coverage.run]
source = ["ghost_trader"]
branch = true

[tool.coverage.report]
fail_under = 80          # Mínimo 80% de cobertura

[tool.mypy]
strict = true
python_version = "3.11"
```

**Comandos de verificación:**

```bash
ruff check ghost_trader tests          # lint
mypy ghost_trader                      # type check
pytest tests/ --cov=ghost_trader --cov-report=term-missing   # tests + coverage
```

#### 🔄 6.3 CI/CD (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -e ".[dev]"
      - run: ruff check ghost_trader tests
      - run: mypy ghost_trader
      - run: pytest tests/ --cov=ghost_trader --cov-report=term-missing
```

#### 🖥️ 6.4 Despliegue (deploy/)

**`deploy/ghost-trader.service` (systemd):**

```ini
[Unit]
Description=Ghost Trader
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/opt/ghost-trader
ExecStart=/opt/ghost-trader/.venv/bin/python -m ghost_trader.main
Restart=always
RestartSec=10
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
```

**`deploy/deploy.sh` (resumen):**

```bash
#!/usr/bin/env bash
set -euo pipefail

APP_DIR=/opt/ghost-trader
git -C "$APP_DIR" pull
cd "$APP_DIR"
python -m venv .venv || true
.venv/bin/pip install -e ".[dev]"
.venv/bin/python -m pytest tests/ -q
sudo systemctl restart ghost-trader
```

#### 🩺 6.5 Monitoreo (scripts/healthcheck.py)

```python
"""Health check del servicio (llamado por systemd/systemd timers o cron)."""

import httpx
import sys

def main() -> int:
    """Comprueba /health y exit code 0 si está sano."""
    try:
        response = httpx.get("http://127.0.0.1:9001/health", timeout=5)
        if response.status_code == 200 and response.json().get("status") == "ok":
            print("OK")
            return 0
    except Exception:  # noqa: BLE001
        pass
    print("FAIL")
    return 1

if __name__ == "__main__":
    sys.exit(main())
```

**Alertas de monitoreo:** el Notifier (FASE 5) se usa para alertar cuando el healthcheck falla o cuando un circuit breaker se dispara.

#### 📅 6.6 Paper Trading Period

- **Duración mínima:** 14 días en modo `paper`
- **Criterios de pase a demo/live:**
  - Cobertura de tests ≥ 80%
  - Backtest de EMACross validado en histórico real
  - Paper trading sin errores de ejecución durante 14 días
  - Risk Engine aprobando/rechazando correctamente
- **Autorización explícita de Mr. Jair** antes de cualquier cuenta real

#### 🧪 6.7 Tests de la FASE 6

```python
# tests/integration/test_healthcheck.py
def test_healthcheck_ok(mocker):
    mocker.patch("httpx.get", return_value=mocker.Mock(status_code=200, json=lambda: {"status": "ok"}))
    from scripts.healthcheck import main
    assert main() == 0
```

#### 📋 6.8 Checklist de Aprobación FASE 6

- [ ] Tests unitarios + integración con ≥ 80% coverage
- [ ] CI/CD pipeline (GitHub Actions) pasando en cada push
- [ ] Ruff + Mypy (strict) + Pytest verdes
- [ ] Documentación completa (README + docs/)
- [ ] Monitoreo: logs, health checks, alertas
- [ ] Paper trading period completado (14 días)
- [ ] Despliegue production (systemd service) funcionando
- [ ] Autorización de Mr. Jair para pasar a demo/live

**Entregable FASE 6:**
- Sistema productivo, testeado, documentado y desplegado en el VPS
- CI/CD garantizando calidad en cada cambio

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
| WebSocket | websockets (público) / aiohttp |
| Datos | Polars ≥ 1.0 (DataFrames) |
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
│   ├── indicators/           # (FASE 2) base, trend, momentum, volatility, volume, patterns
│   ├── signals/              # (FASE 2) generator, models
│   ├── strategy/
│   │   ├── __init__.py
│   │   ├── base.py           # Abstract Strategy class
│   │   ├── ema_cross.py      # EMA Crossover
│   │   └── registry.py       # Strategy registry
│   ├── backtest/
│   │   ├── __init__.py
│   │   ├── engine.py         # Backtest engine
│   │   ├── metrics.py        # Métricas de rendimiento
│   │   └── report.py         # Exportación JSON/CSV
│   ├── risk/                 # (FASE 4) models, rules, engine
│   │   ├── __init__.py
│   │   ├── models.py         # RiskDecision, PortfolioState
│   │   ├── rules.py          # MaxLoss, MaxPositions, CircuitBreaker, ...
│   │   └── engine.py         # Risk Engine
│   ├── execution/            # (FASE 4) models, base, deriv_executor, log
│   │   ├── __init__.py
│   │   ├── models.py         # Order, OrderType, OrderStatus
│   │   ├── base.py           # AbstractExecutor
│   │   ├── deriv_executor.py # Executor Deriv API (contratos)
│   │   └── log.py            # ExecutionLog (SQLite)
│   ├── api/                  # (FASE 5) server + routes
│   │   ├── __init__.py
│   │   ├── server.py         # FastAPI app
│   │   ├── dependencies.py   # Estado compartido (DI)
│   │   └── routes/           # price, candles, indicators, orders, backtest, strategy
│   └── notifications/        # (FASE 5) notifier.py
│       ├── __init__.py
│       └── notifier.py       # Notificaciones a OpenClaw/Telegram
├── tests/
│   ├── unit/
│   ├── integration/
│   └── conftest.py
├── .github/
│   └── workflows/ci.yml      # (FASE 6) CI pipeline
├── deploy/                   # (FASE 6) systemd unit + deploy.sh
├── scripts/                  # (FASE 6) healthcheck, daily_summary
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
6. **Estrategia piloto:** ¿SMA/EMA crossover es aceptable como primera estrategia? *(el plan asume que sí — EMACross en FASE 3)*
7. **Recovery:** ¿Cuál de las 4 estrategias de recovery prefiere para empezar?
8. **Tipo de contrato por defecto (FASE 4):** ¿CALL/PUT (opciones digitales, resultado binario) o MULTUP/MULTDOWN (Multipliers, con SL/TP real)?
9. **Límites de riesgo (FASE 4):** ¿Confirmar `max_daily_loss_pct = 2.0`, `max_open_positions = 3`, `max_position_size_pct = 2.0`, `circuit_breaker_loss_streak = 3`?
10. **Horario de trading (FASE 4):** ¿24/7 (índices sintéticos abren todo el día) o ventanas específicas?
11. **Modo de ejecución (FASE 4):** ¿Empezar en `paper` y pasar a `demo` solo tras aprobar el checklist? ¿Autorización explícita antes de `live`?
12. **Servidor HTTP (FASE 5):** ¿Confirmar `127.0.0.1:9001` (solo local, OpenClaw accede vía loopback) o exponerlo?
13. **VPS (FASE 6):** ¿Seguimos usando el Ubuntu VPS actual para el despliegue systemd?

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
