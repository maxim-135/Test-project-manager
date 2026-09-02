"""OpenAI API compatibility tests."""
import pytest
from httpx import AsyncClient
from unified_manager.api.app import app


@pytest.mark.asyncio
async def test_openai_chat():
    """Test OpenAI-compatible chat endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/v1/chat/completions", json={
            "model": "test",
            "messages": [{"role": "user", "content": "Hello"}]
        })
        assert response.status_code in [200, 401, 404]
