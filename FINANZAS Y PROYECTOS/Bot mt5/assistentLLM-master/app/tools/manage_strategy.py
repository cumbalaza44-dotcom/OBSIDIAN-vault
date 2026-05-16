"""
manage_strategy - Herramienta para gestionar el ciclo de vida de estrategias
Router centralizado para crear, activar, desactivar y consultar estrategias.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def run(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gestiona estrategias de trading.
    
    Args:
        action (str): Acción a realizar ('create', 'activate', 'deactivate', 'get_status')
        strategy_name (str, optional): Nombre de la estrategia (para create)
        strategy_id (str, optional): ID de la estrategia (para activate/deactivate/get_status)
        symbol (str, optional): Símbolo (para create)
        timeframe (str, optional): Timeframe (para create)
        rules (dict, optional): Reglas de la estrategia (para create)
    
    Returns:
        Dict con status, message y data
    """
    try:
        from ..services.trading_engine import trading_engine
        
        action = args.get("action")
        if not action:
            return {
                "status": "error",
                "message": "Parámetro requerido: action",
                "data": {"valid_actions": ["create", "activate", "deactivate", "get_status"]}
            }
        
        # Delegar al TradingEngine
        result = await trading_engine.handle_strategy_management(action, args)
        
        return result
            
    except Exception as e:
        logger.error(f"Error en manage_strategy: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error interno: {str(e)}",
            "data": {}
        }
