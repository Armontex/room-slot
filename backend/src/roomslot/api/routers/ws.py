from uuid import UUID

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from roomslot.api.routers.dependencies import RoomConnectionManagerDepend

router = APIRouter(prefix="/ws", tags=["WebSocket"])


@router.websocket("/rooms/{room_id}")
async def room_ws(
    websocket: WebSocket, room_id: UUID, manager: RoomConnectionManagerDepend
) -> None:
    await manager.connect(room_id=room_id, ws=websocket)

    try:
        while True:
            await websocket.receive()
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect(room_id=room_id, ws=websocket)
