from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator
from pydantic.networks import RedisDsn


class RedisSettings(BaseModel):
    model_config = ConfigDict(frozen=True)

    host: str = "redis"
    port: int = 6379
    db: int = 0
    password: str | None = Field(default=None, min_length=1)

    @field_validator("password", mode="before")
    @classmethod
    def empty_password_to_none(cls, value: str | None) -> str | None:
        if value == "":
            return None
        return value

    @computed_field
    @property
    def url(self) -> str:
        return str(
            RedisDsn.build(
                scheme="redis",
                host=self.host,
                port=self.port,
                path=str(self.db),
                password=self.password,
            )
        )
