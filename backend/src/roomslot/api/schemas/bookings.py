from datetime import date, datetime, time
from uuid import UUID

from roomslot.api.schemas.base import BaseResponse, BaseSchema, PaginatedResponse
from roomslot.domain.enums import BookingStatus


class CreateBookingRequest(BaseSchema):
    room_id: UUID
    date: date
    start_time: time


class CreateBookingResponse(BaseResponse):
    id: UUID
    room_id: UUID
    user_id: UUID
    date: date
    start_time: time
    status: BookingStatus
    created_at: datetime


class BookingSlot(BaseSchema):
    date: date
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
