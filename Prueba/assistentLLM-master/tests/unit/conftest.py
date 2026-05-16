import pytest


def pytest_configure(config):
    """Ensure basic tools are registered for tests when heavy deps (pandas/mt5) are missing."""
    try:
        from app.tools.registry import list_tools, register_tool, get_tool

        # If registry is empty, register lightweight stubs
        if not list_tools():
            TOOL_META = {"name": "get_account_balance", "description": "stub", "args": {}}

            @register_tool("get_account_balance", TOOL_META)
            def _stub_get_account_balance(args):
                return {"status": "success", "data": {"balance": 1000}}

            TOOL_META2 = {"name": "get_symbol_price", "description": "stub", "args": {}}

            @register_tool("get_symbol_price", TOOL_META2)
            def _stub_get_symbol_price(args):
                return {"status": "success", "data": {"symbol": args.get('symbol', 'EURUSD'), "price": 1.2345}}

            TOOL_META3 = {"name": "calculate_rsi", "description": "stub", "args": {}}

            @register_tool("calculate_rsi", TOOL_META3)
            def _stub_calculate_rsi(args):
                return {"status": "success", "data": {"rsi": 50}}
    except Exception:
        # If registry import fails, tests that depend on tools will fail later and show root cause
        pass
