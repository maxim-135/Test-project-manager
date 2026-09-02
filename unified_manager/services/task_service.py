import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class TaskService:
    """Service for task operations."""
    
    async def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task."""
        from unified_manager.repository.task_repository import TaskRepository
        repo = TaskRepository()
        return await repo.create_task(
            title=task_data.get("title"),
            description=task_data.get("description", ""),
            priority=task_data.get("priority", 0)
        )
    
    async def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """Get a task by ID."""
        from unified_manager.repository.task_repository import TaskRepository
        repo = TaskRepository()
        return await repo.get_task(task_id)
    
    async def list_tasks(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """List tasks with pagination."""
        from unified_manager.repository.task_repository import TaskRepository
        repo = TaskRepository()
        return await repo.list_tasks(limit=limit, offset=offset)
    
    async def update_task(self, task_id: int, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Update a task."""
        from unified_manager.repository.task_repository import TaskRepository
        repo = TaskRepository()
        return await repo.update_task(task_id, updates)
    
    async def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        from unified_manager.repository.task_repository import TaskRepository
        repo = TaskRepository()
        return await repo.delete_task(task_id)
