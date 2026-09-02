from typing import List, Dict, Any, Optional
from unified_manager.core.db_utils import get_db_connection, jsonb_get, jsonb_set
from unified_manager.logging_config import get_logger

logger = get_logger(__name__)

async def create_task(module_id: int, title: str, description: str = "", priority: str = "Medium",
                      status: str = "Pending", scope: str = "", depends_on: Optional[List[int]] = None,
                      extra_params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    conn = await get_db_connection()
    try:
        async with conn.cursor() as cur:
            await cur.execute(
                "INSERT INTO tasks (module_id, title, description, priority, status, scope, extra_params) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (module_id, title, description, priority, status, scope, jsonb_set(extra_params or {}))
            )
            task_id = (await cur.fetchone())[0]
            if depends_on:
                for dep_id in depends_on:
                    await cur.execute(
                        "INSERT INTO dependencies (task_id, depends_on_task_id) VALUES (%s, %s)",
                        (task_id, dep_id)
                    )
            await conn.commit()
            return await get_task(task_id)
    finally:
        conn.close()

async def get_task(task_id: int) -> Optional[Dict[str, Any]]:
    conn = await get_db_connection()
    try:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
            row = await cur.fetchone()
            if not row:
                return None
            columns = [c[0] for c in cur.description]
            task = dict(zip(columns, row))
            await cur.execute("SELECT depends_on_task_id FROM dependencies WHERE task_id = %s", (task_id,))
            task["depends_on"] = [r[0] for r in await cur.fetchall()]
            return task
    finally:
        conn.close()

async def list_tasks() -> List[Dict[str, Any]]:
    conn = await get_db_connection()
    try:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            rows = await cur.fetchall()
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()

async def update_task(task_id: int, **updates) -> Optional[Dict[str, Any]]:
    conn = await get_db_connection()
    try:
        set_clauses = []
        values = []
        for key, value in updates.items():
            set_clauses.append(f"{key} = %s")
            values.append(value)
        if not set_clauses:
            return await get_task(task_id)
        values.append(task_id)
        async with conn.cursor() as cur:
            await cur.execute(f"UPDATE tasks SET {', '.join(set_clauses)} WHERE id = %s", values)
            await conn.commit()
        return await get_task(task_id)
    finally:
        conn.close()

async def delete_task(task_id: int) -> bool:
    conn = await get_db_connection()
    try:
        async with conn.cursor() as cur:
            await cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            await conn.commit()
            return cur.rowcount > 0
    finally:
        conn.close()

async def list_tasks_by_module(module_id: int) -> List[Dict[str, Any]]:
    conn = await get_db_connection()
    try:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM tasks WHERE module_id = %s ORDER BY created_at DESC", (module_id,))
            rows = await cur.fetchall()
            columns = [c[0] for c in cur.description]
            return [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()
