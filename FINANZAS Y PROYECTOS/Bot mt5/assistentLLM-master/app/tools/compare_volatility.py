from typing import Dict, Any
from ..services.mt5_bridge import mt5_bridge
from ..services.data_engine import data_engine
from .registry import register_tool
import pandas as pd

from .tool_schemas import CompareVolatilitySchema

TOOL_META = {
    "name": "compare_volatility",
    "description": "Compara ATR (volatilidad) entre dos símbolos",
    "args": {"symbol_a": "string", "symbol_b": "string", "period": "int"},
    "schema": CompareVolatilitySchema
}


@register_tool("compare_volatility", TOOL_META)
def run(args: Dict[str, Any]):
    a = args.get('symbol_a')
    b = args.get('symbol_b')
    period = int(args.get('period', 14))
    if not a or not b:
        return {"status": "error", "error": "symbol_a y symbol_b son requeridos"}

    end = None
    start = pd.Timestamp.now() - pd.Timedelta(days=7)
    df_a = mt5_bridge.get_historical_data(a, 16385, start.to_pydatetime(), end, count=period*10)
    df_b = mt5_bridge.get_historical_data(b, 16385, start.to_pydatetime(), end, count=period*10)
    if df_a is None or df_b is None:
        return {"status": "error", "error": "No data for one or both symbols"}

    # Simple ATR-like: high-low rolling std as proxy
    try:
        atr_a = (df_a['high'] - df_a['low']).rolling(window=period).std().iloc[-1]
        atr_b = (df_b['high'] - df_b['low']).rolling(window=period).std().iloc[-1]
    except Exception as e:
        return {"status": "error", "error": str(e)}

    return {"status": "success", "data": {"symbol_a": a, "symbol_b": b, "atr_a": float(atr_a), "atr_b": float(atr_b)}}
