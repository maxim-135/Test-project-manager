#!/usr/bin/env python3
"""CLI clients for interacting with the API."""
import httpx
import json
from typing import Optional, Dict, Any


class APIClient:
    """Base API client."""
    
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.client = httpx.Client(timeout=30.0)
    
    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    def get(self, path: str) -> Dict[str, Any]:
        resp = self.client.get(f"{self.base_url}{path}", headers=self._headers())
        resp.raise_for_status()
        return resp.json()
    
    def post(self, path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        resp = self.client.post(f"{self.base_url}{path}", json=data, headers=self._headers())
        resp.raise_for_status()
        return resp.json()
    
    def close(self):
        self.client.close()


class TaskClient(APIClient):
    """Client for task operations."""
    
    def create_task(self, title: str, description: str = "", priority: int = 0) -> Dict[str, Any]:
        return self.post("/api/tasks", {"title": title, "description": description, "priority": priority})
    
    def list_tasks(self) -> Dict[str, Any]:
        return self.get("/api/tasks")
    
    def get_task(self, task_id: int) -> Dict[str, Any]:
        return self.get(f"/api/tasks/{task_id}")


class AgentClient(APIClient):
    """Client for agent operations."""
    
    def list_agents(self) -> Dict[str, Any]:
        return self.get("/api/agents")
    
    def get_agent(self, agent_id: int) -> Dict[str, Any]:
        return self.get(f"/api/agents/{agent_id}")
    
    def create_agent(self, agent_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.post("/api/agents", agent_data)


if __name__ == "__main__":
    import sys
    client = TaskClient()
    if len(sys.argv) > 1 and sys.argv[1] == "tasks":
        print(json.dumps(client.list_tasks(), indent=2))
    client.close()
