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

        logger.info("redis.listener.listen", channel=self._channel)

        try:
            while True:
                message = await pubsub.get_message(  # pyright: ignore[reportUnknownVariableType]
                    ignore_subscribe_messages=True,
                    timeout=1.0,
                )
                if message is None:
                    continue

                message = cast(dict[str, JsonValue], message)
                if message["type"] != "message":
                    continue
                event = json.loads(cast(str | bytes | bytearray, message["data"]))
                if not isinstance(event, dict):
                    logger.warning("redis.listener.invalid_event", event_payload=event)
                    continue

                event = cast(dict[str, JsonValue], event)
                logger.info("redis.listener.event_received", event_payload=event)
                await self._send_event_to_subs(event)

        finally:
            await pubsub.unsubscribe(self._channel)  # pyright: ignore[reportUnknownMemberType]
            await pubsub.close()
            logger.debug("redis.listener.closed")

    async def _send_event_to_subs(self, event: dict[str, JsonValue]) -> None:
        logger.info("redis.listener.send_event_to_subs", subscribers_count=len(self._subscribers))
        for sub in self._subscribers:
            res = sub(event)
            if inspect.isawaitable(res):
                await res

    def subscribe(self, sub: Subscriber) -> None:
        self._subscribers.append(sub)
