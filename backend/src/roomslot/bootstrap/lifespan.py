import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress

import structlog
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from roomslot.bootstrap.redis import create_redis
from roomslot.bootstrap.session import create_session_factory
from roomslot.config.settings import Settings
from roomslot.messaging.channels import BOOKING_EVENTS_CHANNEL
from roomslot.messaging.listener import RedisListener
from roomslot.ws.handlers import handle_booking_event
from roomslot.ws.room_connection_manager import RoomConnectionManager

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(
    app: FastAPI,
) -> AsyncGenerator[None]:
    settings: Settings = app.state.settings

    engine: AsyncEngine = app.state.engine
    session_maker = create_session_factory(engine)
    redis = create_redis(settings.redis)

    rcm = RoomConnectionManager()
    booking_events_listener = RedisListener(redis, BOOKING_EVENTS_CHANNEL)
    booking_events_listener.subscribe(handle_booking_event(rcm))

    booking_event_listener_task = asyncio.create_task(booking_events_listener.listen())

    app.state.session_maker = session_maker
    app.state.room_connection_manager = rcm
    app.state.redis = redis

    logger.info("application.started")
    try:
        yield
    finally:
        booking_event_listener_task.cancel()
        with suppress(asyncio.CancelledError):
            await booking_event_listener_task

        await engine.dispose()
        await redis.close()
        logger.info("application.stopped")
