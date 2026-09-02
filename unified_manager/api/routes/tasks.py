from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from unified_manager.repository.task_repository import (
    create_task, get_task, list_tasks, update_task, delete_task, list_tasks_by_module
)
from unified_manager.domain.models import TaskCreateRequest, TaskUpdateRequest
from unified_manager.api.auth import require_permission
from unified_manager.logging_config import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def api_create_task(payload: TaskCreateRequest, _: dict = Depends(require_permission("task:create"))):
    task = await create_task(
        module_id=payload.module_id,
        title=payload.title,
        description=payload.description,
        priority=payload.priority,
        status=payload.status,
        scope=payload.scope,
        depends_on=payload.depends_on,
        extra_params=payload.extra_params
    )
    return {"success": True, "task": task}

@router.get("/{task_id}")
async def api_get_task(task_id: int, _: dict = Depends(require_permission("task:read"))):
    task = await get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True, "task": task}

@router.get("/")
async def api_list_tasks(module_id: Optional[int] = None, _: dict = Depends(require_permission("task:read"))):
    if module_id:
        tasks = await list_tasks_by_module(module_id)
    else:
        tasks = await list_tasks()
    return {"success": True, "tasks": tasks}

@router.put("/{task_id}")
async def api_update_task(task_id: int, payload: TaskUpdateRequest, _: dict = Depends(require_permission("task:update"))):
    task = await update_task(task_id, **payload.dict(exclude_unset=True))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True, "task": task}

@router.delete("/{task_id}")
async def api_delete_task(task_id: int, _: dict = Depends(require_permission("task:delete"))):
    success = await delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True}
