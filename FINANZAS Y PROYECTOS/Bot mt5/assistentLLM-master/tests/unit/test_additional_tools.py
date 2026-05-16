import pytest
from app.tools.registry import get_tool


def test_list_open_positions_tool():
    tool = get_tool('list_open_positions')
    assert tool is not None
    res = tool['run']({})
    assert isinstance(res, dict)
    assert 'status' in res


def test_compare_volatility_tool():
    tool = get_tool('compare_volatility')
    assert tool is not None
    res = tool['run']({'symbol_a': 'EURUSD', 'symbol_b': 'GBPUSD', 'period': 14})
    assert isinstance(res, dict)
    assert 'status' in res


def test_check_correlation_tool():
    tool = get_tool('check_correlation')
    assert tool is not None
    res = tool['run']({'symbol_a': 'EURUSD', 'symbol_b': 'GBPUSD', 'period': 7})
    assert isinstance(res, dict)
    assert 'status' in res
