import time

from typing import Callable, Awaitable

from fastapi import Request, Response

from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(end_time)
        return response
