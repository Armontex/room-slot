from datetime import date as date_
from datetime import datetime, time

from attrs import define, field
from attrs_validation import validators as v

from roomslot.core.const import LOCAL_TZ
from roomslot.domain.const import SLOT_TIME_DIFFERENCE
from roomslot.domain.utils.validators import validate_slot_date, validate_slot_start_time


@define(frozen=True, slots=True, kw_only=True)
class Slot:
    date: date_ = field(validator=[v.instance_of(date_), validate_slot_date])
    _start: time = field(validator=[v.instance_of(time), validate_slot_start_time], alias="start")

    @property
    def start_at(self) -> datetime:
        return datetime.combine(date=self.date, time=self._start, tzinfo=LOCAL_TZ)

    @property
    def end_at(self) -> datetime:
        return self.start_at + SLOT_TIME_DIFFERENCE
