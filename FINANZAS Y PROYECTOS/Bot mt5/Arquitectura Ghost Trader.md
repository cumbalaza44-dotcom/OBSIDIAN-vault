# 🏗️ Ghost Trader — Arquitectura y Prácticas Profesionales

> **Versión:** 1.0 — 17/05/2026
> **Propósito:** Definir el rumbo del proyecto y cómo lo construiremos como profesionales.

---

## 🎯 Filosofía del proyecto

Ghost Trader es un asistente de trading al que se le habla en lenguaje natural (Telegram) y ejecuta análisis, estrategias y órdenes en Deriv. **Simple, robusto, sin dependencias externas frágiles.**

**Principios rectores:**
1. **Un solo proceso** — Nada de microservicios, orquestadores ni colas de mensajes
2. **Sin vendor lock-in** — LLM intercambiable, broker intercambiable
3. **Datos reales siempre** — Deriv API = ticks reales 24/7, no simulaciones
4. **Seguridad por defecto** — Risk Engine antes de cada orden
5. **Código que dura** — Tipado estático, tests, documentación

---

## 📜 Arquitectura Anterior (v1 — MT5-dependent, para referencia)

```
┌── Windows ──────────────────────────────────┐
│  MT5 Terminal → mt5-bridge-server.py        │
│        ↓ VPN/Tailscale                      │
├──────────────────────────────────────────────┤
┌── Linux VPS ────────────────────────────────┐
│  FastAPI Orchestrator → Gemini → MT5 Bridge │
│  State Manager + Tool Registry (15 tools)   │
└──────────────────────────────────────────────┘
```

**Problemas fatales:**
- Dependía de Windows encendido + VPN + MT5 abierto
- Gemini hardcodeado (sin salida si Google cambia algo)
- Orquestador monolítico de 500 líneas haciendo de todo
- Backend de datos dual: real si MT5 conectado, simulado si no

---

## 🆕 Arquitectura Nueva (v2 — Deriv API nativa)

### Diagrama

```
┌── Linux VPS ───────────────────────────────────────────┐
│                                                         │
│  ghost-trader (1 solo proceso Python service systemd)    │
│                                                         │
│  ┌─ Deriv Connector ─────────────────────────────────┐  │
│  │  WebSocket → wss://ws.derivws.com (persistente)    │  │
│  │  ├── Ticks en vivo (subscribe)                     │  │
│  │  ├── Órdenes (buy/sell)                            │  │
│  │  ├── Cuenta (balance, portfolio, profit_table)     │  │
│  │  └── Histórico (ticks_history)                     │  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─ Data Engine ──────────────────────────────────────┐  │
│  │  Cálculos financieros optimizados con Polars       │  │
│  │  RSI, EMA, SMA, ATR, correlaciones, volatilidad    │  │
│  │  Modo batch (histórico) + streaming (ticks vivos)  │  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─ Backtest Engine ──────────────────────────────────┐  │
│  │  Simulación vela por vela con datos reales          │  │
│  │  Slippage, comisiones, spread variables            │  │
│  │  Métricas: Sharpe, Sortino, Profit Factor, DD      │  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─ Strategy Engine ──────────────────────────────────┐  │
│  │  Estrategias OOP (clase abstracta Strategy)         │  │
│  │  EMACross, RSI, Dynamic (reglas JSON)              │  │
│  │  Evaluación periódica o por tick                    │  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─ Risk Engine ──────────────────────────────────────┐  │
│  │  Reglas de seguridad evaluadas ANTES de cada orden  │  │
│  │  Max daily loss, max positions, require SL, horas   │  │
│  │  Si viola alguna regla → orden rechazada            │  │  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
│  ┌─ HTTP API (localhost:9001) ────────────────────────┐  │
│  │  Endpoints mínimos para que OpenClaw consuma        │  │
│  │  GET /price/{symbol}   GET /indicator/{name}/{sym}  │  │
│  │  GET /candles/{sym}    POST /order                  │  │
│  │  POST /backtest        POST /strategy/{action}      │  │
│  │  GET /positions        GET /account                 │  │
│  └────────────────────────────────────────────────────┘  │
│                                                         │
├──────────────────────────────────────────────────────────┤
│                                                         │
│  OpenClaw (capa de interacción)                          │
│  └── Skills HTTP thin (máx 15 líneas c/u)               │
│  └── Telegram (usted)                                    │
│  └── TaskFlow (estrategias autónomas)                    │
│  └── LLM (DeepSeek → OpenAI → Claude)                 │
│                                                         │
└──────────────────────────────────────────────────────────┘

(Opcional) MT5 en PC solo para MONITOREO visual
```

