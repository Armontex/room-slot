from pydantic import Field, SecretStr

from roomslot.config.base import SettingsModel


class SecuritySettings(SettingsModel):
    jwt_secret_key: SecretStr = SecretStr("some-secret-key")
    jwt_ttl_minutes: int = Field(
        default=52_560_000  # FIX: https://github.com/Armontex/room-slot/issues/2
    )
