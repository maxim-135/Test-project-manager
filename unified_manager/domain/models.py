from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime

# --- DDL SQL Queries ---

CREATE_ROLES_TABLE_PG = """
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);
"""

CREATE_USERS_TABLE_PG = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER NOT NULL REFERENCES roles (id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_PERMISSIONS_TABLE_PG = """
CREATE TABLE IF NOT EXISTS permissions (
    id SERIAL PRIMARY KEY,
    role_id INTEGER NOT NULL REFERENCES roles (id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL
);
"""

CREATE_MODULES_TABLE_PG = """
CREATE TABLE IF NOT EXISTS modules (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL,
    path VARCHAR(500) NOT NULL
);
"""

CREATE_CONTRACTS_TABLE_PG = """
CREATE TABLE IF NOT EXISTS contracts (
    id SERIAL PRIMARY KEY,
    contract_id VARCHAR(255) NOT NULL,
    provider_module VARCHAR(255) NOT NULL,
    consumer_module VARCHAR(255) NOT NULL,
    description TEXT,
    input_schema TEXT,
    output_schema TEXT,
    version VARCHAR(50)
);
"""

CREATE_TASKS_TABLE_PG = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    module_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(50),
    status VARCHAR(50),
    scope TEXT,
    resource_metrics JSONB DEFAULT '{}'::jsonb,
    extra_params JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES modules (id) ON DELETE CASCADE
);
"""

CREATE_DEPENDENCIES_TABLE_PG = """
CREATE TABLE IF NOT EXISTS dependencies (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL,
    depends_on_task_id INTEGER NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE,
    FOREIGN KEY (depends_on_task_id) REFERENCES tasks (id) ON DELETE CASCADE
);
"""

CREATE_TASK_LOGS_TABLE_PG = """
CREATE TABLE IF NOT EXISTS task_logs (
    id SERIAL PRIMARY KEY,
    task_id INTEGER NOT NULL,
    agent_key VARCHAR(100) NOT NULL,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
);
"""

CREATE_AI_AGENTS_TABLE_PG = """
CREATE TABLE IF NOT EXISTS ai_agents (
    id SERIAL PRIMARY KEY,
    agent_key VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    client VARCHAR(50) NOT NULL DEFAULT 'openai_compatible',
    base_url VARCHAR(500) NOT NULL DEFAULT '',
    api_key_encrypted TEXT DEFAULT '',
    model VARCHAR(255) NOT NULL DEFAULT 'local-default',
    system_prompt TEXT DEFAULT '',
    temperature DOUBLE PRECISION DEFAULT 0.7,
    max_tokens INTEGER DEFAULT 2048,
    is_valid INTEGER DEFAULT 0,
    is_active INTEGER DEFAULT 0,
    validation_error TEXT DEFAULT '',
    pipeline_order INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_ai_agents_agent_key ON ai_agents(agent_key);
CREATE INDEX IF NOT EXISTS idx_ai_agents_is_active ON ai_agents(is_active);
CREATE INDEX IF NOT EXISTS idx_ai_agents_pipeline_order ON ai_agents(pipeline_order);
"""

# --- Domain Enums & Entities ---

class Role(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""

class User(BaseModel):
    id: int
    username: str
    role: str
    created_at: Optional[datetime] = None

class Module(BaseModel):
    id: int
    name: str
    type: str
    path: str

class Task(BaseModel):
    id: int
    module_id: int
    title: str
    description: str
    priority: str
    status: str
    scope: str
    resource_metrics: Dict[str, Any]
    extra_params: Dict[str, Any]
    created_at: datetime
    depends_on: List[int] = Field(default_factory=list)

class GenerateRequest(BaseModel):
    agent_key: str = "orchestrator"
    prompt: str
    task_id: Optional[int] = None

class ChatCompletionRequest(BaseModel):
    model: str = "orchestrator"
    messages: List[Dict[str, str]]
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 2048
