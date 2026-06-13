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
**Objetivo:** Obtener ticks en vivo y histórico

```
[Deriv WebSocket] → [Deriv Connector] → [Data Store]
```

- [ ] Scaffold del proyecto (estructura de carpetas)
- [ ] Deriv Connector: conexión WebSocket persistente
- [ ] Suscripción a ticks en vivo (múltiples símbolos)
- [ ] Obtención de histórico (ticks_history)
- [ ] Almacenamiento en Polars DataFrame
- [ ] Reconexión automática + heartbeat

**Entregable:** Script que conecta a Deriv, obtiene ticks y los almacena.

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
