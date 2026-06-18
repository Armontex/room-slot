from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from roomslot.config.database import DatabaseSettings

DB_CONNECT_TIMEOUT_SECONDS = 3.0


def create_db_engine(settings: DatabaseSettings) -> AsyncEngine:
    return create_async_engine(
        url=settings.async_url,
        echo=settings.echo,
        pool_pre_ping=True,
        connect_args={
            "connect_timeout": DB_CONNECT_TIMEOUT_SECONDS,
            "read_timeout": DB_CONNECT_TIMEOUT_SECONDS,
        },
    )
