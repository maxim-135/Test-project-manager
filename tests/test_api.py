import pytest
from httpx import AsyncClient
from unified_manager.api.app import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/health")
        assert response.status_code == 200

@pytest.mark.asyncio
async def test_login():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/auth/token", data={
            "username": "admin",
            "password": "admin"
        })
        assert response.status_code in [200, 401]
