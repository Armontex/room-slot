from collections.abc import Callable
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from structlog import get_logger

from roomslot.common.dto import UserBookingRead
from roomslot.common.exceptions import (
    BookingAccessDeniedError,
    BookingAlreadyCancelled,
    BookingNotFoundError,
    RoomNotFoundError,
)
from roomslot.domain.entities.booking import Booking
from roomslot.domain.enums import BookingStatus
from roomslot.domain.ports import Clock, UuidGenerator
from roomslot.domain.value_objects.slot import Slot
from roomslot.repositories.booking import BookingRepository
from roomslot.repositories.room import RoomRepository
from roomslot.services.event_publisher import EventPublisher

logger = get_logger(__name__)


class BookingService:
    def __init__(
        self,
        booking_repo_factory: Callable[[], BookingRepository],
        room_repo_factory: Callable[[AsyncSession], RoomRepository],
        clock: Clock,
        uuid_generator: UuidGenerator,
        event_publisher: EventPublisher,
    ) -> None:
        self._booking_repo_factory = booking_repo_factory
        self._room_repo_factory = room_repo_factory
        self._clock = clock
        self._uuid_generator = uuid_generator
        self._publisher = event_publisher

    async def create_booking(
        self,
        user_id: UUID,
        room_id: UUID,
        slot: Slot,
    ) -> Booking:
        logger.debug("booking.create_booking.started")
        booking_repo = self._booking_repo_factory()
        session = booking_repo.get_session()
        room_repo = self._room_repo_factory(session)

        room = await room_repo.get_by_id(room_id)
        if room is None:
            raise RoomNotFoundError("booking.create_booking.room_not_found")

        if not room.is_active:
            raise RoomNotFoundError("booking.create_booking.not_active_room")

        booking = Booking.create(
            room_id=room_id,
            user_id=user_id,
            slot=slot,
            clock=self._clock,
            uuid_generator=self._uuid_generator,
        )

        await booking_repo.add(booking)
        await session.commit()

        await self._publisher.booking_created(booking)

        logger.info("booking.create_booking.succeeded", booking_id=booking.id)

        return booking

    async def cancel_booking(
        self,
        user_id: UUID,
        booking_id: UUID,
    ) -> None:
        logger.debug("booking.cancel_booking.started")

        repo = self._booking_repo_factory()
        session = repo.get_session()

        booking = await repo.get_by_id(booking_id)

        if not booking:
            raise BookingNotFoundError("booking.cancel_booking.not_found")

        if booking.user_id != user_id:
            raise BookingAccessDeniedError("booking.cancel_booking.access_denied_error")

        if booking.status == BookingStatus.CANCELLED:
            raise BookingAlreadyCancelled("booking.cancel_booking.already_cancelled")

        booking = booking.cancel(clock=self._clock)

        await repo.update(booking)
        await session.commit()

        await self._publisher.booking_cancelled(booking)
        logger.info("booking.cancel_booking.succeeded", booking_id=booking.id)

    async def get_user_bookings(
        self,
        user_id: UUID,
        offset: int,
        limit: int,
    ) -> tuple[tuple[UserBookingRead, ...], int]:
        if offset < 0:
            raise ValueError("offset must be greater than or equal 0")
        if limit <= 0:
            raise ValueError("limit must be greater than 0")

        logger.debug("booking.get_user_bookings.started")

        repo = self._booking_repo_factory()

        bookings = await repo.get_user_bookings(user_id, offset=offset, limit=limit)
        total = await repo.get_user_bookings_count(user_id=user_id)

        return bookings, total
