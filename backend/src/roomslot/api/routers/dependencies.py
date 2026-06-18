from collections.abc import AsyncGenerator, Callable
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from roomslot.common.providers import SystemClock, Uuid4Generator
from roomslot.config.settings import Settings
from roomslot.domain.ports import Clock, UuidGenerator
from roomslot.repositories.auth import AuthRepository
from roomslot.repositories.booking import BookingRepository
from roomslot.repositories.room import RoomRepository
from roomslot.security.jwt.manager import JWTManager
from roomslot.security.password_hasher import PasswordHasher
from roomslot.services.auth import AuthService


def get_engine(request: Request) -> AsyncEngine:
    return request.app.state.engine


async def get_session(request: Request) -> AsyncGenerator[AsyncSession]:
    session_maker: async_sessionmaker[AsyncSession] = request.app.state.session_maker
    async with session_maker() as session:
        yield session


@lru_cache(maxsize=1)
def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()


@lru_cache(maxsize=1)
def get_clock() -> Clock:
    return SystemClock


@lru_cache(maxsize=1)
def get_uuid_generator() -> UuidGenerator:
    return Uuid4Generator()


def get_settings(request: Request) -> Settings:
    return request.app.state.settings


ClockDepend = Annotated[Clock, Depends(get_clock)]
UuidGenDepend = Annotated[UuidGenerator, Depends(get_uuid_generator)]
SessionDepend = Annotated[AsyncSession, Depends(get_session)]
SettingsDepend = Annotated[Settings, Depends(get_settings)]


def get_jwt_manager(
    settings: SettingsDepend,
    clock: ClockDepend,
) -> JWTManager:
    return JWTManager(
        private_key=settings.security.jwt_secret_key.get_secret_value(),
        clock=clock,
    )


AuthRepoFactory = Callable[[], AuthRepository]
BookingRepoFactory = Callable[[], BookingRepository]
RoomRepoFactory = Callable[[], RoomRepository]


def get_auth_repo_factory(
    session: SessionDepend,
) -> AuthRepoFactory:
    return lambda: AuthRepository(session)


def get_booking_repo_factory(
    session: SessionDepend,
) -> Callable[[], BookingRepository]:
    return lambda: BookingRepository(session)


def get_room_repo_factory(
    session: SessionDepend,
) -> Callable[[], RoomRepository]:
    return lambda: RoomRepository(session)


AuthRepoFactoryDepend = Annotated[AuthRepoFactory, Depends(get_auth_repo_factory)]
BookingRepoFactoryDepend = Annotated[BookingRepoFactory, Depends(get_booking_repo_factory)]
RoomRepoFactoryDepend = Annotated[RoomRepoFactory, Depends(get_room_repo_factory)]


def get_auth_service(
    repo_factory: AuthRepoFactoryDepend,
    password_hasher: Annotated[PasswordHasher, Depends(get_password_hasher)],
    clock: ClockDepend,
    uuid_generator: UuidGenDepend,
    jwt_manager: Annotated[JWTManager, Depends(get_jwt_manager)],
    settings: SettingsDepend,
) -> AuthService:
    return AuthService(
        repo_factory=repo_factory,
        password_hasher=password_hasher,
        clock=clock,
        uuid_generator=uuid_generator,
        jwt_manager=jwt_manager,
        jwt_ttl_minutes=settings.security.jwt_ttl_minutes,
    )
