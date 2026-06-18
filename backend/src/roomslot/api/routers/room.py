from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from roomslot.api.routers.dependencies import get_room_service
from roomslot.api.schemas.base import PaginationQuery
from roomslot.api.schemas.rooms import RoomResponse, RoomsResponse, RoomsResponseItem
from roomslot.services.room import RoomService

router = APIRouter(prefix="/rooms", tags=["Rooms"])

RoomServiceDepend = Annotated[RoomService, Depends(get_room_service)]


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=RoomsResponse,
)
async def get_rooms(
    query: Annotated[PaginationQuery, Depends()],
    service: RoomServiceDepend,
) -> RoomsResponse:
    rooms, total = await service.get_rooms(
        offset=query.offset,
        limit=query.limit,
    )
    return RoomsResponse(
        items=[
            RoomsResponseItem(
                id=r.id,
                name=r.name,
                building=r.building,
                floor=r.floor,
                capacity=r.capacity,
                description=r.description,
            )
            for r in rooms
        ],
        total=total,
        limit=query.limit,
        offset=query.offset,
    )


@router.get(
    path="/{room_id}",
    status_code=status.HTTP_200_OK,
    response_model=RoomResponse,
)
async def get_room(
    room_id: UUID,
    service: RoomServiceDepend,
) -> RoomResponse:
    room = await service.get_room(room_id)
    return RoomResponse(
        id=room.id,
        name=room.name,
        building=room.building,
        floor=room.floor,
        capacity=room.capacity,
        description=room.description,
    )
