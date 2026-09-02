from fastapi import APIRouter, Depends
from unified_manager.domain.models import ChatCompletionRequest, ChatCompletionResponse
from unified_manager.engine.dispatcher import get_dispatcher

router = APIRouter(prefix="/v1", tags=["openai"])

@router.post("/chat/completions")
async def chat_completions(payload: ChatCompletionRequest):
    dispatcher = get_dispatcher()
    agent_key = payload.agent_key or payload.model
    result = await dispatcher.dispatch(agent_key, payload.messages[-1]["content"])
    return {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "created": 1234567890,
        "model": agent_key,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": result.get("response", "")},
            "finish_reason": "stop"
        }],
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
    }
