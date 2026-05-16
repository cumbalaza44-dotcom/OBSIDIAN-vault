from typing import Dict, Any
from ..services.mt5_bridge import mt5_bridge
from .registry import register_tool

from .tool_schemas import GetSymbolPriceSchema

TOOL_META = {
    "name": "get_symbol_price",
    "description": "Obtiene el precio actual (bid/ask) de un símbolo",
    "args": {"symbol": "string"},
    "schema": GetSymbolPriceSchema
}


@register_tool("get_symbol_price", TOOL_META)
def run(args: Dict[str, Any]):
    symbol = args.get("symbol")
    if not symbol:
        return {"status": "error", "error": "symbol is required"}
    info = mt5_bridge.get_symbol_info(symbol)
    if not info:
        return {"status": "error", "error": f"No info for {symbol}"}
    return {"status": "success", "data": {"bid": info.get("bid"), "ask": info.get("ask")}}
