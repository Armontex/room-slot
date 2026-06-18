import inspect
import json
from collections.abc import Awaitable, Callable
from typing import cast

from redis.asyncio import Redis
from structlog import get_logger

from roomslot.common.types import JsonValue

logger = get_logger(__name__)

Subscriber = Callable[[dict[str, JsonValue]], None | Awaitable[None]]


class RedisListener:
    def __init__(self, redis: Redis, channel: str) -> None:
        self._redis = redis
        self._channel = channel
        self._subscribers: list[Subscriber] = []

    async def listen(self) -> None:
        pubsub = self._redis.pubsub()  # pyright: ignore[reportUnknownMemberType]
        await pubsub.subscribe(self._channel)

        logger.debug("redis.listener.listen")

        try:
            async for message in pubsub.listen():  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
                message = cast(dict[str, JsonValue], message)
                if message["type"] != "message":
                    continue
                event = json.loads(cast(str | bytes | bytearray, message["data"]))
                if not isinstance(event, dict):
                    logger.warning("redis.listener.invalid_event", event=event)
                    continue

                event = cast(dict[str, JsonValue], event)
                await self._send_event_to_subs(event)

        finally:
            await pubsub.unsubscribe(self._channel)  # pyright: ignore[reportUnknownMemberType]
            await pubsub.close()
            logger.debug("redis.listener.closed")

    async def _send_event_to_subs(self, event: dict[str, JsonValue]) -> None:
        for sub in self._subscribers:
            res = sub(event)
            if inspect.isawaitable(res):
                await res

    def subscribe(self, sub: Subscriber) -> None:
        self._subscribers.append(sub)
