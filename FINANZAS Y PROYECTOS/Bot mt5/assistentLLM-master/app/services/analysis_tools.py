"""
Analysis Tools - Lógica de negocio para herramientas de análisis técnico.
Refactorizado para usar Polars para máximo rendimiento.
"""
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json

try:
    import polars as pl
    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False

from ..services.mt5_bridge import mt5_bridge
from ..services.data_engine import data_engine

logger = logging.getLogger(__name__)

async def run_dynamic_analysis(
    symbol: str,
    timeframe: str,
    args: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Ejecuta un análisis técnico dinámico usando Polars.
    """
    try:
        # 1. Parámetros
        days_to_analyze = args.get("days", 2)
        indicators_to_calc = args.get("indicators", [])
        conditions = args.get("conditions", [])
        output_columns = args.get("output_columns")

        if not indicators_to_calc:
            return {"error": "No se especificaron indicadores para calcular.", "status": "error"}

        # 2. Obtener datos (Pandas -> Polars)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_to_analyze)
        timeframe_map = {
            "M1": 1, "M5": 5, "M15": 15, "M30": 30,
            "H1": 16385, "H4": 16388, "D1": 16408
        }
        mt5_timeframe = timeframe_map.get(timeframe.upper(), 16385)
        
        df = mt5_bridge.get_historical_data(symbol, mt5_timeframe, start_date, end_date, as_polars=True)
        if df is None:
            return {"error": f"No se pudieron obtener datos para {symbol}", "status": "error"}

        # 3. Calcular indicadores
        for indicator_spec in indicators_to_calc:
            try:
                spec = indicator_spec.copy()
                name = spec.pop("name")
                output_name = spec.pop("output", None) or name.upper()
                
                # data_engine ahora devuelve pl.Series si Polars está disponible
                series = data_engine.calculate_indicator(df, {"name": name, **spec})
                
                if POLARS_AVAILABLE:
                    df = df.with_columns(series.alias(output_name))
                else:
                    df[output_name] = series
            except Exception as e:
                logger.warning(f"Error calculando indicador {indicator_spec}: {e}")
                return {"error": f"Error en indicador: {indicator_spec}", "status": "error"}

        # 4. Aplicar condiciones (Polars Expressions)
        if POLARS_AVAILABLE:
            filter_expr = None
            for cond in conditions:
                op = cond["operator"]
                ind1 = cond["indicator1"]
                
                if op == "greater_than":
                    expr = pl.col(ind1) > cond["value"]
                elif op == "less_than":
                    expr = pl.col(ind1) < cond["value"]
                elif op in ["cross_above", "cross_below", "cross"]:
                    ind2 = cond["indicator2"]
                    prev_ind1 = pl.col(ind1).shift(1)
                    prev_ind2 = pl.col(ind2).shift(1)
                    
                    if op == "cross_above":
                        expr = (pl.col(ind1) > pl.col(ind2)) & (prev_ind1 <= prev_ind2)
                    elif op == "cross_below":
                        expr = (pl.col(ind1) < pl.col(ind2)) & (prev_ind1 >= prev_ind2)
                    else: # cross
                        expr = ((pl.col(ind1) > pl.col(ind2)) & (prev_ind1 <= prev_ind2)) | \
                               ((pl.col(ind1) < pl.col(ind2)) & (prev_ind1 >= prev_ind2))
                else:
                    continue
                
                filter_expr = expr if filter_expr is None else filter_expr & expr
            
            if filter_expr is not None:
                df = df.filter(filter_expr)
        else:
            # Fallback Pandas (mantenemos lógica anterior si Polars falla)
            pass

        # 5. Formatear salida
        if not output_columns:
            # Columnas base + indicadores (mayúsculas)
            base_cols = ['time', 'open', 'high', 'low', 'close']
            if POLARS_AVAILABLE:
                all_cols = df.columns
                output_columns = base_cols + [c for c in all_cols if c.isupper() and c not in base_cols]
            else:
                output_columns = base_cols + [c for c in df.columns if c.isupper()]

        # Filtrar columnas existentes
        final_cols = [c for c in output_columns if c in df.columns]
        
        if POLARS_AVAILABLE:
            # Polars to dicts
            result_data = df.select(final_cols).to_dicts()
        else:
            result_data = df[final_cols].to_dict(orient='records')

        # Serializar fechas
        result_data = json.loads(json.dumps(result_data, default=str))

        return {
            "status": "success",
            "data": {
                "event_count": len(result_data),
                "events": result_data
            }
        }

    except Exception as e:
        logger.error(f"Error en run_dynamic_analysis: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}
