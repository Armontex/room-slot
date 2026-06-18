from collections import defaultdict
from uuid import UUID

from fastapi import WebSocket
from structlog import get_logger

from roomslot.common.types import JsonValue

logger = get_logger(__name__)


class RoomConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[UUID, set[WebSocket]] = defaultdict(set)

    async def connect(self, room_id: UUID, ws: WebSocket) -> None:
        await ws.accept()
        self._connections[room_id].add(ws)
        logger.debug(
            "websocket.room.new_connection",
            room_id=room_id,
        )

    def disconnect(self, room_id: UUID, ws: WebSocket) -> None:
        connections = self._connections.get(room_id)

        if connections is None:
            return

        connections.discard(ws)

        if not connections:
            del self._connections[room_id]

        logger.debug(
            "websocket.room.disconnect",
            room_id=room_id,
        )

    async def broadcast_to_room(self, room_id: UUID, message: dict[str, JsonValue]) -> None:
        connections = tuple(self._connections.get(room_id, ()))

        for ws in connections:
            try:
                await ws.send_json(message)
            except Exception as e:
                logger.warning(
                    "websocket.room.broadcast_failed",
                    room_id=str(room_id),
                    error=str(e),
                )
                self.disconnect(room_id, ws)
