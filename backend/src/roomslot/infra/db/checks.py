from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.sql import text

from roomslot.errors import DatabaseMigrationError

ALEMBIC_INI = "alembic.ini"
ALEMBIC_VERSION_TABLE = "alembic_version"


async def check_db_connection(engine: AsyncEngine) -> None:
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))


async def check_db_migrations(engine: AsyncEngine) -> None:
    expected_heads = set(_get_alembic_heads())

    if not expected_heads:
        return

    async with engine.connect() as conn:
        has_version_table = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).has_table(ALEMBIC_VERSION_TABLE)
        )

        if not has_version_table:
            raise DatabaseMigrationError("alembic_version table does not exist")

        result = await conn.execute(text("SELECT version_num FROM alembic_version"))
        current_heads = set(result.scalars().all())

    if current_heads != expected_heads:
        raise DatabaseMigrationError(
            f"database migrations are not up to date: current={sorted(current_heads)},"
            f"expected={sorted(expected_heads)}"
        )


def _get_alembic_heads() -> tuple[str, ...]:
    config = Config(ALEMBIC_INI)
    script = ScriptDirectory.from_config(config)
    return tuple(script.get_heads())
