from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from roomslot.config.database import DatabaseSettings


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="BACKEND",
        env_nested_delimiter="__",
        extra="ignore",
    )

    db: DatabaseSettings = Field(default_factory=DatabaseSettings)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
