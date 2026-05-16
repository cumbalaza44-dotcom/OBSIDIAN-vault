import pytest
import asyncio
from datetime import datetime, timedelta

from app.core.state_manager import StateManager


@pytest.mark.asyncio
async def test_session_lifecycle():
    sm = StateManager()
    initialized = await sm.initialize()
    assert initialized is True

    # Create session
    session = await sm.create_session("client1", {"foo": "bar"})
    assert session["client_id"] == "client1"
    assert session["metadata"]["foo"] == "bar"

    # Get session
    got = await sm.get_session("client1")
    assert got is not None
    assert got["client_id"] == "client1"

    # Update session
    updated = await sm.update_session("client1", {"status": "custom"})
    assert updated is True
    got2 = await sm.get_session("client1")
    assert got2["status"] == "custom"

    # Add message and history
    added = await sm.add_message("client1", {"role": "user", "content": "hola"})
    assert added is True
    history = await sm.get_conversation_history("client1")
    assert isinstance(history, list)
    assert len(history) == 1
    assert history[0]["content"] == "hola"

    # Add operation and fetch
    op_added = await sm.add_operation("op1", {"type": "test"})
    assert op_added is True
    op = await sm.get_operation("op1")
    assert op is not None
    assert op["operation_id"] == "op1"

    # Get metrics
    metrics = await sm.get_system_metrics()
    assert "total_sessions" in metrics
    assert metrics["total_sessions"] >= 1

    # Close session
    closed = await sm.close_session("client1")
    assert closed is True
    got3 = await sm.get_session("client1")
    # get_session returns session (cached) even if closed; ensure status == closed
    assert got3 is not None
    assert got3["status"] == "closed"


@pytest.mark.asyncio
async def test_cleanup_expired_sessions():
    sm = StateManager()
    await sm.initialize()
    s = await sm.create_session("old_client")
    # Manually set last_activity to >1 hour ago
    s["last_activity"] = (datetime.now() - timedelta(hours=2)).isoformat()
    sm.sessions["old_client"] = s

    # Run cleanup
    await sm.cleanup_expired_sessions()

    # Session should be marked closed
    sess = await sm.get_session("old_client")
    assert sess is not None
    assert sess.get("status") == "closed"
