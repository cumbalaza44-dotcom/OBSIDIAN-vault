import json
import pytest
from fastapi.testclient import TestClient
from app.api.gateway import app

from app.services.llm_service import llm_service
# Force import of real orchestrator so gateway doesn't fallback to fake one during tests
from app.services import orchestrator as _orchestrator_module

# Monkeypatch llm to return invalid tool args
@pytest.fixture(autouse=True)
def patch_llm_invalid(monkeypatch):
    async def fake_process_prompt(prompt, context=None, use_tools=True):
        return {
            'status': 'success',
            'content': 'Plan with invalid args',
            'tool_calls': [
                {'name': 'get_historical_data', 'args': {'symbol': 123, 'timeframe': 456}}
            ]
        }
    monkeypatch.setattr(llm_service, 'process_prompt', fake_process_prompt)


def test_orchestrator_rejects_invalid_tool_call_ws():
    client = TestClient(app)
    with client.websocket_connect('/ws/test-client') as ws:
        ws.send_json({'prompt': 'Dame datos historicos'})
        data = ws.receive_text()
        resp = json.loads(data)
        assert resp.get('status') == 'error' or (resp.get('tools_executed') == 0)
        # If error, ensure details mention argumentos inválidos
        if resp.get('status') == 'error':
            assert 'Argumentos' in resp.get('error') or 'invalid' in resp.get('error').lower()
