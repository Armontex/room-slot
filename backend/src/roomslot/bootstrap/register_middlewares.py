from fastapi import FastAPI

from roomslot.api.middlewares.request_logging import RequestLoggingMiddleware
from roomslot.config.settings import Settings


def register_middlewares(app: FastAPI, settings: Settings) -> None:

    app.add_middleware(
        RequestLoggingMiddleware,
        excluded_methods=settings.logging.excluded_methods,
        excluded_paths=settings.logging.excluded_paths,
    )
