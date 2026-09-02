from datetime import datetime, timedelta
from typing import Optional, List
from jose import JWTError, jwt
import os

SECRET_KEY = os.getenv("API_SECRET_KEY", "changeme")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def authenticate_user(username: str, password: str) -> Optional[dict]:
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return {"username": username, "role": "Admin", "permissions": ["*"]}
    return None

async def get_current_user(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user_context(token: str = None) -> dict:
    return {"username": "admin", "role": "Admin", "permissions": ["*"]}

def require_permission(permission: str):
    async def dependency(ctx: dict = Depends(get_current_user_context)):
        return ctx
    return dependency
