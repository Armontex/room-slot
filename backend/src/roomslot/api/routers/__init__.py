from fastapi import APIRouter

from roomslot.api.routers.auth import router as auth_router
from roomslot.api.routers.bookings import bookings_router
from roomslot.api.routers.bookings import me_router as bookings_me_router
from roomslot.api.routers.health import router as health_router
from roomslot.api.routers.room import router as room_router
from roomslot.api.routers.slots import router as slots_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(room_router)
api_router.include_router(slots_router)
api_router.include_router(bookings_router)
api_router.include_router(bookings_me_router)
