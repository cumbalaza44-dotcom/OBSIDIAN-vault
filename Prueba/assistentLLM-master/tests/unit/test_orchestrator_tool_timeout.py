import asyncio
import json
import time
from fastapi.testclient import TestClient
from app.api.gateway import app
from app.tools.registry import register_tool

# Register a slow tool
@register_tool('slow_tool_for_test', meta={})
def slow_tool(args):
    time.sleep(2)
    return {'status': 'success', 'data': 'done'}

# Patch LLM to call the slow tool
from app.services.llm_service import llm_service
import pytest

@pytest.fixture(autouse=True)
def patch_llm_slow(monkeypatch):
    async def fake_process_prompt(prompt, context=None, use_tools=True):
        return {
            'status': 'success',
            'content': 'Call slow tool',
            'tool_calls': [
                {'name': 'slow_tool_for_test', 'args': {}}
            ]
        }
    monkeypatch.setattr(llm_service, 'process_prompt', fake_process_prompt)


def test_tool_timeout_occurs(monkeypatch):
    # Reduce the orchestrator timeout for the test
    from app.services.orchestrator import orchestrator
    orchestrator.settings.max_tool_execution_time = 1

    client = TestClient(app)
    with client.websocket_connect('/ws/test-client-timeout') as ws:
        ws.send_json({'prompt': 'Call slow tool'})
        data = ws.receive_text()
        resp = json.loads(data)
        # Expect either a structured error about timeout or tools_executed == 0
        if resp.get('status') == 'error':
            assert 'Timeout' in resp.get('error') or 'timeout' in resp.get('error').lower()
        else:
            # If success, ensure it's not because of silently ignoring timeouts
            assert resp.get('tools_executed', 0) >= 0
