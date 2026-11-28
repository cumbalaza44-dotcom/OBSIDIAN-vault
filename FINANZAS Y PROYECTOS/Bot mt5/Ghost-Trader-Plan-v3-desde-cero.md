# 👻 Ghost Trader v3 — Plan de Construcción desde Cero

> Fecha: 28/11/2026 · Estado: arquitectura · Base: Deriv API v1 + MCP

## 🎯 Objetivo

Sistema funcional de trading algorítmico: Python 24/7 → Deriv API directa → control Telegram. Demo primero, real después.

## 📐 Principios

1. **API = manos, MCP = ojos.** El bot corre solo con API. El MCP solo se usa al programar y mantener.
2. **Demo hasta probar.** Nada real sin Sharpe >1 + 200 trades demo.
3. **Risk primero.** Ninguna orden sin pasar por Risk Engine. Sin bypass.
4. **Campo nuevo.** Símbolo = `underlying_symbol` (API v1). Código viejo con `symbol` se actualiza.

## 🏗️ Arquitectura

```
Deriv WS público (ticks/velas, sin auth)
   → Deriv Connector (OTP + Bearer, auto-reconnect, ping 30s, req_id)
   → Data Engine (Polars: ticks → velas → RSI/EMA/ATR)
   → Strategy Engine (EMA Cross, RSI Reversal → OrderSignal)
   → Risk Engine (pérdida diaria -2%, máx 3 posiciones, horario 08-20 UTC)
   → Deriv Connector (proposal → buy)
   → Log + Telegram (vía OpenClaw)
```

### Capas

| Capa | Archivo | Responsabilidad |
|------|---------|-----------------|
| Conector | `deriv_connector.py` | WS público/demo/real, OTP, reconnect, ping, forget |
| Datos | `data_engine.py` | Buffer ticks → velas OHLC, indicadores Polars |
| Estrategia | `strategy_engine.py` | Clases Strategy → OrderSignal, min_bars propio |
| Riesgo | `risk_engine.py` | Único aprobador, sin bypass |
| Backtest | `backtester.py` | Sharpe, Sortino, Profit Factor, Max DD |
| Modelos | `models.py` | Dataclasses config |
| API local | puerto 9001 | price, indicators, candles, order, positions, account |
| MCP dev | Deriv AI Hub | Schemas vivos al programar, no en runtime |

## 🔑 Auth flow (API v1)

1. OAuth2 + PKCE → access token
2. `GET /trading/v1/options/accounts` → IDs
3. `POST .../accounts/{id}/otp` → URL WS demo/real
4. Conectar y mandar `proposal` (subscribe) → `buy` con ID

## 📅 Fases

### FASE 1 — Conector + Data (semana 1) — 🟡 en curso
> Resuelve: interpretación — ver el mercado sin estar pegado.
- [x] `deriv_connector.py`: WS público v1 (velas + ticks push), ping 30s, reconnect, req_id, resubscribe
- [x] Test: 500 velas R_100 + EMA/RSI/ATR validados (`scripts/phase1_smoke.py`)
- [ ] OTP demo/real (requiere PAT + account_id) + `balance` / `portfolio`
- [ ] `data_engine.py`: buffer de ticks → velas en vivo + indicadores (pandas)
- [ ] Validar schemas contra MCP Deriv (schemas oficiales ya consultados)
- [ ] Pipeline base con pasos obligatorios (ningún dato salta de capa)

### FASE 2 — Estrategia + Risk (semana 2)
> Resuelve: lenguaje → reglas + gestión con criterio. Núcleo iterativo.
- [ ] `strategy_engine.py`: EMACross + RSIReversal, timestamp de vela
- [ ] Lenguaje natural → regla: parser de instrucciones habladas a parámetros de estrategia
- [ ] `risk_engine.py`: -2% diario, máx 3, horario, margen — único aprobador, sin bypass
- [ ] Pipeline de ejecución con pasos verificados (propuesta → validación risk → buy)
- [ ] `backtester.py`: sizing consistente, comisión sin doble cobro
- [ ] Test: backtest 1 año R_75, métricas completas

