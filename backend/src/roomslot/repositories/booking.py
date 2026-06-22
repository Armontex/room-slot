from datetime import date
from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from roomslot.common.dto import UserBookingRead
from roomslot.common.exceptions import BookingAlreadyExists
from roomslot.common.mappers import (
    map_booking_entity_to_model,
    map_booking_model_to_entity,
    map_booking_model_to_user_booking_read,
)
from roomslot.db.models.booking import BookingModel
from roomslot.domain.entities.booking import Booking
from roomslot.domain.enums import BookingStatus
from roomslot.repositories.base import BaseRepository


class BookingRepository(BaseRepository):
    async def add(self, booking: Booking) -> None:
        model = map_booking_entity_to_model(booking)
        self._session.add(model)
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            raise BookingAlreadyExists("booking.create_booking.already_exists") from e

    async def get_by_id(self, booking_id: UUID) -> Booking | None:
        result = await self._session.get(BookingModel, booking_id)

        if result is None:
            return None

        return map_booking_model_to_entity(result)

    async def get_user_bookings(
        self,
        user_id: UUID,
        offset: int,
        limit: int,
    ) -> tuple[UserBookingRead, ...]:
        query = (
            select(BookingModel)
            .options(joinedload(BookingModel.room))
            .filter_by(user_id=user_id)
            .order_by(BookingModel.booking_date.desc(), BookingModel.slot_start.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await self._session.execute(query)

        return tuple(map_booking_model_to_user_booking_read(m) for m in result.scalars())

    async def get_user_bookings_count(self, user_id: UUID) -> int:
        query = (
            select(func.count()).select_from(BookingModel).where(BookingModel.user_id == user_id)
        )
        result = await self._session.execute(query)
        total = result.scalar_one()
        return total

    async def update(self, booking: Booking) -> None:
        stmt = (
            update(BookingModel)
            .filter_by(id=booking.id)
            .values(
                status=booking.status,
                updated_at=booking.updated_at,
                cancelled_at=booking.cancelled_at,
            )
        )
        await self._session.execute(stmt)

    async def get_active_bookings_for_room_between_dates(
        self,
        room_id: UUID,
        date_from: date,
        date_to: date,
    ) -> tuple[Booking, ...]:
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
