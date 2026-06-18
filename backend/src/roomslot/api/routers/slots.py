from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from roomslot.api.routers.dependencies import get_slot_service
from roomslot.api.schemas.slots import DayResponseItem, DaySlotsResponseItem, SlotsResponse
from roomslot.services.slot import SlotService

router = APIRouter(tags=["Slots"])

SlotServiceDepend = Annotated[SlotService, Depends(get_slot_service)]


@router.get(
    path="/rooms/{room_id}/slots",
    status_code=status.HTTP_200_OK,
    response_model=SlotsResponse,
)
async def slots(
    room_id: UUID,
    service: SlotServiceDepend,
) -> SlotsResponse:
    slots_schedule = await service.get_room_slots(room_id)

    return SlotsResponse(
        room_id=room_id,
        date_from=slots_schedule.date_from,
        date_to=slots_schedule.date_to,
        days=[
            DayResponseItem(
                date=day.date,
                slots=[
                    DaySlotsResponseItem(
                        time=slot.slot.start_at.time(),
                        status=slot.status,
                    )
                    for slot in day.slots
                ],
            )
            for day in slots_schedule.days
        ],
    )
