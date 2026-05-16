"""
cancel_pending_order - Herramienta para cancelar órdenes pendientes
Cancela órdenes limit y stop que aún no se han ejecutado.
"""

import logging
from typing import Dict, Any
import MetaTrader5 as mt5

logger = logging.getLogger(__name__)

async def run(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cancela una orden pendiente.
    
    Args:
        order_id (int): ID de la orden pendiente a cancelar
    
    Returns:
        Dict con status, message y data
    """
    try:
        from ..services.mt5_bridge import mt5_bridge
        
        order_id = args.get("order_id")
        if not order_id:
            return {
                "status": "error",
                "message": "Parámetro requerido: order_id",
                "data": {}
            }
        
        # Obtener órdenes pendientes
        pending_orders = mt5_bridge.get_pending_orders()
        order = next((o for o in pending_orders if o["ticket"] == order_id), None)
        
        if not order:
            return {
                "status": "error",
                "message": f"Orden pendiente {order_id} no encontrada",
                "data": {"available_orders": [o["ticket"] for o in pending_orders]}
            }
        
        # Construir request de cancelación
        request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": order_id,
            "symbol": order["symbol"]
        }
        
        # Ejecutar cancelación
        result = mt5_bridge.execute_order(request)
        
        if result.get("retcode") == mt5.TRADE_RETCODE_DONE:
            return {
                "status": "success",
                "message": f"Orden {order_id} cancelada exitosamente",
                "data": {
                    "order_id": order_id,
                    "symbol": order["symbol"],
                    "type": order.get("type_str", "unknown"),
                    "volume": order.get("volume_initial")
                }
            }
        else:
            return {
                "status": "error",
                "message": f"Error cancelando orden: {result.get('comment', 'Unknown error')}",
                "data": {"retcode": result.get("retcode"), "details": result}
            }
            
    except Exception as e:
        logger.error(f"Error en cancel_pending_order: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error interno: {str(e)}",
            "data": {}
        }
