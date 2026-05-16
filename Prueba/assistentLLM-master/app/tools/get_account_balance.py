from typing import Dict, Any
from ..services.mt5_bridge import mt5_bridge
from .registry import register_tool

from .tool_schemas import GetAccountBalanceSchema

TOOL_META = {
    "name": "get_account_balance",
    "description": "Obtiene el balance y datos básicos de la cuenta",
    "args": {},
    "schema": GetAccountBalanceSchema
}


@register_tool("get_account_balance", TOOL_META)
def run(args: Dict[str, Any]):
    acct = mt5_bridge.get_account_info()
    if not acct:
        return {"status": "error", "error": "No account info available"}
    return {"status": "success", "data": {"balance": acct.get("balance"), "equity": acct.get("equity")}}
