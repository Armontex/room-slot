from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from roomslot.bootstrap.engine import create_db_engine
from roomslot.bootstrap.session import create_session_factory
from roomslot.config.settings import Settings

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncGenerator[None]:
    settings: Settings = app.state.settings

    engine = create_db_engine(settings.db)
    session_maker = create_session_factory(engine)

    app.state.engine = engine
    app.state.session_maker = session_maker

    logger.info("application.started")
    try:
        yield
    finally:
        await engine.dispose()
        logger.info("application.stopped")
