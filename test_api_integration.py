"""API integration tests."""
import pytest
from httpx import AsyncClient
from unified_manager.api.app import app


@pytest.mark.asyncio
async def test_api_health():
    """Test health endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_api_tasks_list():
    """Test tasks list endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/tasks")
        assert response.status_code == 200
