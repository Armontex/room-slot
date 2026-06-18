from roomslot.common.types import JsonValue
from roomslot.db.models.booking import BookingModel
from roomslot.db.models.room import RoomModel
from roomslot.db.models.user import UserModel
from roomslot.domain.entities.booking import Booking
from roomslot.domain.entities.room import Room
from roomslot.domain.entities.user import User
from roomslot.domain.value_objects.email import Email
from roomslot.domain.value_objects.slot import Slot


def map_user_entity_to_model(entity: User) -> UserModel:
    return UserModel(
        id=entity.id,
        email=entity.email.value,
        hashed_password=entity.hashed_password,
        role=entity.role,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def map_user_model_to_entity(model: UserModel) -> User:
    return User(
        id=model.id,
        email=Email(model.email),
        role=model.role,
        hashed_password=model.hashed_password,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def map_room_model_to_entity(model: RoomModel) -> Room:
    return Room(
        id=model.id,
        name=model.name,
        building=model.building,
        floor=model.floor,
        capacity=model.capacity,
        description=model.description,
        is_active=model.is_active,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def map_booking_model_to_entity(model: BookingModel) -> Booking:
    return Booking(
        id=model.id,
        user_id=model.user_id,
        room_id=model.room_id,
        slot=Slot(
            date=model.booking_date,
            start=model.slot_start,
        ),
        status=model.status,
        cancelled_at=model.cancelled_at,
        created_at=model.created_at,
        updated_at=model.updated_at,
    )


def map_booking_entity_to_model(entity: Booking) -> BookingModel:
    return BookingModel(
        id=entity.id,
        user_id=entity.user_id,
        room_id=entity.room_id,
        booking_date=entity.slot.date,
        slot_start=entity.slot.start_at.time(),
        status=entity.status,
        cancelled_at=entity.cancelled_at,
        created_at=entity.created_at,
        updated_at=entity.updated_at,
    )


def map_booking_to_payload(event_type: str, entity: Booking) -> dict[str, JsonValue]:
    return {
        "type": event_type,
        "booking_id": str(entity.id),
        "room_id": str(entity.room_id),
        "user_id": str(entity.user_id),
        "date": entity.slot.date.isoformat(),
        "slot_start": entity.slot.start_at.time().isoformat(),
        "slot_end": entity.slot.end_at.time().isoformat(),
        "status": entity.status,
    }
