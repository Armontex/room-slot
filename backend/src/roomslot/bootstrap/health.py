from roomslot.common.health import HealthCheck
from roomslot.containers.container import Container
from roomslot.db.checks import check_db_connection, check_db_migrations


def build_health_checks(container: Container) -> tuple[HealthCheck, ...]:
    engine = container.db().engine()

    return (
        HealthCheck(
            name="db.connection",
            check=lambda: check_db_connection(engine),
        ),
        HealthCheck(
            name="db.migrations",
            check=lambda: check_db_migrations(engine),
        ),
    )
