from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from unified_manager.services.agent_service import list_agents, get_agent, update_agent, delete_agent, create_agent
from unified_manager.services.agent_validator import validate_agent
from unified_manager.domain.models import AgentConfigUpdate, AgentConfigCreate
from unified_manager.api.auth import require_permission

router = APIRouter(prefix="/api/agents", tags=["agents"])

@router.get("/")
async def api_list_agents(_: dict = Depends(require_permission("agent:read"))):
    agents = await list_agents()
    return {"success": True, "agents": agents}

@router.get("/{agent_key}")
async def api_get_agent(agent_key: str, _: dict = Depends(require_permission("agent:read"))):
    agent = await get_agent(agent_key)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"success": True, "agent": agent}

@router.post("/")
async def api_create_agent(payload: AgentConfigCreate, _: dict = Depends(require_permission("agent:create"))):
    agent = await create_agent(payload)
    return {"success": True, "agent": agent}

@router.put("/{agent_key}")
async def api_update_agent(agent_key: str, payload: AgentConfigUpdate, _: dict = Depends(require_permission("agent:update"))):
    agent = await update_agent(agent_key, payload)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"success": True, "agent": agent}

@router.delete("/{agent_key}")
async def api_delete_agent(agent_key: str, _: dict = Depends(require_permission("agent:delete"))):
    success = await delete_agent(agent_key)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"success": True}

@router.post("/{agent_key}/validate")
async def api_validate_agent(agent_key: str, _: dict = Depends(require_permission("agent:validate"))):
    agent = await get_agent(agent_key)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    is_valid = await validate_agent(agent_key, agent)
    return {"success": True, "is_valid": is_valid}
