from collections.abc import AsyncGenerator, Callable
from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker
from starlette.requests import HTTPConnection

from roomslot.common.exceptions import TokenError
from roomslot.common.providers import SystemClock, Uuid4Generator
from roomslot.config.settings import Settings
from roomslot.domain.entities.user import User
from roomslot.domain.ports import Clock, UuidGenerator
from roomslot.messaging.channels import BOOKING_EVENTS_CHANNEL
from roomslot.messaging.publisher import RedisPublisher
from roomslot.repositories.auth import AuthRepository
from roomslot.repositories.booking import BookingRepository
from roomslot.repositories.room import RoomRepository
from roomslot.security.jwt.manager import JWTManager
from roomslot.security.password_hasher import PasswordHasher
from roomslot.services.auth import AuthService
from roomslot.services.booking import BookingService
from roomslot.services.event_publisher import EventPublisher
from roomslot.services.room import RoomService
from roomslot.services.slot import SlotService
from roomslot.ws.room_connection_manager import RoomConnectionManager

HTTP_BEARER = HTTPBearer(auto_error=False)


def get_engine(request: Request) -> AsyncEngine:
    return request.app.state.engine


def get_redis(request: Request) -> Redis:
    return request.app.state.redis


def get_room_connection_manager(conn: HTTPConnection) -> RoomConnectionManager:
    return conn.app.state.room_connection_manager


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
RedisDepend = Annotated[Redis, Depends(get_redis)]
RoomConnectionManagerDepend = Annotated[RoomConnectionManager, Depends(get_room_connection_manager)]


def get_jwt_manager(
    settings: SettingsDepend,
    clock: ClockDepend,
) -> JWTManager:
    return JWTManager(
        private_key=settings.security.jwt_secret_key.get_secret_value(),
        clock=clock,
    )


Channel = str


def get_redis_publisher_factory(
    redis: RedisDepend,
) -> Callable[[Channel], RedisPublisher]:
    return lambda channel: RedisPublisher(redis, channel)


AuthRepoFactory = Callable[[], AuthRepository]
BookingRepoFactory = Callable[[], BookingRepository]
RoomRepoFactory = Callable[[], RoomRepository]
RedisPublisherFactoryDepend = Annotated[
    Callable[[Channel], RedisPublisher], Depends(get_redis_publisher_factory)
]


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


def get_room_service(repo_factory: RoomRepoFactoryDepend) -> RoomService:
    return RoomService(repo_factory=repo_factory)


def get_slot_service(
    room_repo_factory: RoomRepoFactoryDepend,
    booking_repo_factory: BookingRepoFactoryDepend,
    clock: ClockDepend,
) -> SlotService:
    return SlotService(
        room_repo_factory=room_repo_factory,
        booking_repo_factory=booking_repo_factory,
        clock=clock,
    )


def get_event_publisher_factory(
    redis_publisher_factory: RedisPublisherFactoryDepend,
) -> Callable[[Channel], EventPublisher]:
    return lambda channel: EventPublisher(redis_publisher_factory(channel))


EventPublisherFactoryDepend = Annotated[
    Callable[[Channel], EventPublisher], Depends(get_event_publisher_factory)
]


def get_booking_event_publisher(
    event_publisher_factory: EventPublisherFactoryDepend,
) -> EventPublisher:
    return event_publisher_factory(BOOKING_EVENTS_CHANNEL)


def get_booking_service(
    repo_factory: BookingRepoFactoryDepend,
    clock: ClockDepend,
    uuid_generator: UuidGenDepend,
    booking_event_publisher: Annotated[EventPublisher, Depends(get_booking_event_publisher)],
) -> BookingService:
    return BookingService(
        booking_repo_factory=repo_factory,
        room_repo_factory=RoomRepository,
        clock=clock,
        uuid_generator=uuid_generator,
        event_publisher=booking_event_publisher,
    )


def get_access_token(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(HTTP_BEARER),
    ],
) -> str:
    if credentials is None or not credentials.credentials:
        raise TokenError("auth.token.missing")
    return credentials.credentials


async def get_user(
    token: Annotated[str, Depends(get_access_token)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    return await service.authenticate_user(token)


TokenDepend = Annotated[str, Depends(get_access_token)]
UserDepend = Annotated[User, Depends(get_user)]
