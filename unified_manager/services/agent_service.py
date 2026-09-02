from typing import Dict, Any, List, Optional
from unified_manager.logging_config import get_logger
from config import AGENT_CONFIG

logger = get_logger(__name__)

async def list_agents() -> List[Dict[str, Any]]:
    return [{"agent_key": k, **v} for k, v in AGENT_CONFIG.items()]

async def get_agent(agent_key: str) -> Optional[Dict[str, Any]]:
    config = AGENT_CONFIG.get(agent_key)
    if not config:
        return None
    return {"agent_key": agent_key, **config}

async def create_agent(payload: Any) -> Dict[str, Any]:
    from config import add_agent_config
    config = add_agent_config(payload.agent_key, payload.dict())
    return {"agent_key": payload.agent_key, **config}

async def update_agent(agent_key: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    from config import update_agent_config
    try:
        config = update_agent_config(agent_key, updates)
        return {"agent_key": agent_key, **config}
    except ValueError:
        return None

async def delete_agent(agent_key: str) -> bool:
    from config import delete_agent_config
    return delete_agent_config(agent_key)
