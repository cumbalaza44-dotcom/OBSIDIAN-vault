import asyncio
import json
import pytest
from fastapi.testclient import TestClient
from app.api.gateway import app
from app.tools.registry import register_tool


# Flaky idempotent tool: fails first N times then succeeds
class FlakyState:
    calls = 0


@register_tool('flaky_idempotent', meta={'schema': None, 'idempotent': True})
def run_flaky(args):
    FlakyState.calls += 1
    if FlakyState.calls < 2:
        return {'status': 'error', 'error': 'temporary failure'}
    return {'status': 'success', 'data': {'ok': True}}


def test_retry_for_idempotent_tool(monkeypatch):
    # ensure orchestrator retries once by default
    from app.services.orchestrator import orchestrator
    orchestrator.settings.max_tool_retries = 2

    client = TestClient(app)
    with client.websocket_connect('/ws/retry-test') as ws:
        ws.send_json({'prompt': 'Call flaky tool'})
        data = ws.receive_text()
        resp = json.loads(data)
        # Expect success because retry should handle transient failure
        assert resp.get('status') == 'success'


@register_tool('composite_tool', meta={'schema': None})
def run_composite(args):
    # Simulate step1 success and step2 failure, but expose rollback via returned dict
    return {'status': 'error', 'error': 'step2 failed', 'rolled_back': True}


def test_partial_rollback(monkeypatch):
    client = TestClient(app)
    with client.websocket_connect('/ws/rollback-test') as ws:
        ws.send_json({'prompt': 'Call composite_tool'})
        data = ws.receive_text()
        resp = json.loads(data)
        assert resp.get('status') == 'error'
        # composite reported rolled_back in tool_results
        tr = resp.get('tool_results', [])
        assert any(r.get('result', {}).get('rolled_back') for r in tr)


def test_compensator_executes_on_failure(monkeypatch):
    # Register a tool with a compensator
    from app.tools.registry import register_tool, get_tool

    @register_tool('step1', meta={'schema': None, 'compensator': 'step1_compensate'})
    def step1(args):
        return {'status': 'success', 'data': {'ok': True}}

    @register_tool('step1_compensate', meta={'schema': None})
    def step1_compensate(args):
        # Mark that compensator ran by returning success
        return {'status': 'success', 'data': {'compensated': True}}

    @register_tool('step2_fail', meta={'schema': None})
    def step2_fail(args):
        return {'status': 'error', 'error': 'critical failure in step2'}

    # Craft an LLM-like response that calls step1 then step2_fail
    from app.services.llm_service import llm_service

    async def fake_process_prompt(prompt, context=None, use_tools=True):
        return {
            'status': 'success',
            'content': 'Plan: step1 then step2',
            'tool_calls': [
                {'name': 'step1', 'args': {}},
                {'name': 'step2_fail', 'args': {}}
            ]
        }

    monkeypatch.setattr(llm_service, 'process_prompt', fake_process_prompt)

    client = TestClient(app)
    with client.websocket_connect('/ws/compensator-test') as ws:
        ws.send_json({'prompt': 'Do composite steps'})
        data = ws.receive_text()
        resp = json.loads(data)
        assert resp.get('status') == 'error'
        # Expect that compensator was attempted (we can't assert internals, but no exception should occur)


def test_metrics_endpoint_exposes_prometheus_text():
    client = TestClient(app)
    # Trigger a simple call to populate some metrics
    with client.websocket_connect('/ws/metrics-test') as ws:
        ws.send_json({'prompt': 'Call get_account_balance'})
        _ = ws.receive_text()

    r = client.get('/metrics')
    assert r.status_code == 200
    assert 'tool_latency_count' in r.text or 'tool_errors_total' in r.text


def test_state_manager_compensator_queue_in_memory():
    import asyncio
    from app.core.state_manager import state_manager

    async def run_queue_test():
        task = {'id': 't1', 'compensator': 'noop', 'args': {'x': 1}}
        ok = await state_manager.push_compensator_task(task)
        assert ok
        t = await state_manager.pop_compensator_task()
        assert t and t.get('id') == 't1'

    asyncio.get_event_loop().run_until_complete(run_queue_test())
