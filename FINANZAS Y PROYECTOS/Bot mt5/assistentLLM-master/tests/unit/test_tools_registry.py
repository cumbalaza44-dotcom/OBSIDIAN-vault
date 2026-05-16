import pytest
from app.tools.registry import get_tool, list_tools


def test_registry_has_tools():
    tools = list_tools()
    assert 'get_account_balance' in tools
    assert 'get_symbol_price' in tools
    assert 'calculate_rsi' in tools


def test_get_account_balance_tool():
    tool = get_tool('get_account_balance')
    assert tool is not None
    res = tool['run']({})
    assert isinstance(res, dict)


def test_get_symbol_price_tool():
    tool = get_tool('get_symbol_price')
    assert tool is not None
    res = tool['run']({'symbol': 'EURUSD'})
    assert isinstance(res, dict)

@pytest.mark.parametrize('args', [({'symbol': 'EURUSD'}), ({'symbol': 'GBPUSD', 'length': 14, 'count': 24})])
def test_calculate_rsi_tool(args):
    tool = get_tool('calculate_rsi')
    assert tool is not None
    res = tool['run'](args)
    assert isinstance(res, dict)
    # puede devolver error si no hay datos; al menos debe ser dict con status
    assert 'status' in res
