from collections.abc import Callable
from uuid import UUID

from structlog import get_logger

from roomslot.common.exceptions import RoomNotFoundError
from roomslot.domain.entities.room import Room
from roomslot.repositories.room import RoomRepository

logger = get_logger(__name__)


class RoomService:
    def __init__(
        self,
        repo_factory: Callable[[], RoomRepository],
    ) -> None:
        self._repo_factory = repo_factory

    async def get_rooms(
        self,
        offset: int,
        limit: int,
    ) -> tuple[Room, ...]:
        if offset < 0:
            raise ValueError("offset must be greater than or equal 0")
        if limit <= 0:
            raise ValueError("limit must be greater than 0")

        logger.debug("room.get_rooms.started")

        repo = self._repo_factory()

        return await repo.get_rooms(offset=offset, limit=limit)

    async def get_room(self, id: UUID) -> Room:
        logger.debug("room.get_room.started")

        repo = self._repo_factory()
        room = await repo.get_by_id(id)

        if room is None:
            raise RoomNotFoundError()

        return room
