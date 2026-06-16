from sqlalchemy import Boolean, CheckConstraint, Integer, String, UniqueConstraint, func, true
from sqlalchemy.orm import Mapped, mapped_column, validates

from roomslot.domain.const import (
    ROOM_CAPACITY_MIN_VALUE,
    ROOM_DESCRIPTION_MAX_LEN,
    ROOM_DESCRIPTION_MIN_LEN,
    ROOM_FLOOR_MIN_VALUE,
    ROOM_NAME_MAX_LEN,
    ROOM_NAME_MIN_LEN,
)
from roomslot.domain.enums import Building
from roomslot.infra.providers import SystemClock
from roomslot.models.base import Base
from roomslot.models.enums import BuildingEnum
from roomslot.models.types import ID, CreatedAt, UpdatedAt


class RoomModel(Base):  # TODO: Добавить индексы
    __tablename__ = "rooms"

    id: Mapped[ID] = mapped_column()
    name: Mapped[str] = mapped_column(
        String(ROOM_NAME_MAX_LEN),
        nullable=False,
    )
    building: Mapped[Building] = mapped_column(BuildingEnum, nullable=False)
    floor: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(
        String(ROOM_DESCRIPTION_MAX_LEN),
        nullable=True,
        default=None,
        server_default=None,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default=true(),
    )
    created_at: Mapped[CreatedAt] = mapped_column(default=SystemClock.now)
    updated_at: Mapped[UpdatedAt] = mapped_column(default=SystemClock.now)

    __table_args__ = (
        UniqueConstraint(name, building, floor),
        CheckConstraint(
            func.char_length(func.trim(name)) >= ROOM_NAME_MIN_LEN,
            name="name_min_len",
        ),
        CheckConstraint(
            floor >= ROOM_FLOOR_MIN_VALUE,
            name="floor_min_val",
        ),
        CheckConstraint(
            capacity >= ROOM_CAPACITY_MIN_VALUE,
            name="capacity_min_val",
        ),
        CheckConstraint(
            description.is_(None)
            | (func.char_length(func.trim(description)) >= ROOM_DESCRIPTION_MIN_LEN),
            name="description_min_len_or_none",
        ),
        CheckConstraint(
            updated_at >= created_at,
            name="updated_at_ge_than_created_at",
        ),
    )

    @validates("name")
    def _normalize_name(self, _: str, value: str) -> str:
        return value.strip()

    @validates("description")
    def _normalize_description(self, _: str, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()
