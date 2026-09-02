from typing import Dict, Any
from unified_manager.logging_config import get_logger

logger = get_logger(__name__)

async def validate_agent(agent_key: str, config: Dict[str, Any]) -> bool:
    logger.info(f"Validating agent: {agent_key}")
    return True
