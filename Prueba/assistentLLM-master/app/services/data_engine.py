"""
DataEngine - Implementación de alto rendimiento basada en Polars y Numba.
Optimizado para el procesamiento masivo de datos financieros.
"""
import logging
from typing import Dict, Any, Optional, Union
import numpy as np
import pandas as pd

try:
    import polars as pl
    POLARS_AVAILABLE = True
except ImportError:
    POLARS_AVAILABLE = False

try:
    import numba as nb
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False

logger = logging.getLogger(__name__)

if NUMBA_AVAILABLE:
    @nb.njit
    def _rsi_numba(arr: np.ndarray, length: int) -> np.ndarray:
        """Cálculo de RSI acelerado con Numba."""
        n = arr.shape[0]
        rsi = np.full(n, np.nan, dtype=np.float64)
        if n <= length:
            return rsi
            
        gains = np.zeros(n, dtype=np.float64)
        losses = np.zeros(n, dtype=np.float64)
        
        for i in range(1, n):
            diff = arr[i] - arr[i-1]
            if diff > 0:
                gains[i] = diff
            else:
                losses[i] = -diff
                
        # Primer promedio (SMA)
        avg_gain = 0.0
        avg_loss = 0.0
        for i in range(1, length + 1):
            avg_gain += gains[i]
            avg_loss += losses[i]
        avg_gain /= length
        avg_loss /= length
        
        if avg_loss == 0:
            rsi[length] = 100.0
        else:
            rs = avg_gain / avg_loss
            rsi[length] = 100.0 - (100.0 / (1.0 + rs))
            
        # Promedios suavizados (Wilder's Smoothing)
        for i in range(length + 1, n):
            avg_gain = (avg_gain * (length - 1) + gains[i]) / length
            avg_loss = (avg_loss * (length - 1) + losses[i]) / length
            
            if avg_loss == 0:
                rsi[i] = 100.0
            else:
                rs = avg_gain / avg_loss
                rsi[i] = 100.0 - (100.0 / (1.0 + rs))
                
        return rsi

class DataEngine:
    """Motor de procesamiento de datos optimizado."""
    
    def __init__(self):
        self.use_polars = POLARS_AVAILABLE
        self.use_numba = NUMBA_AVAILABLE
        if not self.use_polars:
            logger.warning("Polars no está disponible. Usando Pandas (más lento).")

    def ensure_polars(self, df: Union[pd.DataFrame, 'pl.DataFrame']) -> 'pl.DataFrame':
        """Asegura que el dato sea un DataFrame de Polars."""
        if not self.use_polars:
            return df
        if isinstance(df, pl.DataFrame):
            return df
        return pl.from_pandas(df)

    def calculate_indicator(self, df: Union[pd.DataFrame, 'pl.DataFrame'], spec: Dict[str, Any]) -> Union[pd.Series, 'pl.Series']:
        """
        Calcula un indicador técnico de forma eficiente.
        """
        name = spec.get("name", "").lower()
        col = spec.get("column", "close")
        length = int(spec.get("length", 14))
        
        if self.use_polars:
            return self._calculate_polars(df, name, col, length)
        else:
            return self._calculate_pandas(df, name, col, length)

    def _calculate_polars(self, df: Union[pd.DataFrame, 'pl.DataFrame'], name: str, col: str, length: int) -> 'pl.Series':
        """Cálculo usando Polars."""
        ldf = self.ensure_polars(df)
        
        if name == "ema":
            # Polars tiene ewm_mean nativo
            return ldf.select(
                pl.col(col).ewm_mean(span=length, adjust=False)
            ).to_series()
            
        elif name == "rsi":
            if self.use_numba:
                # Numba es más rápido para RSI (Wilder's Smoothing es iterativo)
                arr = ldf[col].to_numpy()
                res = _rsi_numba(arr, length)
                return pl.Series(res)
            else:
                # Implementación nativa Polars (aproximación SMA)
                diff = pl.col(col).diff()
                gain = pl.when(diff > 0).then(diff).otherwise(0.0)
                loss = pl.when(diff < 0).then(-diff).otherwise(0.0)
                
                avg_gain = gain.rolling_mean(window_size=length)
                avg_loss = loss.rolling_mean(window_size=length)
                
                rs = avg_gain / (avg_loss + 1e-12)
                rsi = 100 - (100 / (1 + rs))
                return ldf.select(rsi).to_series()
                
        elif name == "sma":
            return ldf.select(pl.col(col).rolling_mean(window_size=length)).to_series()
            
        else:
            raise ValueError(f"Indicador '{name}' no soportado en Polars")

    def _calculate_pandas(self, df: pd.DataFrame, name: str, col: str, length: int) -> pd.Series:
        """Fallback a Pandas."""
        if name == "ema":
            return df[col].ewm(span=length, adjust=False).mean()
        elif name == "rsi":
            delta = df[col].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=length).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=length).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))
        elif name == "sma":
            return df[col].rolling(window=length).mean()
        else:
            raise ValueError(f"Indicador '{name}' no soportado en Pandas")

# Instancia global
data_engine = DataEngine()
