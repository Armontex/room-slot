from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from roomslot.api.routers.dependencies import UserDepend, get_booking_service
from roomslot.api.schemas.base import PaginationQuery
from roomslot.api.schemas.bookings import (
    BookingsItem,
    BookingSlot,
    CreateBookingRequest,
    CreateBookingResponse,
    MeBookingsResponse,
    RoomItem,
)
from roomslot.domain.value_objects.slot import Slot
from roomslot.services.booking import BookingService

bookings_router = APIRouter(prefix="/bookings", tags=["Bookings"])
me_router = APIRouter(prefix="/me", tags=["Me"])
BookingServiceDepend = Annotated[BookingService, Depends(get_booking_service)]


@bookings_router.post(
    path="",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateBookingResponse,
)
async def create_booking(
    user: UserDepend,
    body: CreateBookingRequest,
    service: BookingServiceDepend,
) -> CreateBookingResponse:
    booking = await service.create_booking(
        user.id,
        room_id=body.room_id,
        slot=Slot(
            date=body.date,
            start=body.start_time,
        ),
    )

    return CreateBookingResponse(
        id=booking.id,
        room_id=booking.room_id,
        user_id=booking.user_id,
        date=booking.slot.date,
        start_time=booking.slot.start_at.time(),
        status=booking.status,
        created_at=booking.created_at,
    )


@bookings_router.post(
    path="/{booking_id}/cancel",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def cancel_booking(
    user: UserDepend,
    booking_id: UUID,
    service: BookingServiceDepend,
) -> None:
    await service.cancel_booking(
        user_id=user.id,
        booking_id=booking_id,
    )


@me_router.get(
    path="/bookings",
    status_code=status.HTTP_200_OK,
    response_model=MeBookingsResponse,
)
async def me_bookings(
    user: UserDepend,
    query: Annotated[PaginationQuery, Depends()],
    service: BookingServiceDepend,
) -> MeBookingsResponse:
    bookings, total = await service.get_user_bookings(
        user_id=user.id,
        offset=query.offset,
        limit=query.limit,
    )

    return MeBookingsResponse(
        total=total,
        offset=query.offset,
        limit=query.limit,
        items=[
            BookingsItem(
                id=b.booking.id,
                user_id=b.booking.user_id,
                room=RoomItem(
                    id=b.room.id,
                    name=b.room.name,
                    building=b.room.building,
                ),
                slot=BookingSlot(
                    date=b.booking.slot.date,
                    start_time=b.booking.slot.start_at.time(),
                ),
                created_at=b.booking.created_at,
                cancelled_at=b.booking.cancelled_at,
                status=b.booking.status,
            )
            for b in bookings
        ],
    )
