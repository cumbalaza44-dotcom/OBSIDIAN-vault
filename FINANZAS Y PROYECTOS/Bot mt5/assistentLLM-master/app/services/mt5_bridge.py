"""
MT5Bridge - Encapsula todas las llamadas a la librería MetaTrader5.
Actualizado con soporte para Polars.
"""
import logging
from typing import Optional, Dict, Any, List, Tuple, Union
from datetime import datetime, timedelta
import pandas as pd

try:
    import MetaTrader5 as mt5
    MT5_AVAILABLE = True
except ImportError:
    MT5_AVAILABLE = False

try:
    import polars as pl
    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False

logger = logging.getLogger(__name__)

class MT5Bridge:
    """Puente para comunicación con MetaTrader 5."""
    
    def __init__(self, simulated: Optional[bool] = None):
        self.initialized = False
        self.account_info = None
        self.terminal_info = None
        if simulated is None:
            self.simulated = not MT5_AVAILABLE
        else:
            self.simulated = simulated
    
    def initialize(self) -> bool:
        """Inicializa la conexión."""
        if self.simulated:
            self.initialized = True
            self.account_info = {"login": 0, "balance": 100000.0, "currency": "USD"}
            return True
        
        try:
            if not mt5.initialize():
                return False
            self.account_info = mt5.account_info()
            self.initialized = True
            return True
        except Exception as e:
            logger.error(f"Error init MT5: {e}")
            return False
    
    def shutdown(self) -> bool:
        """Cierra la conexión."""
        if not self.simulated:
            mt5.shutdown()
        self.initialized = False
        return True
    
    def is_connected(self) -> bool:
        return self.initialized

    def get_account_info(self) -> Optional[Dict[str, Any]]:
        if not self.is_connected(): return None
        if self.simulated: return self.account_info
        acc = mt5.account_info()
        return acc._asdict() if acc else None

    def get_symbol_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        if not self.is_connected(): return None
        if self.simulated:
            return {"name": symbol, "bid": 1.1000, "ask": 1.1001, "point": 0.0001, "volume_step": 0.01}
        info = mt5.symbol_info(symbol)
        return info._asdict() if info else None

    def get_historical_data(
        self, 
        symbol: str, 
        timeframe: int, 
        start_date: datetime,
        end_date: Optional[datetime] = None,
        count: Optional[int] = None,
        as_polars: bool = False
    ) -> Optional[Union[pd.DataFrame, 'pl.DataFrame']]:
        """Obtiene datos históricos."""
        if not self.is_connected(): return None
        
        try:
            if self.simulated:
                periods = count or 100
                end = end_date or datetime.now()
                # Fix: use 'h' instead of 'H' for deprecated alias
                times = pd.date_range(end=end, periods=periods, freq='h')
                pdf = pd.DataFrame({
                    'time': times,
                    'open': [1.1000 + i*0.0001 for i in range(periods)],
                    'high': [1.1005 + i*0.0001 for i in range(periods)],
                    'low': [1.0995 + i*0.0001 for i in range(periods)],
                    'close': [1.1002 + i*0.0001 for i in range(periods)],
                    'tick_volume': [100 + i for i in range(periods)]
                })
                return pl.from_pandas(pdf) if as_polars and POLARS_AVAILABLE else pdf

            if end_date is None: end_date = datetime.now()
            rates = mt5.copy_rates_range(symbol, timeframe, start_date, end_date)
            if rates is None or len(rates) == 0: return None
            
            if as_polars and POLARS_AVAILABLE:
                return pl.from_numpy(rates).with_columns(
                    pl.from_epoch("time", time_unit="s")
                )
            else:
                df = pd.DataFrame(rates)
                df['time'] = pd.to_datetime(df['time'], unit='s')
                return df
        except Exception as e:
            logger.error(f"Error historical data: {e}")
            return None

    def get_historical_candles(self, symbol: str, timeframe: int, count: int = 100, as_polars: bool = False) -> Optional[Union[pd.DataFrame, 'pl.DataFrame']]:
        """Wrapper para últimas velas."""
        try:
            if self.simulated:
                return self.get_historical_data(symbol, timeframe, datetime.now() - timedelta(hours=count), count=count, as_polars=as_polars)
            
            rates = mt5.copy_rates_from(symbol, timeframe, datetime.now(), count)
            if rates is None or len(rates) == 0: return None
            
            if as_polars and POLARS_AVAILABLE:
                return pl.from_numpy(rates).with_columns(
                    pl.from_epoch("time", time_unit="s")
                )
            else:
                df = pd.DataFrame(rates)
                df['time'] = pd.to_datetime(df['time'], unit='s')
                return df
        except Exception as e:
            logger.error(f"Error candles: {e}")
            return None

    def execute_order(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Envía orden a MT5."""
        if self.simulated:
            return {"retcode": 10009, "status": "success", "comment": "Simulated"}
        if not self.is_connected(): return {"error": "MT5 not connected", "status": "error"}
        res = mt5.order_send(request)
        return res._asdict() if res else {"error": "Order failed", "status": "error"}

    def close_position(self, ticket: int, symbol: str, volume: float, order_type: int, price: float, magic: int = 0) -> Dict[str, Any]:
        """Cierra posición."""
        request = {
            "action": mt5.TRADE_ACTION_DEAL, "symbol": symbol, "volume": volume,
            "type": order_type, "position": ticket, "price": price, "magic": magic,
            "type_time": mt5.ORDER_TIME_GTC, "type_filling": mt5.ORDER_FILLING_IOC,
        }
        return self.execute_order(request)

    def get_positions(self) -> List[Dict[str, Any]]:
        if not self.is_connected() or self.simulated: return []
        pos = mt5.positions_get()
        return [p._asdict() for p in pos] if pos else []

# Instancia global
mt5_bridge = MT5Bridge()