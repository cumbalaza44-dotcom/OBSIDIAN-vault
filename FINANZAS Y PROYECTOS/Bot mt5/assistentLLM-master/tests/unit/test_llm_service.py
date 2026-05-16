import pytest

from app.services.llm_service import LLMService, GOOGLE_AI_AVAILABLE


def test_build_prompt_and_simulation():
    llm = LLMService()
    # No inicialización de la librería externa aquí; probamos _build_prompt y modos internos
    prompt = "¿Cuál es el balance de mi cuenta?"
    full_prompt = llm._build_prompt(prompt, {"extra": "info"})
    assert "Usuario: ¿Cuál es el balance" in full_prompt or "Usuario: ¿Cul es el balance" in full_prompt


@pytest.mark.asyncio
async def test_process_prompt_simulated(monkeypatch):
    llm = LLMService()

    # For simulation, mark as initialized and provide a fake model
    llm.initialized = True

    class FakeModel:
        async def generate_content(self, prompt):
            class Resp:
                text = "Simulated response"
                candidates = []
            return Resp()

    llm.model = FakeModel()

    res = await llm.process_prompt("Hola", {"ctx": 1}, use_tools=False)
    assert res["status"] == "success"
    assert "Simulated response" in res["content"]