### FASE 3 — Ejecución demo (semana 3)
> Resuelve: ejecución autónoma + criterio de cierre. Taller iterativo vivo.
- [ ] `proposal` → `buy` en demo, `sell`/`portfolio`/`statement`
- [ ] Regla de cierre: cuándo cerrar (TP/SL/tiempo/indicador) como parte de la estrategia
- [ ] Ciclo iterativo: hablar → regla → backtest → ajuste → demo, todo por Telegram
- [ ] API local :9001 + Telegram vía OpenClaw
- [ ] 200 trades demo, Sharpe >1 para pasar a real
- [ ] Bitácora de conocimiento: cada iteración guarda qué se aprendió
- [ ] Tests 80%+, CI básico

### FASE 4 — Real micro (semana 4+)
> Resuelve: consistencia con poco. Sistema maduro y estable.
- [ ] Capital $2 USD, micro lots, mismos límites risk
- [ ] Monitoreo Telegram + log completo
- [ ] Revisión semanal de bitácora: conocimiento acumulado → reglas más maduras
- [ ] Modelo JEV (Buy/Sell/Hold 70-300ms) como señal extra — solo si FASE 3 verde

## 🗂️ Mapa de archivos

```
ghost-trader/
├── core/main.py
├── deriv_connector.py
├── data_engine.py
├── strategy_engine.py
├── risk_engine.py
├── backtester.py
├── models.py
├── settings.toml
├── requirements.txt (polars pineado)
├── pyproject.toml
├── tests/ + conftest.py
└── openclaw/skills/
```

## ⚠️ Decisiones tomadas (28/11)

- API v1 + `underlying_symbol` (no `symbol` viejo)
- MCP solo en dev/mantenimiento, nunca en runtime
- Sintéticos primero (R_75, R_100, Boom/Crash), Forex/Multipliers después
- Demo → real solo con métricas verdes

## 🎤 Entrevista 28/11 — visión del sistema

**1. Problema que resuelve — TIEMPO en 3 frentes:**
- Interpretación: detectar patrones con indicadores sin estar pegado a pantalla
- Ejecución: lenguaje natural → reglas claras de operación
- Gestión: criterio de dirección de apertura y momento de cierre, sin emoción

**2. Usuario — solo personal.** Herramienta propia, no producto. Sin UI pública ni multiusuario.

**3. Diferencia — versátil e iterativo.** No estrategia fija: taller para probar ideas hablándolas, convertir en regla, backtestear, ajustar, repetir.

**4. Visión 1 año — maduro, estable, consistente aunque sea con poco.** Sistema con conocimiento acumulado, no pelotazo.

**5. Innegociable — nunca saltarse normas de seguridad ni pasos de ejecución.** Pipeline obligatorio, sin bypass. Risk Engine como único aprobador.

## ✅ Estado real del repositorio (28/11, verificado)

### Lo que ya existe y funciona (prototipo v2)
- `src/data/deriv_client.py`: cliente WS legacy con failover y sondeo.
- `src/data/indicators.py`: EMA, RSI, MACD, ATR, ADX, Bollinger, estocástico (pandas).
- `src/ai/`: 29 features, `HistGradientBoostingClassifier`, agente, estrategia de reglas.
- `src/trading/`: `PaperBroker` + `RiskManager` + persistencia (`state.json`, `trades.jsonl`).
- `src/backtest/backtester.py`, `train.py`, `backtest.py`, `main.py`, dashboard Streamlit.
- Modelo entrenado: `data/models/model_R_75_60.joblib`.

### Nuevo (v3) construido hoy
- `src/data/deriv_connector.py`: conector **Options API v1** (REST + WS público/cuenta, OTP, `req_id`, ping 30 s, backoff, resubscribe automático).
- `scripts/phase1_smoke.py`: **FASE 1 verde** → 500 velas R_100 en 0.29 s, 5 ticks por push, EMA/RSI/ATR válidos.

### API v1 verificada (no asumida)

