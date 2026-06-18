import json

from redis.asyncio import Redis

from roomslot.common.types import JsonValue


class RedisPublisher:
    def __init__(self, redis: Redis, channel: str) -> None:
        self._redis = redis
        self._channel = channel

    async def publish(self, payload: dict[str, JsonValue]) -> None:
        await self._redis.publish(self._channel, json.dumps(payload))  # pyright: ignore[reportUnknownMemberType]
