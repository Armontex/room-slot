from datetime import UTC, datetime
from uuid import UUID, uuid4


class SystemClock:
    @staticmethod
    def now() -> datetime:
        return datetime.now(UTC)


class Uuid4Generator:
    @staticmethod
    def generate() -> UUID:
        return uuid4()
