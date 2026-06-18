from uuid import UUID

from sqlalchemy import func, select

from roomslot.common.mappers import map_room_model_to_entity
from roomslot.db.models.room import RoomModel
from roomslot.domain.entities.room import Room
from roomslot.repositories.base import BaseRepository


class RoomRepository(BaseRepository):
    async def get_rooms(
        self,
        offset: int,
        limit: int,
        only_active: bool = True,
    ) -> tuple[Room, ...]:
        query = (
            select(RoomModel)
            .filter_by(is_active=only_active)
            .offset(offset)
            .order_by(RoomModel.building, RoomModel.floor, RoomModel.name)
            .limit(limit)
        )
        result = await self._session.execute(query)

        return tuple(map_room_model_to_entity(m) for m in result.scalars())

    async def get_count_rooms(self, only_active: bool = True) -> int:
        query = (
            select(func.count()).select_from(RoomModel).where(RoomModel.is_active.is_(only_active))
        )
        result = await self._session.execute(query)
        total = result.scalar_one()
        return total

    async def get_by_id(self, id: UUID) -> Room | None:
        result = await self._session.get(RoomModel, id)

        if result is None:
            return None

        return map_room_model_to_entity(result)
