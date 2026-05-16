from pydantic import ValidationError
from app.tools.tool_schemas import get_schema


def test_get_historical_schema_valid():
    schema = get_schema('get_historical_data')
    inst = schema(symbol='EURUSD', timeframe='H1', count=50)
    assert inst.symbol == 'EURUSD'
    assert inst.timeframe == 'H1'
    assert inst.count == 50


def test_get_historical_schema_invalid():
    schema = get_schema('get_historical_data')
    try:
        schema(symbol=123, timeframe='H1')
        assert False, 'Validation should have failed for non-string symbol'
    except ValidationError:
        pass


def test_get_symbol_info_schema_valid():
    schema = get_schema('get_symbol_info')
    inst = schema(symbol='EURUSD')
    assert inst.symbol == 'EURUSD'


def test_run_dynamic_analysis_schema_valid():
    schema = get_schema('run_dynamic_analysis')
    inst = schema(symbol='EURUSD', timeframe='H1', strategy='ema_cross', days=3)
    assert inst.strategy == 'ema_cross'
    assert inst.days == 3


def test_run_dynamic_analysis_schema_invalid():
    schema = get_schema('run_dynamic_analysis')
    try:
        schema(symbol='EURUSD', timeframe=123, strategy='ema_cross')
        assert False, 'Validation should have failed for non-string timeframe'
    except ValidationError:
        pass
