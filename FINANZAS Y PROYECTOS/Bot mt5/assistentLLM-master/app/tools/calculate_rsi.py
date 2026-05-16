from typing import Dict, Any
from ..services.data_engine import data_engine
from .registry import register_tool
import pandas as pd

from .tool_schemas import CalculateRsiSchema

TOOL_META = {
    "name": "calculate_rsi",
    "description": "Calcula RSI sobre un símbolo dado y retorna la última serie",
    "args": {"symbol": "string", "length": "int", "count": "int"},
    "schema": CalculateRsiSchema
}


@register_tool("calculate_rsi", TOOL_META)
def run(args: Dict[str, Any]):
    symbol = args.get("symbol")
    length = int(args.get("length", 14))
    count = int(args.get("count", 100))

    # Obtener datos históricos vía mt5_bridge
    from ..services.mt5_bridge import mt5_bridge
    end = None
    start = pd.Timestamp.now() - pd.Timedelta(days=1)
    df = mt5_bridge.get_historical_data(symbol, 16385, start.to_pydatetime(), end, count=count)
    if df is None:
        return {"status": "error", "error": "No historical data"}

    # Calcular RSI usando data_engine
    try:
        rsi_series = data_engine.calculate_indicator(df, {"name": "rsi", "column": "close", "length": length})
        # Devolver últimos registros serializados
        last = rsi_series.dropna().tail(10).tolist()
        return {"status": "success", "data": {"rsi": last}}
    except Exception as e:
        return {"status": "error", "error": str(e)}
