from typing import Annotated

from fastapi import APIRouter, Depends, status

from roomslot.api.routers.dependencies import UserDepend, get_auth_service
from roomslot.api.schemas.auth import LoginRequest, LoginResponse, MeResponse, RegisterRequest
from roomslot.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

AuthServiceDepend = Annotated[AuthService, Depends(get_auth_service)]


@router.post(
    path="/register",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def register_user(
    body: RegisterRequest,
    service: AuthServiceDepend,
) -> None:
    await service.register_user(
        email=body.email,
        password=body.password,
    )


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    response_model=LoginResponse,
)
async def login_user(
    body: LoginRequest,
    service: AuthServiceDepend,
) -> LoginResponse:
    token = await service.login_user(
        email=body.email,
        password=body.password,
    )
    return LoginResponse(access_token=token)


@router.get(
    path="/me",
    status_code=status.HTTP_200_OK,
    response_model=MeResponse,
)
async def me(
    user: UserDepend,
) -> MeResponse:
    return MeResponse(
        id=user.id,
        email=user.email.value,
        role=user.role,
        created_at=user.created_at,
    )
