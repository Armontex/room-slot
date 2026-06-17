from roomslot.db.models.room import RoomModel
from roomslot.db.models.user import UserModel
from roomslot.domain.entities.room import Room
from roomslot.domain.entities.user import User
from roomslot.domain.value_objects.email import Email


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
