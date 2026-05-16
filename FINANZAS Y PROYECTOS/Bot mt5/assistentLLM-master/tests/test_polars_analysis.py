import asyncio
import logging
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.analysis_tools import run_dynamic_analysis
from app.services.mt5_bridge import mt5_bridge

async def test_polars_analysis():
    logging.basicConfig(level=logging.INFO)
    print("Iniciando prueba de análisis dinámico con POLARS...")
    
    # Forzar modo simulado
    mt5_bridge.simulated = True
    mt5_bridge.initialize()
    
    # Definir plan de análisis
    analysis_plan = {
        "days": 5,
        "indicators": [
            {"name": "ema", "length": 20, "output": "EMA20"},
            {"name": "ema", "length": 50, "output": "EMA50"},
            {"name": "rsi", "length": 14, "output": "RSI"}
        ],
        "conditions": [
            {"operator": "cross_above", "indicator1": "EMA20", "indicator2": "EMA50"},
            {"operator": "greater_than", "indicator1": "RSI", "value": 50}
        ],
        "output_columns": ["time", "close", "EMA20", "EMA50", "RSI"]
    }
    
    result = await run_dynamic_analysis("EURUSD", "H1", analysis_plan)
    
    if result.get("status") == "success":
        print(f"¡ÉXITO! Análisis completado.")
        print(f"Eventos encontrados: {result['data']['event_count']}")
        if result['data']['event_count'] > 0:
            event = result['data']['events'][0]
            print(f"Muestra del primer evento (Time: {event.get('time')}, Close: {event.get('close')})")
            # No imprimimos el JSON completo para evitar problemas de codificación en consola
    else:
        print(f"ERROR: {result.get('error')}")
    
    mt5_bridge.shutdown()

if __name__ == "__main__":
    asyncio.run(test_polars_analysis())
