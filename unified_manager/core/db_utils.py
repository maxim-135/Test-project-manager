import asyncpg
import os
from typing import Optional

DB_POOL: Optional[asyncpg.Pool] = None

async def get_db_connection():
    global DB_POOL
    if DB_POOL is None:
        DB_POOL = await asyncpg.create_pool(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            database=os.getenv("POSTGRES_DB", "taskdb"),
            user=os.getenv("POSTGRES_USER", "taskuser"),
            password=os.getenv("POSTGRES_PASSWORD", "taskpassword"),
            min_size=5,
            max_size=20
        )
    return await DB_POOL.acquire()

def jsonb_get(data: str, key: str):
    import json
    return json.loads(data).get(key, {})

def jsonb_set(data: dict) -> str:
    import json
    return json.dumps(data)
