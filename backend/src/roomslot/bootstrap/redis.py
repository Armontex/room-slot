from redis.asyncio import Redis

from roomslot.config.redis import RedisSettings


def create_redis(redis_settings: RedisSettings) -> Redis:
    return Redis.from_url(  # pyright: ignore[reportUnknownMemberType]
        redis_settings.url,
        decode_responses=False,
    )
