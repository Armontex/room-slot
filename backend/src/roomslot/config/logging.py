import logging
from enum import StrEnum
from http import HTTPMethod
from typing import Any

from pydantic import Field, field_validator

from roomslot.config.base import SettingsModel
from roomslot.config.types import EnvList

DEFAULT_EXCLUDED_ACCESS_LOG_PATHS: frozenset[str] = frozenset(
    {
        "/health/live",
        "/health/ready",
        "/metrics",
    }
)

DEFAULT_EXCLUDED_ACCESS_LOG_METHODS: frozenset[HTTPMethod] = frozenset(
    {
        HTTPMethod.OPTIONS,
    }
)


class LogLevel(StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    def to_logging(self) -> int:
        match self:
            case LogLevel.DEBUG:
                return logging.DEBUG
            case LogLevel.INFO:
                return logging.INFO
            case LogLevel.WARNING:
                return logging.WARNING
            case LogLevel.ERROR:
                return logging.ERROR
            case LogLevel.CRITICAL:
                return logging.CRITICAL


class LogFormat(StrEnum):
    JSON = "JSON"
    CONSOLE = "CONSOLE"


class LoggingSettings(SettingsModel):
    log_level: LogLevel = Field(default=LogLevel.INFO)
    log_format: LogFormat = Field(default=LogFormat.JSON)
    excluded_paths: EnvList[str] = Field(
        default_factory=lambda: list(DEFAULT_EXCLUDED_ACCESS_LOG_PATHS)
    )
    excluded_methods: EnvList[HTTPMethod] = Field(
        default_factory=lambda: list(DEFAULT_EXCLUDED_ACCESS_LOG_METHODS)
    )

    @field_validator("log_level", "log_format", mode="before")
    @classmethod
    def uppercase_enum_value(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.upper()
        return value
