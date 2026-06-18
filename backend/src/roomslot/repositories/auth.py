from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from roomslot.common.exceptions import EmailAlreadyExistsError
from roomslot.common.mappers import map_user_entity_to_model, map_user_model_to_entity
from roomslot.db.models.user import UserModel
from roomslot.domain.entities.user import User
from roomslot.domain.value_objects.email import Email
from roomslot.repositories.base import BaseRepository


class AuthRepository(BaseRepository):
    async def add(self, user: User) -> None:
        model = map_user_entity_to_model(user)
        self._session.add(model)
        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            raise EmailAlreadyExistsError("auth.register_user.email_already_exists") from e

    async def get_by_email(self, email: Email) -> User | None:
        query = select(UserModel).filter_by(email=email.value)
        result = await self._session.execute(query)

        if (result := result.scalar_one_or_none()) is None:
            return None

        return map_user_model_to_entity(result)

    async def get_by_id(self, id: UUID) -> User | None:
        result = await self._session.get(UserModel, id)

        if result is None:
            return None

        return map_user_model_to_entity(result)
