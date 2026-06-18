import json
from collections.abc import AsyncIterator
from typing import cast

from redis.asyncio import Redis
from structlog import get_logger

from roomslot.common.exceptions import DomainError
from roomslot.common.types import JsonValue

logger = get_logger(__name__)


class RedisListener:
    def __init__(self, redis: Redis, channel: str) -> None:
        self._redis = redis
        self._channel = channel

    async def listen(self) -> AsyncIterator[dict[str, JsonValue]]:
        pubsub = self._redis.pubsub()  # pyright: ignore[reportUnknownMemberType]
        await pubsub.subscribe(self._channel)

        try:
            async for message in pubsub.listen():  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType]
                message = cast(dict[str, JsonValue], message)
                if message["type"] != "message":
                    continue
                event = json.loads(cast(str | bytes | bytearray, message["data"]))
                if not isinstance(event, dict):
                    raise DomainError("Event type is not dict")
                yield event
        finally:
            await pubsub.unsubscribe(self._channel)  # pyright: ignore[reportUnknownMemberType]
            await pubsub.close()
