from collections.abc import Awaitable, Callable
from uuid import UUID

from structlog import get_logger

from roomslot.common.types import JsonValue
from roomslot.ws.room_connection_manager import RoomConnectionManager

logger = get_logger(__name__)


def handle_booking_event(
    manager: RoomConnectionManager,
) -> Callable[[dict[str, JsonValue]], Awaitable[None]]:
    async def handler(event: dict[str, JsonValue]) -> None:
        try:
            room_id = UUID(str(event.get("room_id")))
        except ValueError as e:
            logger.warning("handle_booking_event.invalid_uuid", exc=str(e))
        else:
            await manager.broadcast_to_room(room_id, event)

    return handler
