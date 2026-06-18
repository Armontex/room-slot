from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import cast

from roomslot.common.types import JsonValue


def from_timestamp(value: float) -> datetime:
    return datetime.fromtimestamp(value, UTC)


@dataclass(frozen=True, slots=True)
class TokenClaims:
    subject: str
    issued_at: datetime
    expired_at: datetime
    roles: tuple[str, ...]
    raw: dict[str, JsonValue]

    @classmethod
    def from_payload(cls, payload: dict[str, JsonValue]) -> TokenClaims:
        return TokenClaims(
            subject=cast(str, payload["sub"]),
            issued_at=from_timestamp(cast(float, payload["iat"])),
            expired_at=from_timestamp(cast(float, payload["exp"])),
            roles=tuple(cast(list[str], payload["roles"])),
            raw=payload,
        )
