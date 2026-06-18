from collections.abc import Callable
from uuid import UUID

from structlog import get_logger

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
from roomslot.services.event_publisher import EventPublisher

logger = get_logger(__name__)


class BookingService:
    def __init__(
        self,
        repo_factory: Callable[[], BookingRepository],
        clock: SystemClock,
        uuid_generator: Uuid4Generator,
        event_publisher: EventPublisher,
    ) -> None:
        self._repo_factory = repo_factory
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

        await self._publisher.booking_created(booking)

        logger.info("booking.create_booking.succeeded", booking_id=booking.id)

        return booking

    async def cancel_booking(
        self,
        user_id: UUID,
        booking_id: UUID,
    ) -> None:
        logger.debug("booking.cancel_booking.started")

        repo = self._repo_factory()
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
    ) -> tuple[Booking, ...]:
        if offset < 0:
            raise ValueError("offset must be greater than or equal 0")
        if limit <= 0:
            raise ValueError("limit must be greater than 0")

        logger.debug("booking.get_user_bookings.started")

        repo = self._repo_factory()
        return await repo.get_user_bookings(user_id, offset=offset, limit=limit)
