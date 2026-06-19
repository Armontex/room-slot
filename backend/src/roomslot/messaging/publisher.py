import json

from redis.asyncio import Redis
from structlog import get_logger

from roomslot.common.types import JsonValue

logger = get_logger(__name__)


class RedisPublisher:
    def __init__(self, redis: Redis, channel: str) -> None:
        self._redis = redis
        self._channel = channel

    async def publish(self, payload: dict[str, JsonValue]) -> None:
        await self._redis.publish(self._channel, json.dumps(payload))  # pyright: ignore[reportUnknownMemberType]
        logger.info(
            "redis.publisher.succeeded",
            payload=payload,
        )
