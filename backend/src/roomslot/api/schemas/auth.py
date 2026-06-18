from datetime import datetime
from uuid import UUID

from pydantic import EmailStr, Field

from roomslot.api.schemas.base import BaseResponse, BaseSchema
from roomslot.domain.enums import UserRole


class RegisterRequest(BaseSchema):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class LoginRequest(BaseSchema):
    email: EmailStr
    password: str


class LoginResponse(BaseResponse):
    access_token: str


class MeResponse(BaseResponse):
    id: UUID
    email: str
    role: UserRole
    created_at: datetime
