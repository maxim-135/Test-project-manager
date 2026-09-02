from typing import Optional
from unified_manager.core.database import get_db_connection, release_db_connection
from unified_manager.logging_config import get_logger

logger = get_logger(__name__)

class StateManager:
    def __init__(self):
        self._state = {}

    async def get(self, key: str, default=None):
        return self._state.get(key, default)

    async def set(self, key: str, value):
        self._state[key] = value

    async def delete(self, key: str):
        if key in self._state:
            del self._state[key]

_state_manager: Optional[StateManager] = None

def get_state_manager() -> StateManager:
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager
