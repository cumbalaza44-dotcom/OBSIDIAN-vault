"""
TradingEngine - El brazo ejecutor del sistema.
Responsabilidades:
- Centralizar la ejecución de todas las órdenes (directas y de estrategias)
- Validar parámetros de riesgo antes de ejecutar
- Gestionar el ciclo de vida del StrategyEngine
"""

import logging
from typing import Dict, Any, Optional
import MetaTrader5 as mt5
from .mt5_bridge import mt5_bridge

logger = logging.getLogger(__name__)

class TradingEngine:
    """Motor de ejecución y gestión de estrategias."""
    
    def __init__(self):
        self.initialized = False
        # strategy_engine se importa dentro de los métodos para evitar ciclos o se inyecta

        
    async def initialize(self) -> bool:
        """Inicializa el motor de trading."""
        logger.info("Inicializando Trading Engine...")
        self.initialized = True
        return True

    async def handle_direct_tool_call(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Punto de entrada para llamadas directas desde el Orquestador.
        """
        if tool_name == "open_trade":
            return await self._open_trade(params)
        elif tool_name == "close_trade":
            return await self._close_trade(params)
        elif tool_name == "modify_trade_protection":
            return await self._modify_trade_protection(params)
        elif tool_name == "cancel_pending_order":
            return await self._cancel_pending_order(params)
        else:
            return {"error": f"Herramienta de ejecución '{tool_name}' no soportada", "status": "error"}

    async def handle_strategy_management(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gestiona el ciclo de vida de las estrategias.
        Actions: create, start, stop, status, backtest
        """
        from .strategy_engine import strategy_engine
        
        if action == "create":
            return await strategy_engine.create_strategy(
                params.get("name"), params.get("symbol"), params.get("timeframe"), params.get("rules")
            )
        elif action == "start":
            return await strategy_engine.activate_strategy(params.get("strategy_id"))
        elif action == "stop":
            return await strategy_engine.deactivate_strategy(params.get("strategy_id"))
        elif action == "get_status":
            return await strategy_engine.get_strategy_status(params.get("strategy_id"))
        elif action == "backtest":
            return await strategy_engine.backtest_strategy(
                params.get("symbol"), params.get("timeframe"), params.get("rules"), params.get("days", 30)
            )
        else:
            return {"error": f"Acción de estrategia '{action}' no soportada", "status": "error"}

    async def _open_trade(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Lógica para abrir una operación."""
        symbol = params.get("symbol")
        order_type_str = params.get("order_type", "market").lower()
        volume = params.get("volume")
        
        # Obtener info del símbolo para precios actuales y dígitos
        symbol_info = mt5_bridge.get_symbol_info(symbol)
        if not symbol_info:
            return {"error": f"Símbolo {symbol} no encontrado", "status": "error"}
        
        # Mapeo de tipos de orden
        type_map = {
            "market_buy": mt5.ORDER_TYPE_BUY,
            "market_sell": mt5.ORDER_TYPE_SELL,
            "limit_buy": mt5.ORDER_TYPE_BUY_LIMIT,
            "limit_sell": mt5.ORDER_TYPE_SELL_LIMIT,
            "stop_buy": mt5.ORDER_TYPE_BUY_STOP,
            "stop_sell": mt5.ORDER_TYPE_SELL_STOP
        }
        
        # Determinar tipo exacto si es market
        if order_type_str == "market":
            # Por defecto asumimos buy si no se especifica dirección, 
            # pero lo ideal es que el LLM pase 'market_buy' o 'market_sell'
            # Si solo pasa 'market', necesitamos saber la dirección.
            direction = params.get("direction", "buy").lower()
            order_type_str = f"market_{direction}"
            
        mt5_type = type_map.get(order_type_str)
        if mt5_type is None:
            return {"error": f"Tipo de orden '{order_type_str}' no válido", "status": "error"}
            
        # Precio de ejecución
        price = params.get("price")
        if not price:
            price = symbol_info["ask"] if "buy" in order_type_str else symbol_info["bid"]
            
        # Construir request
        request = {
            "action": mt5.TRADE_ACTION_DEAL if "market" in order_type_str else mt5.TRADE_ACTION_PENDING,
            "symbol": symbol,
            "volume": float(volume),
            "type": mt5_type,
            "price": float(price),
            "magic": params.get("magic", 123456),
            "comment": params.get("comment", "Trading Assistant Order"),
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # SL y TP en pips
        sl_pips = params.get("stop_loss_pips")
        tp_pips = params.get("take_profit_pips")
        point = symbol_info["point"]
        
        if sl_pips:
            if "buy" in order_type_str:
                request["sl"] = price - (sl_pips * point)
            else:
                request["sl"] = price + (sl_pips * point)
                
        if tp_pips:
            if "buy" in order_type_str:
                request["tp"] = price + (tp_pips * point)
            else:
                request["tp"] = price - (tp_pips * point)

        return mt5_bridge.execute_order(request)

    async def _close_trade(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Lógica para cerrar una operación."""
        ticket = params.get("trade_id")
        if not ticket:
            return {"error": "ID de operación (trade_id) requerido", "status": "error"}
            
        # Obtener posición para saber símbolo y volumen
        positions = mt5_bridge.get_positions()
        pos = next((p for p in positions if p["ticket"] == ticket), None)
        
        if not pos:
            return {"error": f"Posición {ticket} no encontrada", "status": "error"}
            
        symbol = pos["symbol"]
        volume = params.get("volume_to_close") or pos["volume"]
        
        # Si se pide porcentaje
        pct = params.get("percentage_to_close")
        if pct:
            volume = pos["volume"] * (pct / 100.0)
            
        # Redondear volumen según el paso del símbolo
        symbol_info = mt5_bridge.get_symbol_info(symbol)
        step = symbol_info["volume_step"]
        volume = round(volume / step) * step
        
        # Tipo de orden contraria
        order_type = mt5.ORDER_TYPE_SELL if pos["type"] == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5_bridge.get_symbol_info(symbol)["bid" if order_type == mt5.ORDER_TYPE_SELL else "ask"]
        
        return mt5_bridge.close_position(ticket, symbol, volume, order_type, price)

    async def _modify_trade_protection(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Modifica SL/TP de una operación."""
        ticket = params.get("trade_id")
        new_sl_pips = params.get("new_sl_pips")
        new_tp_pips = params.get("new_tp_pips")
        move_to_be = params.get("move_sl_to_breakeven", False)
        
        if not ticket:
            return {"error": "ID de operación (trade_id) requerido", "status": "error"}
            
        # Obtener info de la posición
        positions = mt5_bridge.get_positions()
        pos = next((p for p in positions if p["ticket"] == ticket), None)
        if not pos:
            return {"error": f"Posición {ticket} no encontrada", "status": "error"}
            
        symbol = pos["symbol"]
        open_price = pos["price_open"]
        pos_type = pos["type"] # 0=Buy, 1=Sell
        symbol_info = mt5_bridge.get_symbol_info(symbol)
        point = symbol_info["point"]
        
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "symbol": symbol
        }
        
        # Calcular nuevos precios
        sl_price = pos["sl"]
        tp_price = pos["tp"]
        
        if move_to_be:
            # Mover SL a precio de entrada (más un pequeño margen opcional para cubrir comisiones)
            sl_price = open_price
            
        if new_sl_pips is not None:
            if pos_type == mt5.POSITION_TYPE_BUY:
                sl_price = open_price - (float(new_sl_pips) * point)
            else:
                sl_price = open_price + (float(new_sl_pips) * point)

        if new_tp_pips is not None:
            if pos_type == mt5.POSITION_TYPE_BUY:
                tp_price = open_price + (float(new_tp_pips) * point)
            else:
                tp_price = open_price - (float(new_tp_pips) * point)
                
        request["sl"] = float(sl_price)
        request["tp"] = float(tp_price)
            
        return mt5_bridge.execute_order(request)

    async def _cancel_pending_order(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Cancela una orden pendiente."""
        ticket = params.get("order_id")
        if not ticket:
            return {"error": "ID de orden (order_id) requerido", "status": "error"}
            
        request = {
            "action": mt5.TRADE_ACTION_REMOVE,
            "order": ticket
        }
        
        return mt5_bridge.execute_order(request)

# Instancia global
trading_engine = TradingEngine()
