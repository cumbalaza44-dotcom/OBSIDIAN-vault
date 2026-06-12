# 🏗️ Plan de Construcción — Ghost Trader

> **Versión:** 2.0 — 11/06/2026
> **Propósito:** Hoja de ruta para construir el asistente de trading en lenguaje natural, desglosado por módulos
> **Basado en:** Arquitectura v2 — Deriv API nativa

---

## 🧱 MÓDULOS DEL SISTEMA

```mermaid
flowchart TB
    subgraph DERIV[Mundo Exterior]
        A[Deriv API<br>ws.derivws.com]
    end

    subgraph GT[Ghost Trader — 1 Proceso Python]
        direction TB
        
        subgraph M1[📦 M1 — Deriv Connector]
            M1_WS[WebSocket persistente]
            M1_TICK[TickEvent]
            M1_ORDEN[Orden buy/sell]
        end

        subgraph M2[📦 M2 — Data Engine]
            M2_BUF[Buffer de ticks]
            M2_VELA[Agrupación → Velas]
            M2_IND[Indicadores<br>RSI · EMA · SMA · ATR · Vol]
        end

        subgraph M3[📦 M3 — Backtest Engine]
            M3_HIST[Datos históricos<br>ticks_history]
            M3_SIM[Simulación vela x vela]
            M3_MET[Métricas<br>Sharpe · Sortino · DD · PF]
        end

        subgraph M4[📦 M4 — Strategy Engine]
            M4_ABS[Clase abstracta Strategy]
            M4_EMA[EMACross]
            M4_RSI[RSIStrategy]
            M4_DYN[Dynamic JSON]
            M4_SIG[OrderSignal]
        end

        subgraph M5[📦 M5 — Risk Engine]
            M5_R1[🔴 Max pérdida diaria -2%]
            M5_R2[🔴 Max posiciones 3]
            M5_R3[🔴 Stop Loss obligatorio]
            M5_R4[🟡 Horario 08-20 UTC]
            M5_R5[🔴 Margen suficiente]
            M5_OK[✅ ApprovedOrder]
        end

        subgraph M6[📦 M6 — HTTP API :9001]
            M6_PRICE[GET /price/{symbol}]
            M6_IND[GET /indicator/{name}]
            M6_CAND[GET /candles/{symbol}]
            M6_ORDER[POST /order]
            M6_POS[GET /positions]
            M6_ACC[GET /account]
            M6_BT[POST /backtest]
        end
    end

    subgraph OPENCLAW[Capa de Interacción — OpenClaw]
        TG[💬 Telegram]
        LLM[🧠 LLM<br>DeepSeek → OpenAI → Claude]
        TF[⚙️ TaskFlow<br>Estrategias autónomas]
        SK[🔌 Skills HTTP thin]
    end

    %% Conexiones del flujo de datos
    A <-->|WebSocket SSL| M1_WS
    M1_WS -->|TickEvent| M2_BUF
    M2_BUF --> M2_VELA --> M2_IND
    M2_IND -->|IndicatorSnapshot| M4_ABS
    M4_ABS --> M4_EMA & M4_RSI & M4_DYN
    M4_EMA & M4_RSI & M4_DYN -->|OrderSignal| M5_R1
    M5_R1 --> M5_R2 --> M5_R3 --> M5_R4 --> M5_R5
    M5_R5 -->|Si todo OK| M5_OK
    M5_OK -->|ApprovedOrder| M1_ORDEN
    M1_ORDEN -->|buy/sell JSON-RPC| A
    M1_WS -.->|Datos históricos| M3_HIST
    M3_HIST --> M3_SIM --> M3_MET
    M3_MET -.->|Feedback| M4_ABS

    %% HTTP API conecciones
    M1_WS -.->|Precio en vivo| M6_PRICE
    M2_IND -.->|Indicadores| M6_IND
    M2_VELA -.->|Velas| M6_CAND
    M5_OK -.->|Orden aprobada| M6_ORDER
    M1_ORDEN -.->|Posiciones abiertas| M6_POS

    %% OpenClaw conecciones
    TG -->|"compra 10 EURUSD"| LLM
    LLM -->|OrderSignal| M5_R1
    LLM -.->|Consulta de datos| SK
    SK <--> M6_PRICE & M6_IND & M6_ORDER & M6_POS
    TF -.->|Estrategia automática| M4_ABS

    %% Estilos
    classDef danger fill:#ff4444,color:#fff
    classDef ok fill:#00C853,color:#fff
    classDef warning fill:#FFC107,color:#000
    classDef module fill:#1a1a2e,stroke:#e94560,color:#eee
    classDef openclaw fill:#16213e,stroke:#0f3460,color:#eee
    class M5_R1,M5_R2,M5_R3,M5_R5 danger
    class M5_OK ok
    class M5_R4 warning
    class M1,M2,M3,M4,M5,M6 module
    class TG,LLM,TF,SK openclaw
```

