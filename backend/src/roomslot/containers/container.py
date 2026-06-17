from dependency_injector import containers, providers

from roomslot.config.settings import Settings
from roomslot.containers.database import DatabaseContainer


class Container(containers.DeclarativeContainer):
    settings: providers.Dependency[Settings] = providers.Dependency(instance_of=Settings)

    db = providers.Container(
        DatabaseContainer,
        settings=settings.provided.db,
    )
