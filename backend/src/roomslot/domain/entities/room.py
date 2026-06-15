from __future__ import annotations

from datetime import datetime
from uuid import UUID

import attrs.validators as av
from attrs import define, field
from attrs_validation import validators as v

from roomslot.core.exceptions import DomainError
from roomslot.domain.const import (
    ROOM_DESCRIPTION_MAX_LEN,
    ROOM_DESCRIPTION_MIN_LEN,
    ROOM_NAME_MAX_LEN,
    ROOM_NAME_MIN_LEN,
)
from roomslot.domain.enums import Building
from roomslot.domain.ports import Clock, UuidGenerator
from roomslot.domain.utils.converters import optional_strip_str
from roomslot.domain.utils.validators import int_validator


@define(frozen=True, slots=True, kw_only=True)
class Room:
    id: UUID = field(validator=v.instance_of(UUID))
    name: str = field(
        converter=str.strip,
        validator=[
            v.instance_of(str),
            v.min_len(ROOM_NAME_MIN_LEN),
            v.max_len(ROOM_NAME_MAX_LEN),
        ],
    )
    building: Building = field(validator=v.instance_of(Building))
    floor: int = field(validator=[int_validator, v.ge(1)])
    capacity: int = field(validator=[int_validator, v.ge(1)])
    description: str | None = field(
        converter=optional_strip_str,
        validator=[
            av.optional(v.instance_of(str)),
            av.optional(v.min_len(ROOM_DESCRIPTION_MIN_LEN)),
            av.optional(v.max_len(ROOM_DESCRIPTION_MAX_LEN)),
        ],
    )
    is_active: bool = field(validator=v.instance_of(bool))
    created_at: datetime = field(validator=v.instance_of(datetime))
    updated_at: datetime = field(validator=v.instance_of(datetime))

    def __attrs_post_init__(self) -> None:
        if self.updated_at < self.created_at:
            raise DomainError("Room updated_at must be greater than or equal created_at")

    @classmethod
    def create(
        cls,
        name: str,
        building: Building,
        floor: int,
        capacity: int,
        description: str | None = None,
        *,
        clock: Clock,
        uuid_generator: UuidGenerator,
    ) -> Room:
        now = clock.now()
        return Room(
            id=uuid_generator.generate(),
            name=name,
            building=building,
            floor=floor,
            capacity=capacity,
            description=description,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
