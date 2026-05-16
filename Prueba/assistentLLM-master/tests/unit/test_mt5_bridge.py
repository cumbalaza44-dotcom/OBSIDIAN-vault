import pytest
import pandas as pd
from datetime import datetime, timedelta

from app.services.mt5_bridge import MT5Bridge


def test_mt5_initialize_simulated():
    bridge = MT5Bridge(simulated=True)
    # Force simulated by ensuring MT5_AVAILABLE is False in module (it is set at import time)
    # initialize should succeed in simulated mode
    ok = bridge.initialize()
    assert ok is True
    assert bridge.initialized is True
    assert bridge.simulated is True
    acct = bridge.get_account_info()
    assert acct is not None
    assert isinstance(acct, dict)


def test_get_historical_data_simulated():
    bridge = MT5Bridge(simulated=True)
    bridge.initialize()

    start = datetime.now() - timedelta(days=1)
    df = bridge.get_historical_data("EURUSD", 16385, start, None, count=24)
    assert df is not None
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert 'time' in df.columns
    assert 'close' in df.columns
