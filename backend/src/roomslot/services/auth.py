from collections.abc import Callable
from datetime import timedelta
from uuid import UUID

from structlog import get_logger

from roomslot.common.exceptions import InvalidCredentials
from roomslot.common.providers import SystemClock, Uuid4Generator
from roomslot.domain.entities.user import User
from roomslot.domain.value_objects.email import Email
from roomslot.repositories.auth import AuthRepository
from roomslot.security.jwt.manager import JWTManager
from roomslot.security.password_hasher import PasswordHasher

logger = get_logger(__name__)


class AuthService:
    def __init__(
        self,
        repo_factory: Callable[[], AuthRepository],
        password_hasher: PasswordHasher,
        clock: SystemClock,
        uuid_generator: Uuid4Generator,
        jwt_manager: JWTManager,
        jwt_ttl_minutes: int,
    ) -> None:
        self._repo_factory = repo_factory
        self._ph = password_hasher
        self._clock = clock
        self._uuid_generator = uuid_generator
        self._jwt = jwt_manager
        self._jwt_ttl_minutes = jwt_ttl_minutes

    async def register_user(self, email: str, password: str) -> User:
        logger.debug("auth.register_user.started")

        hashed_password = await self._ph.hash(password)
        user = User.create(
            email=Email(email),
            hashed_password=hashed_password,
            clock=self._clock,
            uuid_generator=self._uuid_generator,
        )

        repo = self._repo_factory()
        session = repo.get_session()

        await repo.add(user)
        await session.commit()

        logger.info("auth.register_user.succeeded")

        return user

    async def login_user(self, email: str, password: str) -> str:
        logger.debug("auth.login_user.started")

        repo = self._repo_factory()
        user = await repo.get_by_email(Email(email))

        if user is None:
            logger.warning("auth.login_user.not_found")
            raise InvalidCredentials()

        if not await self._ph.verify(user.hashed_password, password):
            logger.warning("auth.login_user.invalid_password")
            raise InvalidCredentials()

        access_token = self._jwt.issue_token(
            subject=str(user.id),
            ttl=timedelta(minutes=self._jwt_ttl_minutes),
        )

        logger.info("auth.login_user.succeeded")

        return access_token

    async def authenticate_user(self, token: str) -> User:
        logger.debug("auth.authenticate_user.started")

        claims = self._jwt.verify(token)
        try:
            user_id = UUID(claims.subject)
        except ValueError as e:
            logger.warning("auth.authenticate_user.invalid_token")
            raise InvalidCredentials() from e

        repo = self._repo_factory()
        user = await repo.get_by_id(user_id)

        if user is None:
            logger.warning("auth.authenticate_user.not_found")
            raise InvalidCredentials()

        return user
