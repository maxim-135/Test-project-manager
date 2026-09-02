import os
import asyncio
from typing import Optional

from unified_manager.core.database import init_db, close_db, get_db_connection
from unified_manager.domain.models import CREATE_TABLES_PG, CREATE_TABLES_SQLITE


def get_db_url() -> str:
    db_type = os.getenv("DB_TYPE", "postgres")
    if db_type == "postgres":
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        db = os.getenv("POSTGRES_DB", "taskdb")
        user = os.getenv("POSTGRES_USER", "taskuser")
        password = os.getenv("POSTGRES_PASSWORD", "taskpassword")
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
    else:
        return "sqlite+aiosqlite:///./unified_manager/data/taskdb.db"


async def run_migrations():
    """Run database migrations."""
    await init_db()
    
    db_type = os.getenv("DB_TYPE", "postgres")
    conn = await get_db_connection()
    
    try:
        if db_type == "postgres":
            for statement in CREATE_TABLES_PG.split(";"):
                statement = statement.strip()
                if statement:
                    await conn.execute(statement)
        else:
            for statement in CREATE_TABLES_SQLITE.split(";"):
                statement = statement.strip()
                if statement:
                    await conn.execute(statement)
        print("Migrations completed successfully.")
    finally:
        await conn.close()
        await close_db()


if __name__ == "__main__":
    asyncio.run(run_migrations())
