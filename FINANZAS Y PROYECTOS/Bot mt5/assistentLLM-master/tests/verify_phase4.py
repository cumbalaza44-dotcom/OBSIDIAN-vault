import asyncio
import logging
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.orchestrator import orchestrator
from app.services.mt5_bridge import mt5_bridge
from app.services.strategy_engine import strategy_engine

async def test_phase4_flow():
    logging.basicConfig(level=logging.INFO)
    print("Iniciando prueba integral de FASE 4 (Autonomía)...")
    
    # 1. Inicialización
    mt5_bridge.simulated = True
    if not await orchestrator.initialize():
        print("ERROR: Falló inicialización del orquestador")
        return

    # 2. Crear Estrategia
    print("\n--- Creando Estrategia de Prueba ---")
    strategy_rules = {
        "indicators": [
            {"name": "ema", "length": 10, "output": "EMA10"},
            {"name": "ema", "length": 20, "output": "EMA20"}
        ],
        "conditions": [
            # Condición dummy que siempre sea verdadera con los datos simulados
            # Datos simulados: Close sube constantemente.
            # EMA10 > EMA20 debería cumplirse eventualmente si sube.
            # Pero para asegurar, usamos algo más simple: Close > 0
            {"operator": "greater_than", "indicator1": "close", "value": 0}
        ],
        "action": "buy",
        "volume": 0.1,
        "sl_pips": 20,
        "tp_pips": 40
    }
    
    result = await strategy_engine.create_strategy("TestStrategy", "EURUSD", "H1", strategy_rules)
    strategy_id = result.get("strategy_id")
    print(f"Estrategia creada: {strategy_id}")
    
    # 3. Iniciar Estrategia
    print(f"\n--- Iniciando Estrategia {strategy_id} ---")
    await strategy_engine.start_strategy(strategy_id)
    
    # 4. Forzar evaluación (Simular paso del tiempo)
    print("\n--- Forzando evaluación de estrategia ---")
    # Accedemos directamente a la estrategia para evaluarla
    strategy = strategy_engine.active_strategies[strategy_id]
    await strategy_engine._evaluate_strategy(strategy)
    
    # 5. Verificar si se ejecutó trade
    # En modo simulado, MT5Bridge no guarda trades en memoria persistente compleja,
    # pero podemos ver los logs o verificar si execute_order fue llamado.
    # Para esta prueba, confiaremos en que _evaluate_strategy imprime logs.
    
    print("\n--- Verificando estado ---")
    status = await strategy_engine.get_strategy_status(strategy_id)
    print(f"Estado estrategia: {status['data']['status']}")
    
    # 6. Probar Backtest
    print("\n--- Probando Backtest ---")
    bt_result = await strategy_engine.backtest_strategy("EURUSD", "H1", strategy_rules, days=2)
    print(f"Backtest completado. Señales encontradas: {bt_result['data']['total_signals']}")
    
    # 7. Limpieza
    await orchestrator.shutdown()
    print("\nPrueba finalizada.")

if __name__ == "__main__":
    asyncio.run(test_phase4_flow())
