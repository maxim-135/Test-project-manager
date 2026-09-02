from typing import List, Dict, Any, Optional
from unified_manager.core.db_utils import get_db_connection
from unified_manager.logging_config import get_logger

logger = get_logger(__name__)

async def create_user(username: str, password_raw: str, role_name: str) -> Dict[str, Any]:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    password_hash = pwd_context.hash(password_raw)
    conn = await get_db_connection()
    try:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id FROM roles WHERE name = %s", (role_name,))
            row = await cur.fetchone()
            if not row:
                raise ValueError(f"Role '{role_name}' not found")
            role_id = row[0]
            await cur.execute(
                "INSERT INTO users (username, password_hash, role_id) VALUES (%s, %s, %s) RETURNING id",
                (username, password_hash, role_id)
            )
            user_id = (await cur.fetchone())[0]
            await conn.commit()
            return {"id": user_id, "username": username, "role": role_name}
    finally:
        conn.close()

async def list_users() -> List[Dict[str, Any]]:
    conn = await get_db_connection()
    try:
        async with conn.cursor() as cur:
            await cur.execute("SELECT u.id, u.username, r.name as role FROM users u JOIN roles r ON u.role_id = r.id")
            rows = await cur.fetchall()
            return [{"id": r[0], "username": r[1], "role": r[2]} for r in rows]
    finally:
        conn.close()
