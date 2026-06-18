from structlog import get_logger

from roomslot.common.mappers import map_booking_to_payload
from roomslot.domain.entities.booking import Booking
from roomslot.messaging.publisher import RedisPublisher

logger = get_logger(__name__)


class EventPublisher:
    def __init__(
        self,
        publisher: RedisPublisher,
    ) -> None:
        self._publisher = publisher

    async def booking_created(self, booking: Booking) -> None:
        payload = map_booking_to_payload(booking)
        await self._publisher.publish(payload)
        logger.info(
            "event_publisher.booking_created.published",
            booking_id=booking.id,
        )

    async def booking_cancelled(self, booking: Booking) -> None:
        payload = map_booking_to_payload(booking)
        await self._publisher.publish(payload)
        logger.info(
            "event_publisher.booking_cancelled.published",
            booking_id=booking.id,
        )
