from fastapi import APIRouter
from unified_manager.engine.dispatcher import get_dispatcher
from unified_manager.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/orchestrator", tags=["orchestrator"])

@router.post("/generate")
async def api_generate(prompt: str, agent_key: str = "orchestrator"):
    dispatcher = get_dispatcher()
    result = await dispatcher.dispatch(agent_key, prompt)
    return {"success": True, "result": result}
