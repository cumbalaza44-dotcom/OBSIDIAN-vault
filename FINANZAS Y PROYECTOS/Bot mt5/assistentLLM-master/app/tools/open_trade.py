"""
open_trade - Herramienta para abrir operaciones de trading
Soporta órdenes market, limit y stop con conversión automática de pips a precio.
"""

import logging
from typing import Dict, Any, Optional
import MetaTrader5 as mt5

logger = logging.getLogger(__name__)

async def run(args: Dict[str, Any]) -> Dict[str, Any]:
    """
    Abre una operación de trading.
    
    Args:
        symbol (str): Símbolo a operar
        order_type (str): Tipo de orden ('market_buy', 'market_sell', 'limit_buy', 'limit_sell', 'stop_buy', 'stop_sell')
        volume (float): Volumen en lotes
        stop_loss_pips (float, optional): Stop Loss en pips
        take_profit_pips (float, optional): Take Profit en pips
        price (float, optional): Precio para órdenes limit/stop
        comment (str, optional): Comentario de la orden
    
    Returns:
        Dict con status, message y data
    """
    try:
        from ..services.mt5_bridge import mt5_bridge
        
        # Validar parámetros requeridos
        symbol = args.get("symbol")
        order_type = args.get("order_type", "market_buy").lower()
        volume = args.get("volume")
        
        if not all([symbol, volume]):
            return {
                "status": "error",
                "message": "Parámetros requeridos: symbol, volume",
                "data": {}
            }
        
        # Obtener información del símbolo
        symbol_info = mt5_bridge.get_symbol_info(symbol)
        if not symbol_info:
            return {
                "status": "error",
                "message": f"No se pudo obtener información del símbolo {symbol}",
                "data": {}
            }
        
        point = symbol_info["point"]
        digits = symbol_info["digits"]
        
        # Determinar tipo de orden MT5
        order_type_map = {
            "market_buy": mt5.ORDER_TYPE_BUY,
            "market_sell": mt5.ORDER_TYPE_SELL,
            "limit_buy": mt5.ORDER_TYPE_BUY_LIMIT,
            "limit_sell": mt5.ORDER_TYPE_SELL_LIMIT,
            "stop_buy": mt5.ORDER_TYPE_BUY_STOP,
            "stop_sell": mt5.ORDER_TYPE_SELL_STOP
        }
        
        mt5_order_type = order_type_map.get(order_type)
        if mt5_order_type is None:
            return {
                "status": "error",
                "message": f"Tipo de orden inválido: {order_type}",
                "data": {"valid_types": list(order_type_map.keys())}
            }
        
        # Construir request base
        request = {
            "action": mt5.TRADE_ACTION_DEAL if "market" in order_type else mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": float(volume),
            "type": mt5_order_type,
            "magic": 234000,
            "comment": args.get("comment", "LLM Trade"),
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Determinar precio
        if "market" in order_type:
            # Para market orders, usar precio actual
            if "buy" in order_type:
                price = symbol_info["ask"]
            else:
                price = symbol_info["bid"]
        else:
            # Para limit/stop, usar precio proporcionado
            price = args.get("price")
            if price is None:
                return {
                    "status": "error",
                    "message": f"Precio requerido para órdenes {order_type}",
                    "data": {}
                }
            price = float(price)
        
        request["price"] = round(price, digits)
        
        # Calcular SL/TP si se proporcionan en pips
        sl_pips = args.get("stop_loss_pips")
        tp_pips = args.get("take_profit_pips")
        
        if sl_pips is not None:
            sl_pips = float(sl_pips)
            if "buy" in order_type:
                sl_price = price - (sl_pips * point)
            else:
                sl_price = price + (sl_pips * point)
            request["sl"] = round(sl_price, digits)
        
        if tp_pips is not None:
            tp_pips = float(tp_pips)
            if "buy" in order_type:
                tp_price = price + (tp_pips * point)
            else:
                tp_price = price - (tp_pips * point)
            request["tp"] = round(tp_price, digits)
        
        # Ejecutar orden
        result = mt5_bridge.execute_order(request)
        
        if result.get("retcode") == mt5.TRADE_RETCODE_DONE:
            return {
                "status": "success",
                "message": f"Orden {order_type} ejecutada exitosamente",
                "data": {
                    "order": result.get("order"),
                    "deal": result.get("deal"),
                    "volume": volume,
                    "price": request["price"],
                    "sl": request.get("sl"),
                    "tp": request.get("tp")
                }
            }
        else:
            return {
                "status": "error",
                "message": f"Error ejecutando orden: {result.get('comment', 'Unknown error')}",
                "data": {"retcode": result.get("retcode"), "details": result}
            }
            
    except Exception as e:
        logger.error(f"Error en open_trade: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error interno: {str(e)}",
            "data": {}
        }
