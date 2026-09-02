from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from unified_manager.logging_config import get_logger
import time

logger = get_logger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        start_time = time.time()
        method = request.method
        url = request.url.path

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                status_code = message["status"]
            elif message["type"] == "http.response.body":
                duration = time.time() - start_time
                logger.info(f"{method} {url} - {status_code} - {duration:.3f}s")
            await send(message)

        await self.app(scope, receive, send_wrapper)
