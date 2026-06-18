from datetime import date, datetime, time
from uuid import UUID

from sqlalchemy import (
    CheckConstraint,
    Computed,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    Time,
    UniqueConstraint,
    case,
    func,
    null,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from roomslot.common.providers import SystemClock
from roomslot.db.models.base import Base
from roomslot.db.models.enums import BookingStatusEnum
from roomslot.db.models.types import ID, CreatedAt, UpdatedAt
from roomslot.domain.enums import BookingStatus


class BookingModel(Base):
    __tablename__ = "bookings"

    id: Mapped[ID] = mapped_column()
    room_id: Mapped[UUID] = mapped_column(
        ForeignKey("rooms.id", ondelete="RESTRICT"),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
    )
    booking_date: Mapped[date] = mapped_column(Date, nullable=False)
    slot_start: Mapped[time] = mapped_column(Time, nullable=False)
    status: Mapped[BookingStatus] = mapped_column(
        BookingStatusEnum,
        default=BookingStatus.ACTIVE,
        server_default=text(f"'{BookingStatus.ACTIVE.value}'"),
        nullable=False,
    )
    created_at: Mapped[CreatedAt] = mapped_column(default_factory=SystemClock.now)
    updated_at: Mapped[UpdatedAt] = mapped_column(default_factory=SystemClock.now)
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        server_default=None,
    )

    active_slot_key: Mapped[str | None] = mapped_column(
        String(128),
        Computed(
            case(
                (
                    status == BookingStatus.ACTIVE.value,
                    func.concat(room_id, ":", booking_date, ":", slot_start),
                ),
                else_=null(),
            )
        ),
        init=False,
        nullable=True,
    )

    __table_args__ = (
        Index(
            None,
            room_id,
            status,
            booking_date,
            slot_start,
        ),
        Index(
            None,
            user_id,
            booking_date,
            slot_start,
        ),
        UniqueConstraint(active_slot_key),
        CheckConstraint(
            ((status == BookingStatus.ACTIVE) & cancelled_at.is_(None))
            | ((status == BookingStatus.CANCELLED) & cancelled_at.is_not(None)),
            name="booking_state",
        ),
        CheckConstraint(
            updated_at >= created_at,
            name="updated_at_ge_than_created_at",
        ),
        CheckConstraint(
            cancelled_at.is_(None) | (cancelled_at >= created_at),
            name="cancelled_at_ge_than_created_at",
        ),
    )
