from pydantic import Field, computed_field
from pydantic.networks import MySQLDsn

from roomslot.config.base import SettingsModel

ASYNC_DRIVER = "asyncmy"
SYNC_DRIVER = "pymysql"
DBMS = "mysql"


class DatabaseSettings(SettingsModel):
    host: str = "mysql"
    port: int = Field(default=3306, ge=1, le=65535)

    alembic_host: str | None = None

    name: str = Field(default="roomslot", min_length=1)
    user: str = Field(default="mysql", min_length=1)
    password: str = Field(default="mysql", min_length=1)

    echo: bool = False

    @computed_field
    @property
    def async_url(self) -> str:
        return str(
            MySQLDsn.build(
                scheme=f"{DBMS}+{ASYNC_DRIVER}",
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                path=self.name,
            )
        )

    @computed_field
    @property
    def sync_url(self) -> str:
        return str(
            MySQLDsn.build(
                scheme=f"{DBMS}+{SYNC_DRIVER}",
                host=self.host,
                port=self.port,
                username=self.user,
                password=self.password,
                path=self.name,
            )
        )

    @computed_field
    @property
    def alembic_url(self) -> str:
        host = self.alembic_host or self.host
        return str(
            MySQLDsn.build(
                scheme=f"{DBMS}+{SYNC_DRIVER}",
                host=host,
                port=self.port,
                username=self.user,
                password=self.password,
                path=self.name,
            )
        )
