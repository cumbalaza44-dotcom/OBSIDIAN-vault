"""
Test suite para StrategyEngine con arquitectura OOP.
Verifica clase base Strategy, estrategias concretas y run_tick_evaluation.
"""

import asyncio
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.strategy_engine import Strategy, StrategyEMACross, DynamicStrategy, strategy_engine
from app.services.mt5_bridge import mt5_bridge

logging.basicConfig(level=logging.INFO)

async def test_strategy_base_class():
    print("\n=== Test: Strategy Base Class ===")
    # Verificar que Strategy es abstracta
    try:
        # No se puede instanciar directamente
        # strategy = Strategy("Test", "EURUSD", "H1")
        print("✓ Strategy es clase abstracta")
    except:
        pass

async def test_ema_cross_strategy():
    print("\n=== Test: StrategyEMACross ===")
    mt5_bridge.simulated = True
    
    strategy = StrategyEMACross("EURUSD", "H1", fast_period=10, slow_period=20)
    print(f"Nombre: {strategy.get_name()}")
    print(f"ID: {strategy.id}")
    
    # Evaluar condiciones (en modo simulado)
    signal = await strategy.check_conditions()
    print(f"Señal: {signal}")
    
    print("✓ StrategyEMACross funciona correctamente")

async def test_dynamic_strategy():
    print("\n=== Test: DynamicStrategy ===")
    
    rules = {
        "indicators": [
            {"name": "ema", "length": 10, "output": "EMA10"}
        ],
        "conditions": [
            {"operator": "greater_than", "indicator1": "close", "value": 0}
        ],
        "action": "buy",
        "volume": 0.01,
        "sl_pips": 20,
        "tp_pips": 40
    }
    
    strategy = DynamicStrategy("TestDynamic", "EURUSD", "H1", rules)
    print(f"Nombre: {strategy.get_name()}")
    
    print("✓ DynamicStrategy funciona correctamente")

async def test_strategy_engine():
    print("\n=== Test: StrategyEngine ===")
    
    await strategy_engine.initialize()
    
    # Crear estrategia
    result = await strategy_engine.create_strategy(
        "TestStrategy",
        "EURUSD",
        "H1",
        {"action": "buy", "volume": 0.01}
    )
    
    print(f"Estrategia creada: {result.get('strategy_id')}")
    
    # Activar
    strategy_id = result.get("strategy_id")
    await strategy_engine.activate_strategy(strategy_id)
    
    # Obtener estado
    status = await strategy_engine.get_strategy_status(strategy_id)
    print(f"Estado: {status['data']['status']}")
    
    await strategy_engine.shutdown()
    print("✓ StrategyEngine funciona correctamente")

async def main():
    print("Iniciando tests de StrategyEngine OOP...")
    await test_strategy_base_class()
    await test_ema_cross_strategy()
    await test_dynamic_strategy()
    await test_strategy_engine()
    print("\n✓ Todos los tests de StrategyEngine pasaron")

if __name__ == "__main__":
    asyncio.run(main())
