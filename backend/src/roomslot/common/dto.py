from dataclasses import dataclass

from roomslot.domain.entities.booking import Booking
from roomslot.domain.entities.room import Room


@dataclass(frozen=True, slots=True)
class UserBookingRead:
    booking: Booking
    room: Room
