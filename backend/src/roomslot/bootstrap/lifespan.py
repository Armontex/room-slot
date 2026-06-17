from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from roomslot.containers.container import Container

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    container: Container = app.state.container
    engine = container.db().engine()

    logger.info("application.started")
    try:
        yield
    finally:
        await engine.dispose()
        logger.info("application.stopped")
