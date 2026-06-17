from sqlalchemy.exc import IntegrityError

from roomslot.common.exceptions import EmailAlreadyExistsError
from roomslot.common.mappers import map_user_entity_to_model
from roomslot.domain.entities.user import User
from roomslot.repositories.base import BaseRepository


class AuthRepository(BaseRepository):
    async def add(self, user: User) -> None:
        model = map_user_entity_to_model(user)
        self._session.add(model)
        try:
            await self._session.flush()
        except IntegrityError as e:
            raise EmailAlreadyExistsError() from e
