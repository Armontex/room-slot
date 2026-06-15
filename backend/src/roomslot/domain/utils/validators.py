from __future__ import annotations

from calendar import Day
from datetime import date, time
from typing import TYPE_CHECKING

import attrs_validation as v
from attrs import Attribute
from attrs.validators import and_

from roomslot.core.exceptions import DomainError
from roomslot.domain.const import SLOT_MAX_TIME, SLOT_MIN_TIME

if TYPE_CHECKING:
    from roomslot.domain.value_objects.slot import Slot

int_validator = and_(
    v.instance_of(int),
    v.not_(v.instance_of(bool)),
)


def validate_slot_start_time(inst: Slot, attr: Attribute[time], value: time) -> None:
    if value.minute != 0 or value.second != 0 or value.microsecond != 0:
        raise DomainError("Slot start time cannot have minutes, seconds, or microseconds")

    if value.hour not in range(SLOT_MIN_TIME, SLOT_MAX_TIME):
        raise DomainError(
            f"Slot start time must be between {SLOT_MIN_TIME}:00 and {SLOT_MAX_TIME - 1}:00"
        )


def validate_slot_date(inst: Slot, attr: Attribute[date], value: date) -> None:
    if value.weekday() > Day.FRIDAY:
        raise DomainError("The slot booking date must be between Monday and Friday.")
