from fastapi import FastAPI

from roomslot.bootstrap.lifespan import lifespan
from roomslot.config.settings import get_settings
from roomslot.containers.container import Container
from roomslot.middlewares.request_logging import RequestLoggingMiddleware
from roomslot.observation.logs.setup import setup_logging


def create_app() -> FastAPI:
    settings = get_settings()

    setup_logging(settings.logging)

    container = Container(settings=settings)

    app = FastAPI(
        title=settings.service.name,
        version=settings.service.version,
        debug=False,
        lifespan=lifespan,
    )

    app.state.container = container

    app.add_middleware(
        RequestLoggingMiddleware,
        excluded_paths=settings.logging.excluded_paths,
    )

    return app
