import os
from typing import Dict, Any, Optional

# --- Database Configuration ---
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "taskdb")
POSTGRES_USER = os.getenv("POSTGRES_USER", "taskuser")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "taskpassword")

def get_current_db_type():
    return os.getenv("DB_TYPE", "postgres")

# --- Agent Configuration ---
# API-ключи и URL читаются из переменных окружения для безопасности.

AGENT_CONFIG: Dict[str, Dict[str, Any]] = {
    "orchestrator": {
        "client": os.getenv("ORCHESTRATOR_CLIENT", "llama_cpp"),
        "base_url": os.getenv("ORCHESTRATOR_BASE_URL", "http://127.0.0.1:8081"),
        "api_key": os.getenv("ORCHESTRATOR_API_KEY", ""),
        "model": os.getenv("ORCHESTRATOR_MODEL", "Gemma-4-12b-it-qat-q4_0.gguf"),
        "system_prompt": os.getenv(
            "ORCHESTRATOR_SYSTEM_PROMPT",
            "Ты — Оркестратор. Твоя задача: проанализировать поставленную задачу, "
            "разбить её на подзадачи и распределить между ролями."
        ),
        "temperature": float(os.getenv("ORCHESTRATOR_TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("ORCHESTRATOR_MAX_TOKENS", "2048")),
    },
    "coder": {
        "client": os.getenv("CODER_CLIENT", "llama_cpp"),
        "base_url": os.getenv("CODER_BASE_URL", "http://127.0.0.1:8081"),
        "api_key": os.getenv("CODER_API_KEY", ""),
        "model": os.getenv("CODER_MODEL", "Gemma-4-12b-it-qat-q4_0.gguf"),
        "system_prompt": os.getenv(
            "CODER_SYSTEM_PROMPT",
            "Ты — Кодер. Твоя задача: написать чистый, эффективный код."
        ),
        "temperature": float(os.getenv("CODER_TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("CODER_MAX_TOKENS", "2048")),
    },
    "auditor": {
        "client": os.getenv("AUDITOR_CLIENT", "openai_compatible"),
        "base_url": os.getenv("AUDITOR_BASE_URL", "https://ai.api.cloud.yandex.net/v1"),
        "api_key": os.getenv("AUDITOR_API_KEY", os.getenv("OPENROUTER_API_KEY", "")),
        "model": os.getenv("AUDITOR_MODEL", "gpt-oss-120b"),
        "system_prompt": os.getenv(
            "AUDITOR_SYSTEM_PROMPT",
            "Ты — Аудитор. Проверь код на ошибки и уязвимости."
        ),
        "temperature": float(os.getenv("AUDITOR_TEMPERATURE", "0.3")),
        "max_tokens": int(os.getenv("AUDITOR_MAX_TOKENS", "2048")),
    },
    "coder_power": {
        "client": os.getenv("CODER_POWER_CLIENT", "openai_compatible"),
        "base_url": os.getenv("CODER_POWER_BASE_URL", "https://ai.api.cloud.yandex.net/v1"),
        "api_key": os.getenv("CODER_POWER_API_KEY", os.getenv("OPENROUTER_API_KEY", "")),
        "model": os.getenv("CODER_POWER_MODEL", "gpt-oss-120b"),
        "system_prompt": os.getenv(
            "CODER_POWER_SYSTEM_PROMPT",
            "Ты — Инженер. Реши сложную техническую проблему."
        ),
        "temperature": float(os.getenv("CODER_POWER_TEMPERATURE", "0.5")),
        "max_tokens": int(os.getenv("CODER_POWER_MAX_TOKENS", "4096")),
    },
}

PIPELINE_ORDER = ["orchestrator", "coder", "auditor", "coder_power"]

def get_agent_configs() -> Dict[str, Dict[str, Any]]:
    return AGENT_CONFIG

def get_agent_config(agent_key: str) -> Optional[Dict[str, Any]]:
    return AGENT_CONFIG.get(agent_key)

def update_agent_config(agent_key: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    if agent_key not in AGENT_CONFIG:
        raise ValueError(f"Agent '{agent_key}' not found")
    allowed_fields = {"client", "base_url", "api_key", "model", "system_prompt", "temperature", "max_tokens"}
    for key, value in updates.items():
        if key in allowed_fields:
            AGENT_CONFIG[agent_key][key] = value
    return AGENT_CONFIG[agent_key]

def add_agent_config(agent_key: str, config: Dict[str, Any]) -> Dict[str, Any]:
    if agent_key in AGENT_CONFIG:
        raise ValueError(f"Agent '{agent_key}' already exists")
    AGENT_CONFIG[agent_key] = config
    return AGENT_CONFIG[agent_key]

def delete_agent_config(agent_key: str) -> bool:
    if agent_key in AGENT_CONFIG:
        del AGENT_CONFIG[agent_key]
        if agent_key in PIPELINE_ORDER:
            PIPELINE_ORDER.remove(agent_key)
        return True
    return False

def mask_api_key(key: str) -> str:
    if not key or len(key) <= 8:
        return "***"
    return key[:4] + "..." + key[-4:]

def _agent_row_to_config(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "client": row.get("client", "openai_compatible"),
        "base_url": row.get("base_url", ""),
        "api_key": row.get("api_key", ""),
        "model": row.get("model", "local-default"),
        "system_prompt": row.get("system_prompt", ""),
        "temperature": float(row.get("temperature", 0.7)),
        "max_tokens": int(row.get("max_tokens", 2048)),
        "display_name": row.get("display_name", row.get("agent_key", "")),
        "is_valid": bool(row.get("is_valid", 0)),
        "is_active": bool(row.get("is_active", 0)),
        "id": row.get("id"),
    }

async def load_agents_from_db() -> bool:
    global AGENT_CONFIG, PIPELINE_ORDER
    try:
        from unified_manager.repository import agent_repository
        agents = await agent_repository.get_active_agents()
        if not agents:
            return False
        new_config: Dict[str, Dict[str, Any]] = {}
        new_order: list = []
        for a in agents:
            new_config[a["agent_key"]] = _agent_row_to_config(a)
            new_order.append(a["agent_key"])
        AGENT_CONFIG.clear()
        AGENT_CONFIG.update(new_config)
        PIPELINE_ORDER.clear()
        PIPELINE_ORDER.extend(new_order)
        return True
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning("load_agents_from_db failed: %s", exc)
        return False
