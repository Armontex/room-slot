from datetime import date
from uuid import UUID

from sqlalchemy import select

from roomslot.common.mappers import map_booking_model_to_entity
from roomslot.db.models.booking import BookingModel
from roomslot.domain.entities.booking import Booking
from roomslot.domain.enums import BookingStatus
from roomslot.repositories.base import BaseRepository


class BookingRepository(BaseRepository):
    async def get_active_bookings_for_room_between_dates(
        self,
        room_id: UUID,
        date_from: date,
        date_to: date,
    ) -> tuple[Booking, ...]:
        if date_to < date_from:
            raise ValueError("date_to must be greater than or equal date_from")

        query = (
            select(BookingModel)
            .where(
                BookingModel.room_id == room_id,
                BookingModel.status == BookingStatus.ACTIVE,
                BookingModel.booking_date >= date_from,
                BookingModel.booking_date <= date_to,
            )
            .order_by(BookingModel.booking_date, BookingModel.slot_start)
        )

        result = await self._session.execute(query)

        return tuple(map_booking_model_to_entity(m) for m in result.scalars())
