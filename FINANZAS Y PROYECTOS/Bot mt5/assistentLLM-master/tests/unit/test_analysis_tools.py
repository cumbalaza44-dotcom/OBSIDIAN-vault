import pytest
from datetime import datetime, timedelta
from app.services.analysis_tools import run_dynamic_analysis
from app.services.mt5_bridge import MT5Bridge, mt5_bridge


@pytest.mark.asyncio
async def test_run_dynamic_analysis_rsi():
    # Ensure mt5_bridge is in simulated mode
    # mt5_bridge is a global instance; we will force simulated behavior
    bridge = MT5Bridge(simulated=True)
    bridge.initialize()

    # Monkeypatch the global mt5_bridge used by analysis_tools
    import app.services.analysis_tools as at
    at.mt5_bridge = bridge

    args = {
        "days": 1,
        "indicators": [
            {"name": "rsi", "column": "close", "length": 14, "output": "RSI14"}
        ],
        "conditions": [],
        "output_columns": ["time", "open", "high", "low", "close", "RSI14"]
    }

    res = await run_dynamic_analysis("EURUSD", "H1", args)
    assert isinstance(res, dict)
    assert res.get("status") == "success"
    assert "data" in res
    assert "events" in res["data"]


@pytest.mark.asyncio
async def test_run_dynamic_analysis_missing_indicators():
    args = {
        "days": 1,
        "indicators": [],
    }
    res = await run_dynamic_analysis("EURUSD", "H1", args)
    assert res.get('status') == 'error'
    assert 'No se especificaron indicadores' in res.get('error', '')