### Leyenda del Diagrama

| Símbolo | Significado |
|---------|------------|
| ➡️ Flecha sólida | Flujo principal de datos (tick → orden) |
| ┄ ➡️ Flecha punteada | Flujo secundario / consulta |
| 🔴 Rojo | Regla crítica de seguridad |
| 🟢 Verde | Punto de aprobación |
| 🟡 Amarillo | Regla opcional / informativa |

### Pipeline de Datos — Tick a Orden (Tiempos Estimados)

```mermaid
flowchart LR
    TICK["Tick<br>📡"] -->|"&lt;1ms"| CON["Parseo<br>Connector"]
    CON -->|"~5ms"| DE["Cálculo<br>Data Engine"]
    DE -->|"&lt;1ms"| SE["Evaluación<br>Strategy Engine"]
    SE -->|"&lt;1ms"| RE["Filtro<br>Risk Engine"]
    RE -->|"~50ms"| ORD["Ejecución<br>Deriv API"]
    
    style TICK fill:#4a148c,color:#fff
    style CON fill:#1a237e,color:#fff
    style DE fill:#004d40,color:#fff
    style SE fill:#e65100,color:#fff
    style RE fill:#b71c1c,color:#fff
    style ORD fill:#1b5e20,color:#fff
```

**Latencia total estimada Tick → Orden:** ~60ms
```

---

## 📦 Módulo 1 — Deriv Connector

**Función:** Puente único entre Deriv y el sistema. WebSocket persistente.

### Necesidad del Operador
> "Necesito que el sistema hable con Deriv en tiempo real, reciba ticks, balance y ejecute órdenes sin que yo tenga que tocar código cada vez que cambie algo."

### Solución que Ofrece
| Sub-componente | Solución | Estado | Prioridad |
|---------------|----------|--------|-----------|
| Conexión WebSocket a Deriv Demo | Conecta y autentica con Deriv API sin intervención manual | ⏳ | 🔴 |
| Suscripción a ticks (1RDN8Z3) | Recibe precio en vivo de índices sintéticos 24/7 | ⏳ | 🔴 |
| Suscripción a balance/profit | Sabe cuánto dinero hay y cómo van las operaciones | ⏳ | 🔴 |
| Dataclasses internas (models.py) | Traduce el JSON de Deriv a objetos Python que el resto del sistema entiende | ⏳ | 🔴 |
| Auto-reconnect (backoff exponencial) | Si se cae la conexión, se reconecta solo — sin que usted tenga que reiniciar nada | ⏳ | 🟡 |
| Parseo de mensajes JSON-RPC | Cada tick, orden o actualización se convierte en un evento usable | ⏳ | 🔴 |

**Dependencias:** `websockets`, `orjson`
**El operador gana:** No tocar Deriv manualmente. El sistema lo maneja.

---

## 📦 Módulo 2 — Data Engine

**Función:** Convierte ticks en velas y calcula indicadores. Corazón analítico.

### Necesidad del Operador
> "Necesito que los ticks sueltos se conviertan en velas OHLC de diferentes temporalidades (1m, 5m, 15m), se mantengan agrupadas y actualizadas en vivo, y de ahí se calculen indicadores sin que yo tenga que pedirlos uno por uno."

**Lo que ya definimos en sesiones anteriores (18/05):**

```
Buffer de ticks → Agrupación por intervalo (1m, 5m) → Candle →
    ├── RSI(14): Wilder's Smoothing
    ├── EMA(12): Exponential Moving Average
    ├── SMA(50): Simple Moving Average
    ├── ATR(14): Average True Range
    └── Volatilidad: Desviación estándar de retornos
