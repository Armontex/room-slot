from typing import Annotated

from fastapi import APIRouter, Depends, Response, status

from roomslot.api.routers.dependencies import get_container
from roomslot.api.schemas.health import (
    HealthCheckResultResponse,
    HealthReportResponse,
    LiveResponse,
)
from roomslot.bootstrap.health import build_health_checks
from roomslot.containers.container import Container
from roomslot.core.health import run_health_checks

router = APIRouter(prefix="/health", tags=["Health"])


@router.get(
    path="/live",
    status_code=status.HTTP_200_OK,
    response_model=LiveResponse,
)
async def live() -> LiveResponse:
    return LiveResponse()


@router.get(
    path="/ready",
    status_code=status.HTTP_200_OK,
    response_model=HealthReportResponse,
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "model": HealthReportResponse,
            "description": "Service not ready",
        }
    },
)
async def ready(
    response: Response,
    container: Annotated[
        Container,
        Depends(get_container),
    ],
) -> HealthReportResponse:
    checks = build_health_checks(container)
    result = await run_health_checks(checks)

    if not result.is_ok:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return HealthReportResponse(
        status=result.status,
        checks=tuple(
            HealthCheckResultResponse(name=res.name, status=res.status, error=res.error)
            for res in result.checks
        ),
    )
