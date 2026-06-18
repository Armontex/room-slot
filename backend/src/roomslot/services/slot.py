from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from enum import StrEnum
from uuid import UUID

from roomslot.common.exceptions import RoomNotFoundError
from roomslot.domain.const import SLOT_MAX_TIME, SLOT_MIN_TIME
from roomslot.domain.ports import Clock
from roomslot.domain.value_objects.slot import Slot
from roomslot.repositories.booking import BookingRepository
from roomslot.repositories.room import RoomRepository


class SlotStatus(StrEnum):
    BOOKED = "booked"
    PAST = "past"
    AVAILABLE = "available"


@dataclass(frozen=True, slots=True)
class SlotView:
    slot: Slot
    status: SlotStatus


@dataclass(frozen=True, slots=True)
class DaySlotSchedule:
    date: date
    slots: tuple[SlotView, ...]


@dataclass(frozen=True, slots=True)
class RoomSlotSchedule:
    room_id: UUID
    date_from: date
    date_to: date
    days: tuple[DaySlotSchedule, ...]


class SlotService:
    def __init__(
        self,
        room_repo_factory: Callable[[], RoomRepository],
        booking_repo_factory: Callable[[], BookingRepository],
        clock: Clock,
    ) -> None:
        self._room_repo_factory = room_repo_factory
        self._booking_repo_factory = booking_repo_factory
        self._clock = clock

    async def get_room_slots(
        self,
        room_id: UUID,
    ) -> RoomSlotSchedule:
        room_repo = self._room_repo_factory()
        room = await room_repo.get_by_id(room_id)

        if room is None or not room.is_active:
            raise RoomNotFoundError("slot.get_room_slots.room_not_found")

        now = self._clock.now()
        today = now.date()
        date_from, date_to = _get_current_booking_window(today)

        booking_repo = self._booking_repo_factory()
        bookings = await booking_repo.get_active_bookings_for_room_between_dates(
            room_id=room_id,
            date_from=date_from,
            date_to=date_to,
        )

        occupied_slots: set[Slot] = {b.slot for b in bookings}

        days: list[DaySlotSchedule] = []
        for current_date in _iter_dates(date_from, date_to):
            slots_views: list[SlotView] = []

            for slot in _generate_day_slots(current_date):
                if slot in occupied_slots:
                    status = SlotStatus.BOOKED
                elif _is_slot_in_past(slot, now):
                    status = SlotStatus.PAST
                else:
                    status = SlotStatus.AVAILABLE

                view = SlotView(slot=slot, status=status)
                slots_views.append(view)

            days.append(
                DaySlotSchedule(
                    date=current_date,
                    slots=tuple(slots_views),
                )
            )

        return RoomSlotSchedule(
            room_id=room_id,
            date_from=date_from,
            date_to=date_to,
            days=tuple(days),
        )


def _get_current_booking_window(today: date) -> tuple[date, date]:
    weekday = today.weekday()

    if weekday <= 4:
        date_from = today
        date_to = today + timedelta(days=4 - weekday)
        return date_from, date_to

    days_until_next_monday = 7 - weekday
    date_from = today + timedelta(days=days_until_next_monday)
    date_to = date_from + timedelta(days=4)
    return date_from, date_to


def _generate_day_slots(booking_date: date) -> tuple[Slot, ...]:
    return tuple(
        Slot(
            date=booking_date,
            start=time(hour),
        )
        for hour in range(SLOT_MIN_TIME, SLOT_MAX_TIME)
    )


def _iter_dates(date_from: date, date_to: date) -> Iterable[date]:
    current = date_from
    while current <= date_to:
        yield current
        current += timedelta(days=1)


def _is_slot_in_past(slot: Slot, now: datetime) -> bool:
    return slot.start_at <= now