```

### Solución que Ofrece — Dos Modos de Operación

**Modo Batch** — Al cargar el sistema:
1. Pide 500 velas históricas a Deriv (ticks_history)
2. Procesa todo con Polars (vectorizado, milisegundos)
3. Calcula indicadores desde el inicio
4. Entrega un snapshot completo al Strategy Engine

**Modo Streaming** — En vivo, por cada tick:
1. Acumula tick en buffer circular (en RAM, sin disco)
2. Cuando completa una vela (ej. pasó 1 minuto):
   - Cierra la vela anterior
   - Abre una nueva
   - Recalcula SOLO el indicador que cambió (no todo)
3. Mantiene N velas en memoria (configurable: 100, 500, 1000)
4. Velas viejas se persisten a SQLite/Parquet para consultas históricas

### Estructura de datos en memoria:

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
```

### Pipeline completo de tick a indicador:

```mermaid
flowchart LR
    RAW["Tick crudo<br>JSON-RPC"] -->|"&lt;1ms"| PARSE["Parseo<br>→ TickEvent"]
    PARSE -->|"O(1)"| BUF["Buffer<br>circular"]
    BUF -->|¿Vela completa?| VELA["❌ No → esperar<br>✅ Sí → Cerrar vela"]
    VELA -->|Candle nuevo| IND["Recalcular<br>indicador"]
    IND -->|IndicatorSnapshot| SNAP["Entregar a<br>Strategy Engine"]
    
    style RAW fill:#4a148c,color:#fff
    style PARSE fill:#1a237e,color:#fff
    style BUF fill:#004d40,color:#fff
    style VELA fill:#e65100,color:#fff
    style IND fill:#01579b,color:#fff
    style SNAP fill:#1b5e20,color:#fff
```

**El operador gana:** Datos listos para estrategias sin preocuparse por la matemática. Pide un indicador y ya está calculado.

---

## 📦 Módulo 3 — Backtest Engine

**Función:** Simulación vela por vela con datos reales Deriv para probar estrategias antes de arriesgar capital.

### Necesidad del Operador
> "Necesito saber si una estrategia funciona ANTES de poner dinero real. Quiero simularla con datos históricos reales y ver métricas de rendimiento."

### Solución que Ofrece
| Sub-componente | Solución | Estado | Prioridad |
|---------------|----------|--------|-----------|
| Obtener ticks_history de Deriv | Toma datos reales del broker, no simulaciones inventadas | ⏳ | 🔴 |
| Simulación vela por vela | Reconstruye cada vela como si el tiempo hubiera pasado en vivo | ⏳ | 🔴 |
| Slippage + comisiones | Refleja el costo real de operar (no fantasía) | ⏳ | 🟡 |
| Spread variable | Simula el diferencial real del mercado en cada momento | ⏳ | 🟡 |
| Métricas: Sharpe, Sortino, PF, DD | Números objetivos para decidir si la estrategia sirve | ⏳ | 🟡 |

**Dependencias:** Módulo 2 (Data Engine)
**El operador gana:** Validación objetiva antes de arriesgar capital.

---

## 📦 Módulo 4 — Strategy Engine

**Función:** Estrategias OOP. Evalúa reglas y genera señales de compra/venta.

### Necesidad del Operador
> "Necesito definir reglas de trading que el sistema evalúe automáticamente en cada tick o vela, sin que yo esté pegado a la pantalla."

### Solución que Ofrece
| Sub-componente | Solución | Estado | Prioridad |
|---------------|----------|--------|-----------|
| Clase abstracta Strategy | Cualquier estrategia nueva se escribe heredando de una clase base — estructura predecible | ⏳ | 🔴 |
| EMACross | Dispara orden cuando EMA(12) cruza SMA(50) | ⏳ | 🔴 |
| RSIStrategy | Compra si RSI < 30, vende si RSI > 70 | ⏳ | 🟡 |
| Dynamic JSON | Permite cambiar reglas sin modificar código (solo editar un JSON) | ⏳ | 🟡 |
| Evaluación O(1) por tick | Cada tick se evalúa en tiempo constante — no se acumula latencia | ⏳ | 🔴 |

