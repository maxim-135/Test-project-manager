"""Live model integration test."""
import pytest
from unified_manager.services.agent_service import AgentService


@pytest.mark.asyncio
async def test_live_model():
    """Test with live model."""
    service = AgentService()
    agents = await service.list_agents()
    assert isinstance(agents, list)
