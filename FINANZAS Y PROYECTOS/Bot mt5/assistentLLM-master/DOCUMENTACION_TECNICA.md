# Documentación Técnica: Trading Assistant

Este documento describe la arquitectura, componentes y flujos de datos del sistema "Trading Assistant", incluyendo el plan detallado para la Fase 4.

## 1. Arquitectura Actual y Futura (Fase 4)

El sistema evolucionará para incluir un motor de trading y estrategias, centralizando la lógica de ejecución.

### Diagrama de Componentes (Mermaid con Fase 4)

```mermaid
graph TD
    subgraph Cliente
        UI[Cliente UI]
    end

    subgraph Backend
        Gateway[API Gateway / WebSocket]
        Orchestrator[Orquestador]
        
        subgraph Fase 4 - Motores
            TradingEngine[Trading Engine]
            StrategyEngine[Strategy Engine]
        end

        subgraph Servicios
            LLM[LLM Service (Gemini)]
            MT5[MT5 Bridge]
            State[State Manager (Redis/Memoria)]
            DataEngine[Data Engine (Pandas/Polars)]
        end
        
        subgraph Herramientas
            Tools[Registro de Herramientas]
            ToolA[open_trade]
            ToolB[manage_strategy]
            ToolC[create_and_backtest_strategy]
        end
    end

    subgraph Sistemas Externos
        Google[Google AI Platform]
        MetaTrader[Terminal MetaTrader 5]
    end

    UI --"Prompt (JSON)"--> Gateway
    Gateway --"process_request()"--> Orchestrator
    Orchestrator --"process_prompt()"--> LLM
    LLM --"API Call"--> Google
    
    Orchestrator --"handle_direct_tool_call()"--> TradingEngine
    Orchestrator --"handle_strategy_management()"--> TradingEngine
    TradingEngine --"activate/deactivate"--> StrategyEngine
    TradingEngine --"_execute_trade_request()"--> MT5
    
    StrategyEngine --"Señal de Trade"--> TradingEngine
    
    Orchestrator --"Ejecuta Herramientas de Análisis"--> Tools
    Tools --"Llama a"--> DataEngine
    
    Orchestrator --"get/set estado"--> State
    MT5 --"Conexión TCP"--> MetaTrader

    subgraph Flujo de Respuesta
        Orchestrator --"Respuesta Final (JSON)"--> Gateway
        Gateway --"Mensaje WebSocket"--> UI
    end
```

### Flujo de Datos (Fase 4)
1.  El flujo inicial no cambia: **UI -> Gateway -> Orchestrator -> LLM**.
2.  **Nueva Derivación**:
    a.  Si el LLM solicita una herramienta de ejecución (`open_trade`, `close_trade`), el **Orquestador** llama a `handle_direct_tool_call` en el **Trading Engine**.
    b.  Si el LLM solicita gestionar una estrategia (`manage_strategy`), el **Orquestador** llama a `handle_strategy_management` en el **Trading Engine**, que a su vez controla el **Strategy Engine**.
3.  El **Trading Engine** se convierte en el único componente que invoca directamente al **MT5 Bridge** para ejecutar, modificar o cerrar operaciones.
4.  El **Strategy Engine**, una vez activado, recibe datos (ticks o velas) y evalúa sus condiciones internas. Si una condición se cumple, genera una señal de trade que es enviada al **Trading Engine** para su ejecución.

## 2. Especificación de APIs

### API Externa (WebSocket)
(Sin cambios)

### APIs Internas (Inter-servicio - Actualizado Fase 4)

-   `Orchestrator -> LLMService`: (Sin cambios)
-   **`Orchestrator -> TradingEngine`**:
    -   `handle_direct_tool_call(tool_name, params)`: Enruta una llamada de herramienta de ejecución.
    -   `handle_strategy_management(action, strategy_name)`: Controla el ciclo de vida de las estrategias autónomas.
-   **`TradingEngine -> MT5Bridge`**:
    -   Se convierte en el consumidor principal de los métodos de ejecución de `MT5Bridge`.
-   `Orchestrator -> StateManager`: (Sin cambios)

## 3. Schema de Datos y Modelos (Actualizado Fase 4)

Se añadirán nuevos schemas para las herramientas de ejecución y gestión.

-   **`GetHistoricalDataSchema`**: (Existente)
-   **`RunDynamicAnalysisSchema`**: (Existente)
-   ... (otros schemas existentes)

---

-   **`OpenTradeSchema` (Planeado en Fase 4)**:
    -   `symbol: str`
    -   `order_type: str` ('market', 'limit', 'stop')
    -   `volume: float`
    -   `stop_loss_pips: Optional[int]`
    -   `take_profit_pips: Optional[int]`
    -   ... (parámetros adicionales para órdenes pendientes)
-   **`CloseTradeSchema` (Planeado en Fase 4)**:
    -   `trade_id: int`
    -   `volume_to_close: Optional[float]`
    -   `percentage_to_close: Optional[float]`
