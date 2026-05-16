"""
close_trade - Herramienta para cerrar operaciones de trading
Soporta cierre por volumen absoluto o porcentaje.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

async def run(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Cierra una operación de trading.
    
    Args:
        trade_id (int): ID de la operación a cerrar
        volume_to_close (float, optional): Volumen en lotes a cerrar
        percentage_to_close (float, optional): Porcentaje de la posición a cerrar (0-100)
    
    Returns:
        Dict con status, message y data
    
    Nota: Si se proporcionan ambos parámetros, percentage_to_close tiene prioridad.
    """
    try:
        from ..services.mt5_bridge import mt5_bridge
        import MetaTrader5 as mt5
        
        trade_id = args.get("trade_id")
        if not trade_id:
            return {
                "status": "error",
                "message": "Parámetro requerido: trade_id",
                "data": {}
            }
        
        # Obtener información de la posición
        positions = mt5_bridge.get_positions()
        position = next((p for p in positions if p["ticket"] == trade_id), None)
        
        if not position:
            return {
                "status": "error",
                "message": f"Posición {trade_id} no encontrada",
                "data": {}
            }
        
        # Determinar volumen a cerrar
        total_volume = position["volume"]
        percentage = args.get("percentage_to_close")
        volume_arg = args.get("volume_to_close")
        
        if percentage is not None:
            # Prioridad a porcentaje
            percentage = float(percentage)
            if not 0 < percentage <= 100:
                return {
                    "status": "error",
                    "message": "percentage_to_close debe estar entre 0 y 100",
                    "data": {}
                }
            volume_to_close = total_volume * (percentage / 100.0)
        elif volume_arg is not None:
            volume_to_close = float(volume_arg)
            if volume_to_close > total_volume:
                return {
                    "status": "error",
                    "message": f"Volumen a cerrar ({volume_to_close}) excede volumen de posición ({total_volume})",
                    "data": {}
                }
        else:
            # Si no se especifica, cerrar toda la posición
            volume_to_close = total_volume
        
        # Redondear volumen según step del símbolo
        symbol_info = mt5_bridge.get_symbol_info(position["symbol"])
        volume_step = symbol_info.get("volume_step", 0.01)
        volume_to_close = round(volume_to_close / volume_step) * volume_step
        
        # Determinar precio de cierre y tipo de orden opuesta
        if position["type"] == mt5.POSITION_TYPE_BUY:
            price = symbol_info["bid"]
            order_type = mt5.ORDER_TYPE_SELL
        else:
            price = symbol_info["ask"]
            order_type = mt5.ORDER_TYPE_BUY
        
        # Ejecutar cierre
        result = mt5_bridge.close_position(
            ticket=trade_id,
            symbol=position["symbol"],
            volume=volume_to_close,
            order_type=order_type,
            price=price,
            magic=position.get("magic", 234000)
        )
        
        if result.get("retcode") == mt5.TRADE_RETCODE_DONE:
            is_partial = volume_to_close < total_volume
            return {
                "status": "success",
                "message": f"Posición {'parcialmente ' if is_partial else ''}cerrada exitosamente",
                "data": {
                    "deal": result.get("deal"),
                    "volume_closed": volume_to_close,
                    "volume_remaining": total_volume - volume_to_close if is_partial else 0,
                    "price": price
                }
            }
        else:
            return {
                "status": "error",
                "message": f"Error cerrando posición: {result.get('comment', 'Unknown error')}",
                "data": {"retcode": result.get("retcode"), "details": result}
            }
            
    except Exception as e:
        logger.error(f"Error en close_trade: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error interno: {str(e)}",
            "data": {}
        }
