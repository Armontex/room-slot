from collections.abc import Callable
from uuid import UUID

from roomslot.common.exceptions import (
    BookingAccessDeniedError,
    BookingAlreadyCancelled,
    BookingNotFoundError,
)
from roomslot.common.providers import SystemClock, Uuid4Generator
from roomslot.domain.entities.booking import Booking
from roomslot.domain.enums import BookingStatus
from roomslot.domain.value_objects.slot import Slot
from roomslot.repositories.booking import BookingRepository


class BookingService:
    def __init__(
        self,
        repo_factory: Callable[[], BookingRepository],
        clock: SystemClock,
        uuid_generator: Uuid4Generator,
    ) -> None:
        self._repo_factory = repo_factory
        self._clock = clock
        self._uuid_generator = uuid_generator

    async def create_booking(
        self,
        user_id: UUID,
        room_id: UUID,
        slot: Slot,
    ) -> Booking:
        repo = self._repo_factory()
        session = repo.get_session()

        booking = Booking.create(
            room_id=room_id,
            user_id=user_id,
            slot=slot,
            clock=self._clock,
            uuid_generator=self._uuid_generator,
        )

        await repo.add(booking)
        await session.commit()

        return booking

    async def cancel_booking(
        self,
        user_id: UUID,
        booking_id: UUID,
    ) -> None:
        repo = self._repo_factory()
        session = repo.get_session()

        booking = await repo.get_by_id(booking_id)

        if not booking:
            raise BookingNotFoundError()

        if booking.user_id != user_id:
            raise BookingAccessDeniedError()

        if booking.status == BookingStatus.CANCELLED:
            raise BookingAlreadyCancelled()

        booking = booking.cancel(clock=self._clock)

        await repo.update(booking)
        await session.commit()

    async def get_user_bookings(
        self,
        user_id: UUID,
        offset: int,
        limit: int,
    ) -> tuple[Booking, ...]:
        if offset < 0:
            raise ValueError("offset must be greater than or equal 0")
        if limit <= 0:
            raise ValueError("limit must be greater than 0")

        repo = self._repo_factory()
        return await repo.get_user_bookings(user_id, offset=offset, limit=limit)