**Dependencias:** Módulo 2 (IndicatorSnapshot)
**El operador gana:** Estrategias automáticas que operan 24/7 sin supervisión constante.

---

## 📦 Módulo 5 — Risk Engine

**Función:** Último filtro de seguridad. NO HAY BYPASS.

### Necesidad del Operador
> "Necesito estar seguro de que el sistema no va a arriesgar más de lo debido, incluso si yo mismo pido una orden arriesgada o si la estrategia automática se desvía."

### Solución que Ofrece
| Regla | Solución | Estado | Prioridad |
|-------|----------|--------|-----------|
| Máx pérdida diaria (-2%) | Si hoy ya perdió el 2% del balance, no se ejecutan más órdenes hasta mañana | ⏳ | 🔴 |
| Máx posiciones abiertas (3) | No permite tener más de 3 operaciones abiertas simultáneas | ⏳ | 🔴 |
| Stop Loss obligatorio | Toda orden DEBE tener un SL definido. Sin SL = orden rechazada | ⏳ | 🔴 |
| Horario permitido (08-20 UTC) | Solo opera en horas de mercado activo | ⏳ | 🟡 |
| Margen suficiente | Verifica que hay saldo disponible antes de cada orden | ⏳ | 🔴 |
| Short-circuit | Si UNA regla falla, la orden se rechaza al instante (no evalúa las siguientes) | ⏳ | 🟡 |

**Regla de oro:** Risk Engine aplica a TODAS las órdenes — automáticas, manuales y por LLM.
**El operador gana:** Dormir tranquilo sabiendo que el sistema no se va a autodestruir.

---

## 📦 Módulo 6 — HTTP API (localhost:9001)

**Función:** Endpoints para que OpenClaw consuma datos y ejecute órdenes.

### Necesidad del Operador
> "Necesito que H.E.L.E.N. pueda preguntarle al sistema el precio actual, los indicadores, mis posiciones y ejecutar órdenes sin tener que abrir Deriv."

### Solución que Ofrece
| Endpoint | Solución | Estado | Prioridad |
|----------|----------|--------|-----------|
| GET /price/{symbol} | "Señor, el EURUSD está a 1.0834" | ⏳ | 🔴 |
| GET /indicator/{name}/{symbol} | "El RSI(14) está en 62.3" | ⏳ | 🟡 |
| GET /candles/{symbol} | "Aquí tiene las últimas 20 velas" | ⏳ | 🟡 |
| POST /order | "Compro 10 EURUSD" → Risk Engine → Deriv | ⏳ | 🔴 |
| POST /backtest | Ejecuta backtest de una estrategia y devuelve métricas | ⏳ | 🟡 |
| POST /strategy/{action} | Activar/desactivar estrategia, cambiar parámetros | ⏳ | 🟡 |
| GET /positions | "Tiene 1 posición abierta" | ⏳ | 🟡 |
| GET /account | "Balance: $1,234.56" | ⏳ | 🔴 |

**Dependencias:** Flask/FastAPI (liviano)
**El operador gana:** Interactuar con Ghost Trader desde Telegram como si estuviera hablando con un broker.

---

## 📦 Módulo 7 — OpenClaw (Capa de Interacción)

**Función:** Interface con usted vía Telegram + LLM.

### Necesidad del Operador
> "Necesito que todo esto funcione desde mi chat de Telegram, en lenguaje natural, sin abrir terminales ni recordar comandos."

### Solución que Ofrece
| Sub-componente | Solución | Estado | Prioridad |
|---------------|----------|--------|-----------|
| Skills HTTP thin | Capa delgada que traduce comandos de Telegram a llamadas HTTP a M6 | ⏳ | 🟡 |
| Telegram → LLM → orden | Usted dice "compra 10 EURUSD" y el sistema lo procesa hasta ejecutar | ⏳ | 🔴 |
| TaskFlow (estrategias autónomas) | Estrategias que se ejecutan en background sin necesidad de que usted esté en el chat | ⏳ | 🟡 |
| LLM intercambiable | Puede usar DeepSeek, OpenAI o Claude según lo que convenga | ✅ | 🟢 |

**El operador gana:** Trading desde el bolsillo, en español, sin interfaces.

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
