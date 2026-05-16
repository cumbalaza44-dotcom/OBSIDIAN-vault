from typing import Dict, Any
from ..services.mt5_bridge import mt5_bridge
from .registry import register_tool

from .tool_schemas import ListOpenPositionsSchema

TOOL_META = {
    "name": "list_open_positions",
    "description": "Lista posiciones abiertas en la cuenta",
    "args": {},
    "schema": ListOpenPositionsSchema
}


@register_tool("list_open_positions", TOOL_META)
def run(args: Dict[str, Any]):
    positions = mt5_bridge.get_positions()
    return {"status": "success", "data": {"count": len(positions), "positions": positions}}
