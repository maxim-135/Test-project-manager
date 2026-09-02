from fastapi import APIRouter, Depends
from unified_manager.domain.models import ModelListResponse, ModelInfo

router = APIRouter(prefix="/v1", tags=["models"])

@router.get("/models")
async def list_models():
    return ModelListResponse(data=[
        ModelInfo(id="orchestrator"),
        ModelInfo(id="coder"),
        ModelInfo(id="auditor"),
        ModelInfo(id="coder_power"),
    ])
