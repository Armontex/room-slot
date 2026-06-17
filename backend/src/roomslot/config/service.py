from pydantic import Field

from roomslot.config.base import SettingsModel


class ServiceSettings(SettingsModel):
    name: str = Field(default="RoomSlot")
    version: str = Field(default="0.1.0", pattern=r"^\d+\.\d+\.\d+$")
    description: str | None = Field(default=None)
