"""
create_and_backtest_strategy - Herramienta para crear y probar estrategias dinámicamente
Acepta JSON con entry_conditions y exit_conditions, ejecuta simulación vela por vela.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def run(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea y ejecuta backtest de una estrategia.
    
    Args:
        symbol (str): Símbolo a testear
        timeframe (str): Timeframe
        rules (dict): Reglas de la estrategia con entry_conditions y exit_conditions
        days (int, optional): Días de histórico para backtest (default: 30)
    
    Ejemplo de rules:
    {
        "entry_conditions": [
            {"type": "indicator", "name": "RSI", "params": {"period": 14}, "condition": "less_than", "value": 30}
        ],
        "exit_conditions": [
            {"type": "protection", "name": "stop_loss", "params": {"type": "ATR", "multiplier": 2}}
        ]
    }
    
    Returns:
        Dict con status, message y data (incluyendo métricas de rendimiento)
    """
    try:
        from ..services.backtester import run_backtest
        
        symbol = args.get("symbol")
        timeframe = args.get("timeframe", "H1")
        rules = args.get("rules")
        days = args.get("days", 30)
        
        if not all([symbol, rules]):
            return {
                "status": "error",
                "message": "Parámetros requeridos: symbol, rules",
                "data": {}
            }
        
        # Validar estructura de rules
        if not isinstance(rules, dict):
            return {
                "status": "error",
                "message": "rules debe ser un diccionario",
                "data": {}
            }
        
        # Ejecutar backtest
        result = await run_backtest(symbol, timeframe, rules, days)
        
        return result
            
    except Exception as e:
        logger.error(f"Error en create_and_backtest_strategy: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error interno: {str(e)}",
            "data": {}
        }