-   **`ModifyTradeProtectionSchema` (Planeado en Fase 4)**:
    -   `trade_id: int`
    -   `new_sl_pips: Optional[int]`
    -   `new_tp_pips: Optional[int]`
    -   `move_sl_to_breakeven: bool`
-   **`CancelPendingOrderSchema` (Planeado en Fase 4)**:
    -   `order_id: int`
-   **`ManageStrategySchema` (Planeado en Fase 4)**:
    -   `action: str` ('activate', 'deactivate')
    -   `strategy_name: str`
    -   `symbol: str`
    -   `timeframe: str`
-   **`CreateAndBacktestStrategySchema` (Planeado en Fase 4)**:
    -   `name: str`
    -   `entry_conditions: List[Dict]`
    -   `exit_conditions: List[Dict]`
    -   (La estructura interna de las condiciones será un objeto JSON complejo)

## 4. Configuración de Entorno y Dependencias
(Sin cambios significativos en esta sección, pero se requerirá `python-dotenv` para el despliegue)

## 5. Inventario de Componentes (Actualizado Fase 4)

| Archivo/Módulo | Estado | Completado | Dependencias | Riesgos Conocidos |
| :--- | :--- | :--- | :--- | :--- |
| 📁 `main.py` | Production | 95% | FastAPI, Uvicorn, Orchestrator | - |
| 📁 `app/api/gateway.py` | Production | 90% | FastAPI, WebSocket, Orchestrator | - |
| 📁 `app/core/config.py` | Production | 100% | Pydantic | - |
| 📁 `app/core/state_manager.py` | Beta | 85% | Redis (opcional) | La versión en memoria no es persistente. |
| 📁 `app/services/orchestrator.py` | Beta | 80% -> 75% | LLMService, **TradingEngine**, StateManager | Su rol cambiará para delegar ejecución. |
| 📁 `app/services/trading_engine.py` | **Planned** | 0% | MT5Bridge, StrategyEngine | **NUEVO**. Punto central de ejecución. |
| 📁 `app/services/strategy_engine.py` | **Planned** | 0% | DataEngine | **NUEVO**. Lógica de estrategias autónomas. |
| 📁 `app/services/llm_service.py` | Production | 90% | `google-generativeai` | Dependencia de servicio externo. |
| 📁 `app/services/mt5_bridge.py` | Production | 90% | `MetaTrader5` | Conexión con MT5 puede ser inestable. |
| 📁 `app/services/data_engine.py` | Beta | 70% | Pandas, Polars/Numba (opcional) | - |
| 📁 `app/tools/registry.py` | Production | 100% | - | - |
| 📁 `app/tools/*.py` | **Development** | 30% -> **60%** | MT5Bridge, DataEngine, **TradingEngine** | Se añadirán herramientas de ejecución y gestión. |

## 6. Flujos Críticos (Actualizado Fase 4)

-   **[✅] Prompt → LLM → Herramienta de Análisis → Respuesta**: Flujo de solo lectura, sin cambios.
-   **[🟡] Prompt → LLM → Herramienta de Ejecución → Trading Engine → MT5**: **NUEVO FLUJO**. El orquestador delega la ejecución al Trading Engine.
-   **[🟡] Prompt → LLM → Gestión de Estrategia → Trading Engine → Strategy Engine**: **NUEVO FLUJO**. El usuario puede activar/desactivar estrategias autónomas.
-   **[🟡] Strategy Engine → Señal → Trading Engine → MT5**: **NUEVO FLUJO AUTÓNOMO**. El sistema opera por sí mismo basado en estrategias activas.
-   **[🟡] Definición dinámica de estrategia → Backtesting → Resultados**: **FLUJO PLANEADO**. A través de la herramienta `create_and_backtest_strategy`.
-   **[✅] Conexión MT5 → Streaming → Procesamiento**: El `StrategyEngine` requerirá un streaming de datos real, pasando de un modelo bajo demanda a uno de suscripción.

## 7. Plan de Extensión Fase 4 (Revisado)

### Objetivo: Construir un `TradingEngine` robusto que pueda ejecutar tanto órdenes directas del LLM como gestionar un `StrategyEngine` interno para la operación autónoma, y dotar al LLM de herramientas para la validación y creación dinámica de estrategias.

---

### **Paso 4.1: Toolbox - Habilidades de Ejecución Avanzada**

**Acción:** Crear e implementar las siguientes herramientas en el directorio `/tools`. Deben encapsular lógica de negocio, manejar errores exhaustivamente y devolver un JSON de estado claro.

-   **`open_trade(symbol, order_type, volume, stop_loss_pips, take_profit_pips, ...)`**
    -   **Aclaración:** Reemplaza a `open_market_order`. Será más versátil, aceptando `order_type` ('market', 'limit', 'stop'). La herramienta contendrá la lógica para construir los diferentes tipos de `request` que `mt5.order_send()` necesita.
