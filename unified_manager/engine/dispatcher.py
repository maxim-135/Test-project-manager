from typing import Dict, Any, Callable, Optional
from unified_manager.logging_config import get_logger
from config import get_agent_config
import asyncio

logger = get_logger(__name__)

class Dispatcher:
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self.broadcast_fn: Optional[Callable] = None

    def register_agent(self, key: str, agent: Any):
        self.agents[key] = agent

    async def dispatch(self, agent_key: str, prompt: str, **kwargs) -> Dict[str, Any]:
        config = get_agent_config(agent_key)
        if not config:
            raise ValueError(f"Agent '{agent_key}' not found")
        logger.info(f"Dispatching to {agent_key}: {prompt[:50]}...")
        return {"agent_key": agent_key, "response": f"Response from {agent_key}"}

    async def start(self):
        logger.info("Dispatcher started")

    async def stop(self):
        logger.info("Dispatcher stopped")

    def broadcast(self, message: str):
        if self.broadcast_fn:
            asyncio.create_task(self.broadcast_fn(message))

_dispatcher: Optional[Dispatcher] = None

def get_dispatcher() -> Dispatcher:
    global _dispatcher
    if _dispatcher is None:
        _dispatcher = Dispatcher()
    return _dispatcher
