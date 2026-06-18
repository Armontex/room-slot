from uuid import UUID

from roomslot.api.schemas.base import BaseResponse, BaseSchema, PaginatedResponse
from roomslot.domain.enums import Building


class RoomsResponseItem(BaseSchema):
    id: UUID
    name: str
    building: Building
    floor: int
    capacity: int
    description: str | None


class RoomResponse(BaseResponse):
    id: UUID
    name: str
    building: Building
    floor: int
    capacity: int
    description: str | None


class RoomsResponse(PaginatedResponse[RoomsResponseItem]): ...
