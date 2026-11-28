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

### FASE 1 — Conector + Data (semana 1)
> Resuelve: interpretación — ver el mercado sin estar pegado.
- [ ] `deriv_connector.py`: público (ticks) + OTP demo, ping, reconnect, req_id
- [ ] `data_engine.py`: ticks_history → velas, RSI/EMA/ATR en Polars
- [ ] Test: 500 velas R_100 en demo, indicadores calculados
- [ ] Validar schemas contra MCP Deriv
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

## ⏭️ Siguiente acción

- [ ] FASE 1: conector público + 500 velas R_100
