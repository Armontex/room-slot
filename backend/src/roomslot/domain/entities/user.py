from __future__ import annotations

from datetime import datetime
from uuid import UUID

from attrs import define, field
from attrs_validation import validators as v

from roomslot.core.exceptions import DomainError
from roomslot.domain.const import USER_HASHED_PASSWORD_MAX_LEN, USER_HASHED_PASSWORD_MIN_LEN
from roomslot.domain.enums import UserRole
from roomslot.domain.ports import Clock, UuidGenerator
from roomslot.domain.value_objects.email import Email


@define(frozen=True, slots=True, kw_only=True)
class User:
    id: UUID = field(validator=v.instance_of(UUID))
    email: Email = field(validator=v.instance_of(Email))
    role: UserRole = field(validator=v.instance_of(UserRole))
    hashed_password: str = field(
        converter=str.strip,
        validator=[
            v.instance_of(str),
            v.min_len(USER_HASHED_PASSWORD_MIN_LEN),
            v.max_len(USER_HASHED_PASSWORD_MAX_LEN),
        ],
    )
    created_at: datetime = field(validator=v.instance_of(datetime))
    updated_at: datetime = field(validator=v.instance_of(datetime))

    def __attrs_post_init__(self) -> None:
        if self.updated_at < self.created_at:
            raise DomainError("User updated_at must be greater than or equal created_at")

    @classmethod
    def create(
        cls,
        email: Email,
        hashed_password: str,
        role: UserRole = UserRole.USER,
        *,
        clock: Clock,
        uuid_generator: UuidGenerator,
    ) -> User:
        now = clock.now()
        return User(
            id=uuid_generator.generate(),
            email=email,
            hashed_password=hashed_password,
            created_at=now,
            updated_at=now,
            role=role,
        )
