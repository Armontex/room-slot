from datetime import date, time
from uuid import UUID

from roomslot.api.schemas.base import BaseResponse, BaseSchema
from roomslot.services.slot import SlotStatus


class DaySlotsResponseItem(BaseSchema):
    time: time
    status: SlotStatus


class DayResponseItem(BaseSchema):
    date: date
    slots: list[DaySlotsResponseItem]


class SlotsResponse(BaseResponse):
    room_id: UUID
    date_from: date
    date_to: date
    days: list[DayResponseItem]
