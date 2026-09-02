import asyncpg
import os
from typing import Optional
from contextlib import asynccontextmanager

DB_POOL: Optional[asyncpg.Pool] = None

async def init_db():
    global DB_POOL
    DB_TYPE = os.getenv("DB_TYPE", "postgres")
    if DB_TYPE == "postgres":
        DB_POOL = await asyncpg.create_pool(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            database=os.getenv("POSTGRES_DB", "taskdb"),
            user=os.getenv("POSTGRES_USER", "taskuser"),
            password=os.getenv("POSTGRES_PASSWORD", "taskpassword"),
            min_size=5,
            max_size=20
        )
    return DB_POOL is not None

async def close_db():
    global DB_POOL
    if DB_POOL:
        await DB_POOL.close()

async def get_db_connection():
    global DB_POOL
    if DB_POOL is None:
        await init_db()
    return await DB_POOL.acquire()

async def release_db_connection(conn):
    global DB_POOL
    if DB_POOL:
        await DB_POOL.release(conn)

def jsonb_set(data: dict) -> str:
    import json
    return json.dumps(data)
