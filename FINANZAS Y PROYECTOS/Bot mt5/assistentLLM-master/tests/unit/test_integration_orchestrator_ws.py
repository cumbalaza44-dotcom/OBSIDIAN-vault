import asyncio
import json
from pydantic import BaseModel, Field
import pytest
from fastapi.testclient import TestClient
from app.api.gateway import app, get_orchestrator, manager

# Import registry to register a test tool
from app.tools.registry import register_tool, _TOOLS

# Mock LLM service
from app.services.llm_service import llm_service


class HistoricalArgs(BaseModel):
    symbol: str = Field(...)
    timeframe: str = Field(...)


# Register a simple test tool that returns a deterministic result
@register_tool('test_get_historical', meta={'schema': HistoricalArgs})
def run_test_tool(args):
    # Return a fake dataframe-like dict
    return {'status': 'success', 'data': {'symbol': args.get('symbol'), 'timeframe': args.get('timeframe'), 'rows': 10}}


@pytest.fixture(autouse=True)
def patch_llm(monkeypatch):
    async def fake_process_prompt(prompt, context=None, use_tools=True):
        # Simulate LLM returning a plan that calls our test tool
        return {
            'status': 'success',
            'content': 'Plan to get historical data',
            'tool_calls': [
                {'name': 'test_get_historical', 'args': {'symbol': 'EURUSD', 'timeframe': 'H1'}}
            ]
        }

    monkeypatch.setattr(llm_service, 'process_prompt', fake_process_prompt)


def test_websocket_orchestrator_flow():
    client = TestClient(app)
    with client.websocket_connect('/ws/test-client') as websocket:
        websocket.send_json({'prompt': 'Dame datos historicos de EURUSD H1'})
        data = websocket.receive_text()
        resp = json.loads(data)
        assert resp.get('status') == 'success'
        assert 'content' in resp
        # Since LLM is mocked, tool execution should have happened and tools_executed > 0
        assert isinstance(resp.get('tools_executed', 0), int)
