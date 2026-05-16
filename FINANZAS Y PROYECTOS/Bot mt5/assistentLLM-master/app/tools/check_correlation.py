from typing import Dict, Any
from ..services.mt5_bridge import mt5_bridge
from .registry import register_tool
import pandas as pd

from .tool_schemas import CheckCorrelationSchema

TOOL_META = {
    "name": "check_correlation",
    "description": "Calcula la correlación entre dos símbolos en un periodo dado",
    "args": {"symbol_a": "string", "symbol_b": "string", "period": "int"},
    "schema": CheckCorrelationSchema
}


@register_tool("check_correlation", TOOL_META)
def run(args: Dict[str, Any]):
    a = args.get('symbol_a')
    b = args.get('symbol_b')
    period = int(args.get('period', 30))
    if not a or not b:
        return {"status": "error", "error": "symbol_a y symbol_b son requeridos"}

    end = None
    start = pd.Timestamp.now() - pd.Timedelta(days=period)
    df_a = mt5_bridge.get_historical_data(a, 16385, start.to_pydatetime(), end, count=period*24)
    df_b = mt5_bridge.get_historical_data(b, 16385, start.to_pydatetime(), end, count=period*24)
    if df_a is None or df_b is None:
        return {"status": "error", "error": "No data for one or both symbols"}

    try:
        merged = pd.merge(df_a[['time', 'close']], df_b[['time', 'close']], on='time', suffixes=('_a', '_b'))
        corr = merged['close_a'].corr(merged['close_b'])
    except Exception as e:
        return {"status": "error", "error": str(e)}

    return {"status": "success", "data": {"symbol_a": a, "symbol_b": b, "correlation": float(corr)}}
