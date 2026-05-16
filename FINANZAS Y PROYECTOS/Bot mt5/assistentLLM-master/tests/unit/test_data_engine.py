import pandas as pd
import numpy as np
from app.services.data_engine import DataEngine


def test_to_polars_and_indicator():
    de = DataEngine()
    # crear dataframe simple
    n = 50
    df = pd.DataFrame({
        'time': pd.date_range('2025-01-01', periods=n, freq='H'),
        'close': np.linspace(1.0, 2.0, n)
    })

    # Test calculate ema in fallback (polars may not be available)
    ema = de.calculate_indicator(df, {"name": "ema", "column": "close", "length": 5})
    assert ema is not None
    assert len(ema) == n

    # Test rsi fallback
    rsi = de.calculate_indicator(df, {"name": "rsi", "column": "close", "length": 5})
    assert rsi is not None
    assert len(rsi) == n
