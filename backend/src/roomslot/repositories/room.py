from uuid import UUID

from sqlalchemy import select

from roomslot.common.mappers import map_room_model_to_entity
from roomslot.db.models.room import RoomModel
from roomslot.domain.entities.room import Room
from roomslot.repositories.base import BaseRepository


class RoomRepository(BaseRepository):
    async def get_rooms(
        self, offset: int, limit: int, only_active: bool = True
    ) -> tuple[Room, ...]:
        if offset < 0:
            raise ValueError("offset must be greater than or equal 0")
        if limit <= 0:
            raise ValueError("limit must be greater than 0")

        query = (
            select(RoomModel)
            .filter_by(is_active=only_active)
            .offset(offset)
            .order_by(RoomModel.building, RoomModel.floor, RoomModel.name)
            .limit(limit)
        )
        result = await self._session.execute(query)

        return tuple(map_room_model_to_entity(m) for m in result.scalars())

    async def get_by_id(self, id: UUID) -> Room | None:
        result = await self._session.get(RoomModel, id)

        if result is None:
            return None

        return map_room_model_to_entity(result)