---

## ✅ Prácticas Profesionales — Cómo lo construiremos

### 1️⃣ Git Workflow

Rama eterna: `main` — siempre estable, siempre pasando tests.

```
main        ●──────●────────────────●────
              \    /                /
feature/      ●──●──●────●──●
                      \
fix/                     ●──●
```

**Reglas:**
- `main` se protege: no se pushea directo. Solo vía PR.
- Ramas con prefijo: `feature/`, `fix/`, `refactor/`, `docs/`
- **Commits con [Conventional Commits](https://www.conventionalomits.org):**
  ```
  feat(core): add RSI indicator calculation
  fix(connector): handle WebSocket reconnection race condition
  docs: add architecture diagram to README
  refactor(data-engine): extract indicator registry
  test(strategy): add backtest for EMA cross
  ```

### 2️⃣ Calidad de código

| Herramienta | Para qué | Se ejecuta en |
|------------|----------|--------------|
| [Ruff](https://docs.astral.sh/ruff/) | Linting + formato | `ruff check . && ruff format .` |
| [Mypy](https://mypy-lang.org/) | Type checking estático | `mypy core/` |
| [Pytest](https://docs.pytest.org/) | Tests unitarios + async | `pytest tests/ -v` |

**El pipeline de calidad (se corre antes de cada PR):**
```bash
ruff check core/          # Sin errores de lint
ruff format core/ --check # Formato correcto
mypy core/                # Tipado correcto
pytest tests/ -v --cov   --cov=core --cov-fail-under=80  # Tests + cobertura mínima 80%
```

### 3️⃣ Testing philosophy

```
tests/
├── unit/              # Tests rápidos, sin red
│   ├── test_data_engine.py
│   ├── test_risk_engine.py
│   └── test_models.py
├── integration/       # Tests con Deriv API real (demo)
│   ├── test_deriv_connector.py
│   └── test_order_execution.py
└── conftest.py        # Fixtures compartidos
```

**Reglas:**
- **Unitarios:** Cada función pública tiene test. Mock de Deriv WebSocket.
- **Integración:** Tests que tocan Deriv demo. Se marcan con `@pytest.mark.integration` y se ejecutan manualmente.
- **Cobertura mínima:** 80% en core.

### 4️⃣ CI/CD Pipeline (GitHub Actions)

En cada push a `main` o PR:

```yaml
name: CI
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: ruff check core/ && ruff format core/ --check
      - run: mypy core/
      - run: pytest tests/
```

### 5️⃣ Documentación

- **Docstrings Google Style** en toda función pública:
  ```python
  def calculate_rsi(prices: list[float], period: int = 14) -> list[float]:
      """Calculate Relative Strength Index using Wilder's Smoothing.
      
      Args:
          prices: List of closing prices.
          period: RSI period for RSI calculation (default 14).
      
      Returns:
          List of RSI values, same length as input with NaN prefix.
      
      Raises:
          ValueError: If prices is empty or period < 2.
      """
  ```
- **README.md**: Qué hace, cómo instalar, cómo usar, arquitectura, contribuir
- **CHANGELOG.md**: Registro de cambios por versión ([Keep a Changelog](https://keepachangelog.com/))
- **Este documento vault**: Sirve como ADR (Architecture Decision Record)

### 6️⃣ Versionado

[SemVer](https://semver.org/):
- **MAJOR**: Cambios que rompen compatibilidad
- **MINOR**: Nuevas funcionalidades (backward compatible)
- **PATCH**: Bug fixes

### 7️⃣ Manejo de errores

```python
class GhostTraderError(Exception):
    """Base exception for all Ghost Trader errors."""

class ConnectionError(GhostTraderError): ...
class OrderRejectedError(GhostTraderError): ...
class RiskViolationError(GhostTraderError): ...
class InvalidSymbolError(GhostTraderError): ...
```

- **Nunca capturar excepciones genéricas** (`except:` sin tipo)
- **Nunca capturar excepciones genéricas** (`except:` sin tipo)
- **Loggear siempre** con contexto: `logger.error("Order failed: symbol=%s, amount=%s", symbol, amount)`
- **Reintentar** solo operaciones idempotentes (lecturas). Órdenes de compra/venta nunca se reintentan automáticamente.

### 8️⃣ Logging y observabilidad

- **Log estructurado:** `{"time": "...", "level": "INFO", "component": "DerivConnector", "msg": "Tick received", "symbol": "frxEURUSD", "bid": 1.0834}`
- **Archivo de log** rotativo (max 10MB, ive (max 1 archivos)- **Healthchecks.io** externo para monitorear que el proceso systemd esté vivo ( o similar)

### 9️⃣ Seguridad

- **Token de Deriv** nunca en el código. Solo en `.env` (`.env` en `.gitignore`)
- **API HTTP API solo en **localhost**, no expuesta al público
- **Sin almacenar** datos sensibles en logs
- **Rate limiting** en las skills de OpenClaw para evitar spam de órdenes

### 🔟 Estructura definitiva del repositorio

```
ghost-trader/
├── core/                    # Código fuente
│   ├── __init__.py          # Versión + docstring del paquete
│   ├── main.py              # Entry point + servidor HTTP
│   ├── deriv_connector.py # WebSocket Deriv
│   ├── data_engine.py       # Indicadores (Polars)
│   ├── backtester.py        # Simulación histórica
│   ├── strategy_engine.py   # Estrategias OOP
│   ├── risk_engine.py       # Reglas de seguridad
│   └── models.py            # Dataclasses + Enums
│
├── tests/                   # Tests
│   ├── conftest.py
│   ├── unit/
│   └── integration/
│
├── openclaw/                # Wrappers para OpenClaw
│   └── skills/
│
├── .github/                 # CI/CD
│   └── workflows/
│       └── ci.yml
│
├── pyproject.toml           # Config de herramientas
├── .gitignore
├── .env.example
├── README.md
├── CHANGELOG.md
├── Makefile                 # Comandos comunes (make lint, make test, make run...)
└── LICENSE
```

---

## 📊 Comparativa v1 vs v2

| Aspecto | v1 (MT5) | v2 (Deriv) | Ganancia |
|---------|----------|------------|----------|
| Plataforma | Windows + Linux | Solo Linux | Sin dependencia externa |
| Datos | Librería MT5 nativa | WebSocket API | Multiplataforma |
| Latencia | VPN + bridge + VPN | Directo VPS → Deriv | -80% |
| Disponibilidad | Depende de PC encendido | 24/7 desde VPS | Siempre vivo |
| Ejecución | order_send() complejo | buy/sell API simple | Menos bugs |
| Backtesting | Simulado o con MT5 | ticks_history real | Datos legítimos |
| LLM | Solo Gemini | Múltiples proveedores | Sin vendor lock-in |
| Código infra | ~2000 líneas en 15 archivos | ~500 líneas en 1 core | -70% |
| Testing | Tests rotos o inexistentes | Cobertura 80%+ obligatoria | Confiable |

---

## ⏭️ Próximos pasos — Plan de construcción

| Paso | Descripción | Tiempo estimado |
|------|-------------|-----------------|
| **1** | Crear repositorio en GitHub + estructura inicial | 15 min |
| **2** | Conexión WebSocket a Deriv Demo | 30 min |
| **3** | Tick en vivo desde Telegram | 30 min |
| **4** | Data Engine + POST /order en demo | 1 hora |
| **5** | Data Engine + Backtest Engine | 2 horas |
| **6** | Risk Engine | 30 min |
| **7** | Strategy Engine + TaskFlow | 1 hora |
| **8** | Refinamiento: logs, errores, tests | 1 hora |

---

*Documento vivo — se actualiza a medida que el proyecto evoluciona el proyecto.*
*Última actualización: 17/05/2026*
