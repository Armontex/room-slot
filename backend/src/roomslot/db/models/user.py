from sqlalchemy import CheckConstraint, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, validates

from roomslot.common.providers import SystemClock
from roomslot.db.models.base import Base
from roomslot.db.models.enums import UserRoleEnum
from roomslot.db.models.types import ID, CreatedAt, UpdatedAt
from roomslot.domain.const import USER_HASHED_PASSWORD_MAX_LEN, USER_HASHED_PASSWORD_MIN_LEN
from roomslot.domain.enums import UserRole


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[ID] = mapped_column()
    email: Mapped[str] = mapped_column(
        String(length=255, collation="utf8mb4_0900_ai_ci"),
        nullable=False,
        unique=True,
    )
    hashed_password: Mapped[str] = (  # TODO: Когда будем делать OAuth2 нужно поменять nullable
        mapped_column(
            String(USER_HASHED_PASSWORD_MAX_LEN),
            nullable=False,
        )
    )
    role: Mapped[UserRole] = mapped_column(
        UserRoleEnum,
        default=UserRole.USER,
        server_default=text(f"'{UserRole.USER.value}'"),
        nullable=False,
    )
    created_at: Mapped[CreatedAt] = mapped_column(default_factory=SystemClock.now)
    updated_at: Mapped[UpdatedAt] = mapped_column(default_factory=SystemClock.now)

    __table_args__ = (
        CheckConstraint(
            func.char_length(func.trim(email)) >= 1,
            name="email_min_len",
        ),
        CheckConstraint(
            func.char_length(func.trim(hashed_password)) >= USER_HASHED_PASSWORD_MIN_LEN,
            name="hashed_password_min_len",
        ),
        CheckConstraint(
            updated_at >= created_at,
            name="updated_at_ge_than_created_at",
        ),
    )

    @validates("email")
    def _normalize_email(self, _: str, value: str) -> str:
        return value.strip().lower()

    @validates("hashed_password")
    def _normalize_hashed_password(self, _: str, value: str) -> str:
        return value.strip()
