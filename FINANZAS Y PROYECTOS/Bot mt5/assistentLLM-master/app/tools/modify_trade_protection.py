"""
modify_trade_protection - Herramienta para modificar SL/TP de operaciones
Soporta especificación en pips y movimiento automático a breakeven.
"""

import logging
from typing import Dict, Any
import MetaTrader5 as mt5

logger = logging.getLogger(__name__)

async def run(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Modifica Stop Loss y/o Take Profit de una operación.
    
    Args:
        trade_id (int): ID de la operación
        new_sl_pips (float, optional): Nuevo Stop Loss en pips
        new_tp_pips (float, optional): Nuevo Take Profit en pips
        move_sl_to_breakeven (bool, optional): Mover SL al precio de entrada
    
    Returns:
        Dict con status, message y data
    """
    try:
        from ..services.mt5_bridge import mt5_bridge
        
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
        
        symbol = position["symbol"]
        open_price = position["price_open"]
        pos_type = position["type"]
        
        # Obtener información del símbolo
        symbol_info = mt5_bridge.get_symbol_info(symbol)
        point = symbol_info["point"]
        digits = symbol_info["digits"]
        
        # Valores actuales
        current_sl = position.get("sl", 0)
        current_tp = position.get("tp", 0)
        
        # Calcular nuevos valores
        new_sl = current_sl
        new_tp = current_tp
        
        # Breakeven tiene prioridad
        move_to_be = args.get("move_sl_to_breakeven", False)
        if move_to_be:
            new_sl = open_price
            logger.info(f"Moviendo SL a breakeven: {new_sl}")
        
        # Aplicar nuevos pips si se especifican
        new_sl_pips = args.get("new_sl_pips")
        new_tp_pips = args.get("new_tp_pips")
        
        if new_sl_pips is not None and not move_to_be:
            new_sl_pips = float(new_sl_pips)
            if pos_type == mt5.POSITION_TYPE_BUY:
                new_sl = open_price - (new_sl_pips * point)
            else:
                new_sl = open_price + (new_sl_pips * point)
            new_sl = round(new_sl, digits)
        
        if new_tp_pips is not None:
            new_tp_pips = float(new_tp_pips)
            if pos_type == mt5.POSITION_TYPE_BUY:
                new_tp = open_price + (new_tp_pips * point)
            else:
                new_tp = open_price - (new_tp_pips * point)
            new_tp = round(new_tp, digits)
        
        # Validar que al menos algo cambió
        if new_sl == current_sl and new_tp == current_tp:
            return {
                "status": "error",
                "message": "No se especificaron cambios en SL/TP",
                "data": {}
            }
        
        # Construir request
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": trade_id,
            "symbol": symbol,
            "sl": float(new_sl) if new_sl else 0.0,
            "tp": float(new_tp) if new_tp else 0.0
        }
        
        # Ejecutar modificación
        result = mt5_bridge.execute_order(request)
        
        if result.get("retcode") == mt5.TRADE_RETCODE_DONE:
            changes = []
            if new_sl != current_sl:
                changes.append(f"SL: {current_sl} → {new_sl}")
            if new_tp != current_tp:
                changes.append(f"TP: {current_tp} → {new_tp}")
            
            return {
                "status": "success",
                "message": f"Protección modificada: {', '.join(changes)}",
                "data": {
                    "trade_id": trade_id,
                    "old_sl": current_sl,
                    "new_sl": new_sl,
                    "old_tp": current_tp,
                    "new_tp": new_tp,
                    "breakeven_applied": move_to_be
                }
            }
        else:
            return {
                "status": "error",
                "message": f"Error modificando protección: {result.get('comment', 'Unknown error')}",
                "data": {"retcode": result.get("retcode"), "details": result}
            }
            
    except Exception as e:
        logger.error(f"Error en modify_trade_protection: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error interno: {str(e)}",
            "data": {}
        }
