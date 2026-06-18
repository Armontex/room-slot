from collections.abc import Awaitable, Callable, Sequence
from time import perf_counter

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from roomslot.logging.policy import access_log_level_for_status

logger = structlog.get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        *,
        excluded_paths: Sequence[str],
        excluded_methods: Sequence[str],
    ) -> None:
        super().__init__(app)
        self._excluded_paths = set(excluded_paths)
        self._excluded_methods = set(excluded_methods)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        started_at = perf_counter()
        response = await call_next(request)
        duration_ms = round((perf_counter() - started_at) * 1000, 2)

        if (request.url.path in self._excluded_paths) or (request.method in self._excluded_methods):
            return response

        level = access_log_level_for_status(response.status_code)

        logger.log(
            level,
            "http.request.completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        return response
