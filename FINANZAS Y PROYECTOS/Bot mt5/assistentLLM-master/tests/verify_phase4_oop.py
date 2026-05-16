import asyncio
import logging
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.orchestrator import orchestrator
from app.services.mt5_bridge import mt5_bridge

# Configurar logging para ver detalles
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def test_phase4_oop_flow():
    print("Iniciando prueba integral de FASE 4 (OOP & Herramientas Consolidadas)...")
    
    # 1. Inicialización
    mt5_bridge.simulated = True
    if not await orchestrator.initialize():
        print("ERROR: Falló inicialización del orquestador")
        return

    # 2. Crear Estrategia via manage_strategy
    print("\n--- Creando Estrategia (OOP) ---")
    strategy_rules = {
        "indicators": [
            {"name": "ema", "length": 10, "output": "EMA10"},
            {"name": "ema", "length": 20, "output": "EMA20"}
        ],
        "conditions": [
            {"operator": "greater_than", "indicator1": "close", "value": 0} # Dummy condition
        ],
        "action": "buy",
        "volume": 0.1,
        "sl_pips": 20,
        "tp_pips": 40
    }
    
    # Simulamos una llamada de herramienta desde el LLM
    create_args = {
        "action": "create",
        "name": "OOP_Test_Strategy",
        "symbol": "EURUSD",
        "timeframe": "H1",
        "rules": strategy_rules
    }
    
    # Llamamos directamente a _execute_single_tool para simular el flujo interno
    # En producción esto vendría de _execute_tools -> _execute_single_tool
    result_create = await orchestrator._execute_single_tool("manage_strategy", create_args, {})
    print(f"Resultado Creación: {json.dumps(result_create, indent=2)}")
    
    if result_create.get("status") != "success":
        print("ERROR: Falló creación de estrategia")
        return

    strategy_id = result_create["strategy_id"]
    
    # 3. Iniciar Estrategia
    print(f"\n--- Iniciando Estrategia {strategy_id} ---")
    start_args = {"action": "start", "strategy_id": strategy_id}
    result_start = await orchestrator._execute_single_tool("manage_strategy", start_args, {})
    print(f"Resultado Inicio: {result_start}")
    
    # 4. Verificar Estado
    print("\n--- Verificando Estado ---")
    status_args = {"action": "get_status", "strategy_id": strategy_id}
    result_status = await orchestrator._execute_single_tool("manage_strategy", status_args, {})
    print(f"Estado: {result_status['data']['status']}")
    
    # 5. Probar Backtest (Simulación)
    print("\n--- Probando Backtest (create_and_backtest_strategy) ---")
    backtest_args = {
        "symbol": "EURUSD",
        "timeframe": "H1",
        "rules": strategy_rules,
        "days": 2
    }
    result_backtest = await orchestrator._execute_single_tool("create_and_backtest_strategy", backtest_args, {})
    print(f"Backtest Status: {result_backtest.get('status')}")
    if result_backtest.get("status") == "success":
        print(f"Señales encontradas: {result_backtest['data']['total_signals']}")
    else:
        print(f"Error Backtest: {result_backtest}")

    # 6. Limpieza
    await orchestrator.shutdown()
    print("\nPrueba finalizada.")

if __name__ == "__main__":
    asyncio.run(test_phase4_oop_flow())