| Pieza | Valor real |
|---|---|
| REST base | `https://api.derivws.com` |
| Cuentas | `GET /trading/v1/options/accounts` |
| OTP | `POST /trading/v1/options/accounts/{id}/otp` → `data.url` (120 s, un solo uso) |
| WS público | `wss://api.derivws.com/trading/v1/options/ws/public` |
| WS demo/real | la URL que devuelve el OTP |
| Auth | `Authorization: Bearer`; PAT exige header `Deriv-App-ID` |
| Campo símbolo | `underlying_symbol` (nunca `symbol`) |
| Cuenta (schema) | `account_id`, `balance`, `currency`, `group`, `status`, `account_type` |
| Símbolos activos | 95; sintéticos R_10/25/50/75/100 + 1HZ* disponibles |

### Mecánica real de R_100 (medida hoy)
- CALL/PUT (RISE/FALL) 5 ticks, stake 10 USD → **payout 19.54**.
- Ganar: **+9.54**; perder: **−10.00**. **Break-even ≈ 51.2%** de aciertos.
- Stake mínimo 0.35 USD; payout máximo 1000 USD.
- Duraciones: tick (1–10 t), intradía (15 s–1 d), diario (1–365 d).
- MULTUP/MULTDOWN existen, pero no devolvieron propuesta con los parámetros probados.

### ⚠️ Hallazgos que cambian el diseño
1. **Riesgo binario mal modelado en v2.** `RiskManager.stake_size()` dimensiona por distancia entry→SL (lógica CFD). En binarios se pierde **todo el stake**. Con balance 1000 y tope 5%, un stop de 1 ATR produjo stake 50 → primera pérdida = −5% = límite diario. El `state.json` actual está detenido exactamente por eso (modo offline). En v3: `stake = balance × risk_per_trade` (2%), con tope absoluto, sin distancia.
2. **TP/SL de precio no existen en CALL/PUT binario.** El contrato liquida en expiry (o se vende antes al bid). El `PaperBroker` actual cierra por precio y marca PnL no realizado, lo que no representa a Deriv. v3 debe simular **liquidación por expiry**: `win = close_expiry > entry` (CALL); PnL = `payout − stake` o `−stake`.
3. **El label del ML no coincide con el horizonte del contrato.** `make_labels(horizon=1)` predice la siguiente vela; un contrato de 5 ticks o 1 minuto necesita `horizon` = duración. Alinear label ↔ expiry antes de backtestear.
4. **Backtest no representativo.** Usa TP/SL y no payout/expiry reales. Debe reescribirse sobre la mecánica binaria y usar el payout real de `proposal`.
5. **Polars vs pandas.** El plan pide Polars; el código funciona con pandas. Para 500–5000 velas no hay ganancia medible. Recomendación: mantener pandas en v3 y migrar solo si el volumen lo exige.

## 🧭 Decisiones abiertas (bloquean Fase 2/3)

- [ ] **Estructura:** ¿reescribir en la estructura plana del plan o evolucionar `src/` reutilizando datos/ML/backtest? → Recomendado: evolucionar `src/`.
- [ ] **Contrato v3:** ¿CALL/PUT binario (coherente con RISE/FALL y $2) o MULTUP/MULTDOWN (TP/SL nativo)? → Recomendado: CALL/PUT.
- [ ] **Auth inicial:** ¿PAT (desktop, simple) u OAuth2 PKCE? → Recomendado: PAT ahora, OAuth después.
- [ ] **Duración base:** ¿5 ticks, 1 min o 5 min? Afecta label, backtest y frecuencia.

## ⏭️ Siguiente acción

1. [x] FASE 1: conector público + 500 velas R_100
2. [ ] Cerrar decisiones abiertas (estructura, contrato, auth, duración)
3. [ ] `data_engine.py`: ticks → velas en vivo + indicadores, con buffer y tests
4. [ ] Conectar cuenta demo vía PAT + OTP y leer `balance` / `portfolio`
5. [ ] Reescribir `risk_engine.py` y `backtester.py` con mecánica binaria real (stake, payout, expiry)
