from typing import Any, ClassVar

from sqladmin import Admin, ModelView
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.applications import Starlette
from starlette.requests import Request

from roomslot.config.admin import AdminSettings
from roomslot.db.models.booking import BookingModel
from roomslot.db.models.room import RoomModel
from roomslot.db.models.user import UserModel


class AdminAuth(AuthenticationBackend):
    def __init__(
        self,
        secret_key: str,
        username: str,
        password: str,
        **session_kwargs: Any,
    ) -> None:
        super().__init__(secret_key, **session_kwargs)
        self._username = username
        self._password = password

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if username == self._username and password == self._password:
            request.session.update({"admin_user": username})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return request.session.get("admin_user") == self._username


class UserAdmin(ModelView, model=UserModel):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    can_create = False
    can_delete = False

    column_list: ClassVar = [
        UserModel.id,
        UserModel.email,
        UserModel.role,
        UserModel.created_at,
    ]

    column_searchable_list: ClassVar = [UserModel.email]
    column_sortable_list: ClassVar = [UserModel.email, UserModel.created_at]

    form_columns: ClassVar = [UserModel.role]


class RoomAdmin(ModelView, model=RoomModel):
    name = "Room"
    name_plural = "Rooms"
    icon = "fa-solid fa-door-open"

    column_list: ClassVar = [
        RoomModel.id,
        RoomModel.name,
        RoomModel.building,
        RoomModel.floor,
        RoomModel.capacity,
        RoomModel.is_active,
    ]

    column_searchable_list: ClassVar = [RoomModel.name]
    column_sortable_list: ClassVar = [RoomModel.name, RoomModel.floor, RoomModel.capacity]
    form_columns: ClassVar = [
        RoomModel.id,
        RoomModel.name,
        RoomModel.building,
        RoomModel.floor,
        RoomModel.capacity,
        RoomModel.description,
        RoomModel.is_active,
    ]


class BookingAdmin(ModelView, model=BookingModel):
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-calendar-check"

    can_create = False
    can_edit = False
    can_delete = False

    column_list: ClassVar = [
        BookingModel.id,
        BookingModel.room_id,
        BookingModel.user_id,
        BookingModel.booking_date,
        BookingModel.slot_start,
        BookingModel.status,
        BookingModel.created_at,
        BookingModel.cancelled_at,
    ]

    column_sortable_list: ClassVar = [
        BookingModel.booking_date,
        BookingModel.slot_start,
        BookingModel.created_at,
    ]


def register_admin(
    app: Starlette,
    engine: AsyncEngine,
    settings: AdminSettings,
) -> None:
    auth_backend = AdminAuth(
        secret_key=settings.secret_key.get_secret_value(),
        username=settings.username,
        password=settings.password.get_secret_value(),
    )

    admin = Admin(
        app=app,
        engine=engine,
        title="RoomSlot Admin",
        base_url="/admin",
        authentication_backend=auth_backend,
    )

    admin.add_view(UserAdmin)
    admin.add_view(RoomAdmin)
    admin.add_view(BookingAdmin)
