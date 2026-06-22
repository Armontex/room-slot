from pydantic import Field, SecretStr

from roomslot.config.base import SettingsModel


class AdminSettings(SettingsModel):
    secret_key: SecretStr = Field(default=SecretStr("your-secret-key"), min_length=1)
    username: str = Field(default="admin", min_length=1)
    password: SecretStr = Field(default=SecretStr("admin123"), min_length=6)
