from dependency_injector import containers, providers

from roomslot.config.database import DatabaseSettings
from roomslot.infra.db.engine import create_db_engine
from roomslot.infra.db.session import create_session_factory


class DatabaseContainer(containers.DeclarativeContainer):
    settings = providers.Dependency(instance_of=DatabaseSettings)

    engine = providers.Singleton(
        create_db_engine,
        settings=settings,
    )

    session_factory = providers.Singleton(
        create_session_factory,
        engine=engine,
    )
