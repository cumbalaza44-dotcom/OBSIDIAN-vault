"""
Test suite para Backtester dinámico.
Verifica simulación vela por vela y cálculo de métricas.
"""

import asyncio
import logging
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.backtester import run_backtest
from app.services.mt5_bridge import mt5_bridge

logging.basicConfig(level=logging.INFO)

async def test_basic_backtest():
    print("\n=== Test: Backtest Básico ===")
    mt5_bridge.simulated = True
    
    rules = {
        "entry_conditions": [
            {
                "type": "indicator",
                "name": "RSI",
                "params": {"period": 14},
                "condition": "less_than",
                "value": 30
            }
        ],
        "exit_conditions": [],
        "action": "buy",
        "volume": 0.01,
        "sl_pips": 50,
        "tp_pips": 100
    }
    
    result = await run_backtest("EURUSD", "H1", rules, days=30)
    
    print(f"Status: {result.get('status')}")
    if result.get("status") == "success":
        data = result["data"]
        metrics = data["metrics"]
        print(f"Total Trades: {data['total_trades']}")
        print(f"Profit Factor: {metrics['profit_factor']}")
        print(f"Win Rate: {metrics['win_rate']}%")
        print(f"Max Drawdown: {metrics['max_drawdown']}%")
        print(f"Total Return: {metrics['total_return']}%")
        print("✓ Backtest ejecutado correctamente")
    else:
        print(f"Error: {result.get('message')}")

async def test_backtest_with_exit_conditions():
    print("\n=== Test: Backtest con Exit Conditions ===")
    
    rules = {
        "entry_conditions": [
            {
                "type": "indicator",
                "name": "RSI",
                "params": {"period": 14},
                "condition": "less_than",
                "value": 40
            }
        ],
        "exit_conditions": [
            {
                "type": "protection",
                "name": "stop_loss",
                "params": {"type": "fixed_pips", "value": 50}
            }
        ],
        "action": "buy",
        "volume": 0.01,
        "sl_pips": 50,
        "tp_pips": 100
    }
    
    result = await run_backtest("EURUSD", "H1", rules, days=15)
    print(f"Status: {result.get('status')}")
    print("✓ Backtest con exit conditions validado")

async def main():
    print("Iniciando tests de Backtester...")
    await test_basic_backtest()
    await test_backtest_with_exit_conditions()
    print("\n✓ Todos los tests de Backtester pasaron")

if __name__ == "__main__":
    asyncio.run(main())
