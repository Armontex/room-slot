from abc import ABC, abstractmethod
from datetime import timedelta

from redis.asyncio import Redis


class RedisCache(ABC):
    def __init__(self, client: Redis) -> None:
        self._client = client

    @property
    @abstractmethod
    def namespace(self) -> str:
        raise NotImplementedError

    def _key(self, value: object) -> str:
        return f"{self.namespace}:{value}"

    async def set_marker(self, key: str, ttl: timedelta, value: str = "1") -> None:
        ttl_seconds = max(int(ttl.total_seconds()), 1)
        await self._client.set(name=key, value=value, ex=ttl_seconds)

    async def has_key(self, key: str) -> bool:
        return bool(await self._client.exists(key))
