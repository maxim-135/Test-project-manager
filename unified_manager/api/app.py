import os
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Depends, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from unified_manager.logging_config import get_logger
from unified_manager.api.logging_middleware import RequestLoggingMiddleware
from unified_manager.api.auth import (
    ADMIN_USERNAME, ADMIN_PASSWORD, create_access_token, get_current_user,
    authenticate_user, get_current_user_context, require_permission
)
from unified_manager.api import routes_tasks, routes_models, routes_orchestrator, routes_openai, routes_health, routes_agents
from unified_manager.repository.database import init_db
from unified_manager.services.agent_seeder import seed_agents_from_env
from config import load_agents_from_db
from unified_manager.engine.dispatcher import get_dispatcher
from unified_manager.api.ws_manager import ws_manager
from unified_manager.repository.user_repository import create_user, list_users
from unified_manager.domain.models import UserCreate, UserResponse

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    await init_db()
    try:
        await seed_agents_from_env()
    except Exception as exc:
        logger.warning("Agent seeding failed: %s", exc)
    try:
        await load_agents_from_db()
    except Exception as exc:
        logger.warning("load_agents_from_db failed: %s", exc)
    dispatcher = get_dispatcher()
    dispatcher.broadcast_fn = ws_manager.broadcast
    await dispatcher.start()
    logger.info("Application started successfully")
    yield
    logger.info("Shutting down application...")
    await dispatcher.stop()
    logger.info("Application shutdown complete")

app = FastAPI(
    title="Modular Task Manager API & Web Dashboard",
    version="1.0.0",
    description="REST API and Web UI for Modular Task Manager designed for AI agents.",
    lifespan=lifespan,
)

app.add_middleware(RequestLoggingMiddleware)

def get_allowed_origins():
    origins_str = os.getenv("ALLOWED_ORIGINS", "")
    if not origins_str:
        return []
    return [origin.strip() for origin in origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

RATE_LIMIT_WINDOW = 60
MAX_REQUESTS = 120
request_counts = {}

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    if client_ip not in request_counts:
        request_counts[client_ip] = []
    request_counts[client_ip] = [t for t in request_counts[client_ip] if now - t < RATE_LIMIT_WINDOW]
    if len(request_counts[client_ip]) >= MAX_REQUESTS:
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": "Rate limit exceeded. Too many requests."}
        )
    request_counts[client_ip].append(now)
    response = await call_next(request)
    return response

from fastapi import WebSocket, WebSocketDisconnect

app.include_router(routes_health.router)
app.include_router(routes_tasks.router)
app.include_router(routes_models.router)
app.include_router(routes_orchestrator.router)
app.include_router(routes_openai.router)
app.include_router(routes_agents.router)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        ws_manager.disconnect(websocket)

templates = Jinja2Templates(directory="unified_manager/api/templates")

class LoginPayload(BaseModel):
    username: str
    password: str

@app.post("/api/auth/token")
async def login_for_access_token(username: str = Form(...), password: str = Form(...)):
    user = await authenticate_user(username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={
        "sub": user["username"],
        "user_id": user.get("id"),
        "role": user["role"],
        "permissions": user["permissions"]
    })
    return {"access_token": access_token, "token_type": "bearer", "role": user["role"]}

@app.post("/api/auth/json-login")
async def login_json(payload: LoginPayload):
    user = await authenticate_user(payload.username, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    access_token = create_access_token(data={
        "sub": user["username"],
        "user_id": user.get("id"),
        "role": user["role"],
        "permissions": user["permissions"]
    })
    return {"success": True, "access_token": access_token, "role": user["role"]}

@app.get("/api/auth/me")
async def get_me(ctx: dict = Depends(get_current_user_context)):
    return {"success": True, "user": ctx}

@app.get("/api/users", dependencies=[Depends(require_permission("user:manage"))])
async def api_list_users():
    return {"success": True, "users": await list_users()}

@app.post("/api/users", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_permission("user:manage"))])
async def api_create_user(payload: UserCreate):
    try:
        new_user = await create_user(username=payload.username, password_raw=payload.password, role_name=payload.role)
        return {"success": True, "user": new_user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"User creation failed: {str(e)}")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@app.get("/", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse(request, "dashboard.html")
