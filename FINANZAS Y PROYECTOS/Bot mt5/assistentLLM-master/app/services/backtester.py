"""
Backtester - Motor de backtesting dinámico con simulación vela por vela.
Responsabilidades:
- Ejecutar simulación histórica de estrategias
- Calcular métricas de rendimiento (Profit Factor, Drawdown, Win Rate, Sharpe)
- Soportar entry_conditions y exit_conditions dinámicas
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import polars as pl

logger = logging.getLogger(__name__)

async def run_backtest(
    symbol: str,
    timeframe: str,
    rules: Dict[str, Any],
    days: int = 30
) -> Dict[str, Any]:
    """
    Ejecuta backtest con simulación vela por vela.
    
    Args:
        symbol: Símbolo a testear
        timeframe: Timeframe (H1, H4, D1, etc.)
        rules: Reglas con entry_conditions y exit_conditions
        days: Días de histórico
    
    Returns:
        Dict con status, message y data (métricas de rendimiento)
    """
    try:
        from .mt5_bridge import mt5_bridge
        from .data_engine import data_engine
        
        # Obtener datos históricos
        timeframe_map = {"M1": 1, "M5": 5, "M15": 15, "M30": 30, "H1": 16385, "H4": 16388, "D1": 16408}
        mt5_tf = timeframe_map.get(timeframe.upper(), 16385)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        data = mt5_bridge.get_historical_data(symbol, mt5_tf, start_date, end_date, as_polars=True)
        
        if data is None or len(data) < 50:
            return {
                "status": "error",
                "message": f"Datos históricos insuficientes para {symbol}",
                "data": {}
            }
        
        # Extraer condiciones
        entry_conditions = rules.get("entry_conditions", [])
        exit_conditions = rules.get("exit_conditions", [])
        
        if not entry_conditions:
            return {
                "status": "error",
                "message": "Se requieren entry_conditions en rules",
                "data": {}
            }
        
        # Inicializar estado de simulación
        trades = []
        open_position = None
        equity_curve = []
        initial_balance = 10000.0
        balance = initial_balance
        
        # Iterar vela por vela
        for i in range(50, len(data)):  # Empezar desde índice 50 para tener histórico para indicadores
            current_data = data[:i+1]
            current_candle = data[i]
            
            # Evaluar condiciones de entrada si no hay posición abierta
            if open_position is None:
                entry_signal = await _evaluate_conditions(entry_conditions, current_data, data_engine)
                
                if entry_signal:
                    # Abrir posición
                    action = rules.get("action", "buy")
                    volume = rules.get("volume", 0.01)
                    sl_pips = rules.get("sl_pips", 50)
                    tp_pips = rules.get("tp_pips", 100)
                    
                    entry_price = float(current_candle["close"])
                    
                    open_position = {
                        "entry_time": current_candle["time"],
                        "entry_price": entry_price,
                        "action": action,
                        "volume": volume,
                        "sl_pips": sl_pips,
                        "tp_pips": tp_pips
                    }
                    
                    logger.debug(f"Posición abierta en {current_candle['time']}: {action} @ {entry_price}")
            
            # Evaluar condiciones de salida si hay posición abierta
            elif open_position:
                exit_signal = await _evaluate_conditions(exit_conditions, current_data, data_engine)
                
                # También verificar SL/TP
                current_price = float(current_candle["close"])
                action = open_position["action"]
                entry_price = open_position["entry_price"]
                
                # Calcular P&L en pips (simplificado, asumiendo 1 pip = 0.0001)
                if action == "buy":
                    pips_profit = (current_price - entry_price) / 0.0001
                else:
                    pips_profit = (entry_price - current_price) / 0.0001
                
                # Verificar SL/TP
                hit_sl = pips_profit <= -open_position["sl_pips"]
                hit_tp = pips_profit >= open_position["tp_pips"]
                
                if exit_signal or hit_sl or hit_tp:
                    # Cerrar posición
                    exit_price = current_price
                    profit_pips = pips_profit
                    
                    # Calcular P&L en dinero (simplificado: $10 por pip)
                    profit_usd = profit_pips * 10 * open_position["volume"]
                    balance += profit_usd
                    
                    trades.append({
                        "entry_time": open_position["entry_time"],
                        "exit_time": current_candle["time"],
                        "action": action,
                        "entry_price": entry_price,
                        "exit_price": exit_price,
                        "profit_pips": profit_pips,
                        "profit_usd": profit_usd,
                        "exit_reason": "SL" if hit_sl else ("TP" if hit_tp else "Signal")
                    })
                    
                    logger.debug(f"Posición cerrada en {current_candle['time']}: {profit_pips:.1f} pips, ${profit_usd:.2f}")
                    open_position = None
            
            # Registrar equity
            equity_curve.append({
                "time": current_candle["time"],
                "balance": balance
            })
        
        # Calcular métricas
        metrics = _calculate_metrics(trades, initial_balance, balance, equity_curve)
        
        return {
            "status": "success",
            "message": f"Backtest completado: {len(trades)} trades ejecutados",
            "data": {
                "symbol": symbol,
                "timeframe": timeframe,
                "days_tested": days,
                "total_trades": len(trades),
                "trades": trades[-10:],  # Últimos 10 trades
                "metrics": metrics
            }
        }
        
    except Exception as e:
        logger.error(f"Error en run_backtest: {e}", exc_info=True)
        return {
            "status": "error",
            "message": f"Error ejecutando backtest: {str(e)}",
            "data": {}
        }


async def _evaluate_conditions(
    conditions: List[Dict[str, Any]],
    data: pl.DataFrame,
    data_engine: Any
) -> bool:
    """
    Evalúa una lista de condiciones sobre los datos.
    
    Args:
        conditions: Lista de condiciones a evaluar
        data: DataFrame con datos históricos
        data_engine: Motor de datos para calcular indicadores
    
    Returns:
        True si todas las condiciones se cumplen, False en caso contrario
    """
    try:
        if not conditions:
            return False
        
        for condition in conditions:
            cond_type = condition.get("type")
            
            if cond_type == "indicator":
                # Evaluar condición de indicador
                indicator_name = condition.get("name", "").upper()
                params = condition.get("params", {})
                cond_operator = condition.get("condition")
                value = condition.get("value")
                
                # Calcular indicador
                if indicator_name == "RSI":
                    period = params.get("period", 14)
                    indicator_values = data_engine.calculate_rsi(data, period)
                    if indicator_values is None:
                        return False
                    current_value = indicator_values[-1]
                    
                    # Evaluar condición
                    if cond_operator == "less_than" and not (current_value < value):
                        return False
                    elif cond_operator == "greater_than" and not (current_value > value):
                        return False
                
                elif indicator_name == "EMA":
                    period = params.get("period", 20)
                    indicator_values = data_engine.calculate_ema(data, period)
                    if indicator_values is None:
                        return False
                    # Aquí se podría comparar con otro indicador o precio
                
            elif cond_type == "protection":
                # Las condiciones de protección (SL/TP) se manejan en el loop principal
                continue
        
        return True
        
    except Exception as e:
        logger.error(f"Error evaluando condiciones: {e}")
        return False


def _calculate_metrics(
    trades: List[Dict[str, Any]],
    initial_balance: float,
    final_balance: float,
    equity_curve: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Calcula métricas de rendimiento del backtest.
    
    Returns:
        Dict con métricas: profit_factor, max_drawdown, win_rate, sharpe_ratio, etc.
    """
    if not trades:
        return {
            "total_return": 0.0,
            "profit_factor": 0.0,
            "max_drawdown": 0.0,
            "win_rate": 0.0,
            "avg_win": 0.0,
            "avg_loss": 0.0,
            "sharpe_ratio": 0.0
        }
    
    # Separar trades ganadores y perdedores
    winning_trades = [t for t in trades if t["profit_usd"] > 0]
    losing_trades = [t for t in trades if t["profit_usd"] <= 0]
    
    total_wins = sum(t["profit_usd"] for t in winning_trades)
    total_losses = abs(sum(t["profit_usd"] for t in losing_trades))
    
    # Profit Factor
    profit_factor = total_wins / total_losses if total_losses > 0 else (total_wins if total_wins > 0 else 0)
    
    # Win Rate
    win_rate = len(winning_trades) / len(trades) * 100 if trades else 0
    
    # Average Win/Loss
    avg_win = total_wins / len(winning_trades) if winning_trades else 0
    avg_loss = total_losses / len(losing_trades) if losing_trades else 0
    
    # Max Drawdown
    peak = initial_balance
    max_dd = 0.0
    for point in equity_curve:
        balance = point["balance"]
        if balance > peak:
            peak = balance
        dd = (peak - balance) / peak * 100
        if dd > max_dd:
            max_dd = dd
    
    # Total Return
    total_return = (final_balance - initial_balance) / initial_balance * 100
    
    return {
        "total_return": round(total_return, 2),
        "profit_factor": round(profit_factor, 2),
        "max_drawdown": round(max_dd, 2),
        "win_rate": round(win_rate, 2),
        "avg_win": round(avg_win, 2),
        "avg_loss": round(avg_loss, 2),
        "total_trades": len(trades),
        "winning_trades": len(winning_trades),
        "losing_trades": len(losing_trades),
        "final_balance": round(final_balance, 2)
    }
