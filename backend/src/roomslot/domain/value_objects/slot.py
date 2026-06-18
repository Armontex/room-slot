from __future__ import annotations

from calendar import Day
from datetime import UTC, datetime, time
from datetime import date as date_

from attrs import Attribute, define, field
from attrs_validation import validators as v

from roomslot.common.exceptions import DomainError
from roomslot.domain.const import SLOT_MAX_TIME, SLOT_MIN_TIME, SLOT_TIME_DIFFERENCE


def _validate_slot_start_time(inst: Slot, attr: Attribute[time], value: time) -> None:
    if value.minute != 0 or value.second != 0 or value.microsecond != 0:
        raise DomainError("Slot start time cannot have minutes, seconds, or microseconds")

    if value.hour not in range(SLOT_MIN_TIME, SLOT_MAX_TIME):
        raise DomainError(
            f"Slot start time must be between {SLOT_MIN_TIME}:00 and {SLOT_MAX_TIME - 1}:00"
        )


def _validate_slot_date(inst: Slot, attr: Attribute[date_], value: date_) -> None:
    if value.weekday() > Day.FRIDAY:
        raise DomainError("The slot booking date must be between Monday and Friday.")


@define(frozen=True, slots=True, kw_only=True)
class Slot:
    date: date_ = field(validator=[v.instance_of(date_), _validate_slot_date])
    _start: time = field(validator=[v.instance_of(time), _validate_slot_start_time], alias="start")

    @property
    def start_at(self) -> datetime:
        return datetime.combine(date=self.date, time=self._start, tzinfo=UTC)

    @property
    def end_at(self) -> datetime:
        return self.start_at + SLOT_TIME_DIFFERENCE
