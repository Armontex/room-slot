from calendar import Day
from datetime import date as date_
from datetime import datetime, time
from uuid import UUID

from pydantic import field_validator

from roomslot.api.schemas.base import BaseResponse, BaseSchema, PaginatedResponse
from roomslot.domain.enums import BookingStatus


class CreateBookingRequest(BaseSchema):
    room_id: UUID
    date: date_
    start_time: time

    @field_validator("date")
    @classmethod
    def validate_date(cls, value: date_) -> date_:
        if value.weekday() > Day.FRIDAY:
            raise ValueError("The slot booking date must be between Monday and Friday.")
        return value

    @field_validator("start_time")
    @classmethod
    def validate_start_time(cls, value: time) -> time:
        if value.minute != 0 or value.second != 0 or value.microsecond != 0:
            raise ValueError("Slot start time must be a full hour")

        if value.hour not in range(10, 19):
            raise ValueError("Slot start time must be between 10:00 and 18:00")

        return value


class CreateBookingResponse(BaseResponse):
    id: UUID
    room_id: UUID
    user_id: UUID
    date: date_
    start_time: time
    status: BookingStatus
    created_at: datetime


class BookingSlot(BaseSchema):
    date: date_
    start_time: time


class BookingsItem(BaseSchema):
    id: UUID
    room_id: UUID
    user_id: UUID
    slot: BookingSlot
    status: BookingStatus
    created_at: datetime
    cancelled_at: datetime | None


class MeBookingsResponse(PaginatedResponse[BookingsItem]): ...
