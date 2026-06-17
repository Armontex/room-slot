from collections.abc import Callable

from roomslot.common.exceptions import InvalidCredentials
from roomslot.common.providers import SystemClock, Uuid4Generator
from roomslot.domain.entities.user import User
from roomslot.domain.value_objects.email import Email
from roomslot.repositories.auth import AuthRepository
from roomslot.security.password_hasher import PasswordHasher


class AuthService:
    def __init__(
        self,
        repo_factory: Callable[[], AuthRepository],
        password_hasher: PasswordHasher,
        clock: SystemClock,
        uuid_generator: Uuid4Generator,
    ) -> None:
        self._repo_factory = repo_factory
        self._ph = password_hasher
        self._clock = clock
        self._uuid_generator = uuid_generator

    async def register_user(self, email: str, password: str) -> User:
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

        return user

    async def login_user(self, email: str, password: str) -> User:
        repo = self._repo_factory()
        user = await repo.get_by_email(Email(email))

        if user is None:
            raise InvalidCredentials()

        if not await self._ph.verify(user.hashed_password, password):
            raise InvalidCredentials()

        return user