-   **`close_trade(trade_id, volume_to_close, percentage_to_close)`**
    -   **Aclaración:** Mejorada para aceptar tanto un `volume_to_close` (lotes) como un `percentage_to_close`. La herramienta debe definir una prioridad si ambos se proporcionan.
-   **`modify_trade_protection(trade_id, new_sl_pips, new_tp_pips, move_sl_to_breakeven)`**
    -   **Aclaración:** Expandida para aceptar SL/TP en pips (la herramienta los convertirá a precios) y un booleano `move_sl_to_breakeven` para simplificar una acción común.
-   **`cancel_pending_order(order_id)`**
    -   **Aclaración:** Nueva herramienta esencial para cancelar órdenes `limit` o `stop` no ejecutadas.

---

### **Paso 4.2: Construcción del `TradingEngine` y el `StrategyEngine` Interno**

**Acción:**

1.  **Crear `app/services/strategy_engine.py`**:
    -   Definir una clase base abstracta `Strategy` con métodos como `check_conditions(data)` y `get_name()`.
    -   Implementar estrategias concretas que hereden de ella (ej. `StrategyEMACross`).
    -   Crear la clase `StrategyEngine` que gestionará un diccionario de estrategias, con métodos `activate(strategy_name)`, `deactivate(strategy_name)` y un bucle principal `run_tick_evaluation()`.
2.  **Crear `app/services/trading_engine.py`**:
    -   Importará e instanciará el `StrategyEngine`.
    -   Implementará los puntos de entrada para el `Orchestrator`:
        -   `handle_direct_tool_call(tool_name, params)`: Un router para las órdenes directas del LLM.
        -   `handle_strategy_management(action, strategy_name)`: Interfaz para controlar el `StrategyEngine`.
    -   Implementará el método de ejecución centralizado: `_execute_trade_request(trade_request)`, que será usado tanto por las llamadas directas como por las señales del `StrategyEngine`.
3.  **Añadir Herramienta a la Toolbox**:
    -   Crear la herramienta `manage_strategy(action, strategy_name, symbol, timeframe)` que servirá como fachada, llamando al método `handle_strategy_management` del `TradingEngine`.

**Contexto:** Con esta jerarquía, el `TradingEngine` se convierte en el guardián de la ejecución, asegurando que todas las órdenes, sin importar su origen, pasen por los mismos filtros de validación y riesgo.

---

### **Paso 4.3: Habilidades de Creación y Validación Dinámica de Estrategias**

**Acción:** Implementar la herramienta `create_and_backtest_strategy`.

-   **Diseño de la Entrada:** La herramienta recibirá un objeto JSON estructurado que el LLM deberá generar a partir del lenguaje natural del usuario.
    ```json
    {
      "name": "RSI_MACD_Cross_v1",
      "entry_conditions": [
        {"type": "indicator", "name": "RSI", "params": {"period": 14}, "condition": "less_than", "value": 30},
        {"type": "indicator", "name": "MACD", "params": {}, "condition": "cross_above", "value": "signal_line"}
      ],
      "exit_conditions": [
        {"type": "protection", "name": "stop_loss", "params": {"type": "ATR", "multiplier": 2}},
        {"type": "protection", "name": "take_profit", "params": {"type": "fixed_pips", "value": 100}}
      ]
    }
    ```
-   **Implementación del Backtester:** La herramienta usará el `DataEngine` para obtener datos históricos y luego iterará vela por vela, evaluando las `entry_conditions` y `exit_conditions` para simular la estrategia y generar un informe de rendimiento (Profit Factor, Drawdown, etc.).

**Contexto:** Esta herramienta transforma el sistema de un ejecutor pasivo a un entorno de investigación interactivo, cerrando el ciclo entre la idea y la validación con datos.

---

### **Paso 4.4: Despliegue, Seguridad y UI Final**

**Acción:**

-   **Preparación para el Despliegue:** Mover todas las configuraciones sensibles a un archivo `.env` y generar un `requirements.txt` congelado (`pip freeze > requirements.txt`).
-   **Exposición Segura de la API:** Desplegar en un VPS usando Nginx o Caddy como proxy inverso con HTTPS (Let's Encrypt). Implementar autenticación por clave de API en el endpoint de FastAPI.
-   **Configuración de la Interfaz de Google (UI):** Generar una especificación OpenAPI (vía `/docs` de FastAPI) y subirla a Google AI Studio o Vertex AI para que el modelo pueda usar las herramientas.

---

### **Herramientas Adicionales Sugeridas (Post-Fase 4)**

-   `get_economic_calendar(importance_level)`: Para obtener eventos económicos importantes.
-   `set_global_risk_parameters(max_daily_drawdown_pct, ...)`: Para ajustar las reglas de riesgo maestras del `TradingEngine`.
-   `run_correlation_analysis(symbols, period)`: Para generar una matriz de correlación.
-   `get_session_performance()`: Para calcular el P/L de la sesión actual.
-   `save_strategy_to_file(strategy_json)` / `load_strategy_from_file(strategy_name)`: Para persistir y reutilizar estrategias dinámicas.
