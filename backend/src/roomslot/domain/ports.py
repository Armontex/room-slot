from datetime import datetime
from typing import Protocol
from uuid import UUID


class Clock(Protocol):
    @staticmethod
    def now() -> datetime: ...


class UuidGenerator(Protocol):
    @staticmethod
    def generate() -> UUID: ...
