from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field

from roomslot.domain.enums import UserRole


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str


class MeResponse(BaseModel):
    id: UUID
    email: str
    role: UserRole
    created_at: datetime
