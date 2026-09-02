import pytest
from httpx import AsyncClient
from unified_manager.api.app import app


@pytest.mark.asyncio
async def test_final_integration():
    """Final integration test."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200
