import enum
from typing import Any

from sqlalchemy import Enum

from roomslot.domain.enums import BookingStatus, Building, UserRole


def _enum_values(enum_cls: type[enum.Enum]) -> list[str]:
    return [str(member.value) for member in enum_cls]


class SqlEnum(Enum):
    def __init__(self, *enums: str | type[enum.Enum], **kw: Any) -> None:
        kw.setdefault("native_enum", False)
        kw.setdefault("validate_strings", True)
        kw.setdefault("values_callable", _enum_values)
        super().__init__(*enums, **kw)  # pyright: ignore[reportArgumentType, reportCallIssue]


UserRoleEnum = SqlEnum(UserRole)
BuildingEnum = SqlEnum(Building)
BookingStatusEnum = SqlEnum(BookingStatus)
