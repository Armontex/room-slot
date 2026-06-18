from typing import Annotated

from fastapi import APIRouter, Depends, status

from roomslot.api.routers.dependencies import get_auth_service
from roomslot.api.schemas.auth import RegisterRequest
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
