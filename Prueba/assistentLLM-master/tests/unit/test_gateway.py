import pytest
import json
from fastapi.testclient import TestClient
from app.api.gateway import app


client = TestClient(app)


def test_root_health():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "running"


def test_websocket_valid_and_invalid():
    with client.websocket_connect("/ws/test_client") as websocket:
        # Send invalid JSON
        websocket.send_text("not a json")
        data = websocket.receive_text()
        parsed = json.loads(data)
        assert parsed["status"] == "error"
        assert "Formato JSON inválido" in parsed["error"] or "Formato JSON" in parsed.get("error", "")

        # Send valid JSON without prompt
        websocket.send_text(json.dumps({"foo": "bar"}))
        data = websocket.receive_text()
        parsed = json.loads(data)
        assert parsed["status"] == "error"
        assert "prompt" in parsed["error"] or "Campo 'prompt' requerido" in parsed.get("error", "")

        # Send valid JSON with prompt
        websocket.send_text(json.dumps({"prompt": "¿Cuál es el estado de mi cuenta?"}))
        data = websocket.receive_text()
        parsed = json.loads(data)
        # The orchestrator may return an error because services are not fully initialized, but must return JSON
        assert isinstance(parsed, dict)
