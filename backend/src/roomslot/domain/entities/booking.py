from __future__ import annotations

from datetime import datetime
from uuid import UUID

from attrs import define, evolve, field
from attrs_validation import validators as v

from roomslot.core.exceptions import DomainError
from roomslot.domain.enums import BookingStatus
from roomslot.domain.ports import Clock, UuidGenerator
from roomslot.domain.value_objects.slot import Slot


@define(frozen=True, slots=True, kw_only=True)
class Booking:
    id: UUID = field(validator=v.instance_of(UUID))
    room_id: UUID = field(validator=v.instance_of(UUID))
    user_id: UUID = field(validator=v.instance_of(UUID))
    slot: Slot = field(validator=v.instance_of(Slot))
    status: BookingStatus = field(validator=v.instance_of(BookingStatus))
    created_at: datetime = field(validator=v.instance_of(datetime))
    updated_at: datetime = field(validator=v.instance_of(datetime))
    cancelled_at: datetime | None = field(validator=v.instance_of(datetime | None))

    def __attrs_post_init__(self) -> None:
        if self.updated_at < self.created_at:
            raise DomainError("Booking updated_at must be greater than or equal created_at")

        if self.cancelled_at is not None and self.cancelled_at < self.created_at:
            raise DomainError("Booking cancelled_at must be greater than or equal created_at")

        if self.slot.start_at < self.created_at:
            raise DomainError("Booking cannot be created after slot start")

        self._validate_state()

    def _validate_state(self) -> None:
        if self.status == BookingStatus.ACTIVE and self.cancelled_at is not None:
            raise DomainError(
                "Impossible state. cancelled_at must be accompanied by a status of cancelled"
            )

        if self.status == BookingStatus.CANCELLED and self.cancelled_at is None:
            raise DomainError(
                "Impossible state. status of cancelled must be accompanied by a cancelled_at"
            )

    @classmethod
    def create(
        cls,
        room_id: UUID,
        user_id: UUID,
        slot: Slot,
        *,
        clock: Clock,
        uuid_generator: UuidGenerator,
    ) -> Booking:
        now = clock.now()
        return Booking(
            id=uuid_generator.generate(),
            room_id=room_id,
            user_id=user_id,
            slot=slot,
            status=BookingStatus.ACTIVE,
            created_at=now,
            updated_at=now,
            cancelled_at=None,
        )

    def cancel(self, *, clock: Clock) -> Booking:
        if self.status == BookingStatus.CANCELLED:
            raise DomainError("Booking is already cancelled")

        now = clock.now()
        return evolve(
            self,
            status=BookingStatus.CANCELLED,
            updated_at=now,
            cancelled_at=now,
        )
