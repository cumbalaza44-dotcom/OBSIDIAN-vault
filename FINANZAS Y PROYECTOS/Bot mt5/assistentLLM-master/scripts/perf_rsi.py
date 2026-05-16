"""
Pequeña prueba de rendimiento: calcular RSI en 10k filas usando data_engine fallback (pandas) o polars si está disponible.
"""
import time
import pandas as pd
import numpy as np
from app.services.data_engine import data_engine


def generate_df(n=10000):
    idx = pd.date_range('2025-01-01', periods=n, freq='T')
    close = np.cumsum(np.random.randn(n)) + 100
    df = pd.DataFrame({'time': idx, 'close': close})
    return df


def perf_rsi():
    df = generate_df(10000)
    spec = {"name": "rsi", "column": "close", "length": 14}
    t0 = time.time()
    rsi = data_engine.calculate_indicator(df, spec)
    t1 = time.time()
    print(f"RSI computed, len={len(rsi)} in {t1-t0:.3f}s")

if __name__ == '__main__':
    perf_rsi()
