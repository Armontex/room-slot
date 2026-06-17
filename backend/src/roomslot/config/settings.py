from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from roomslot.config.database import DatabaseSettings
from roomslot.config.logging import LoggingSettings
from roomslot.config.service import ServiceSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_prefix="BACKEND__",
        env_nested_delimiter="__",
        extra="ignore",
    )

    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    service: ServiceSettings = Field(default_factory=ServiceSettings)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
