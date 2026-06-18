from typing import Any

from fastapi import Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from structlog import get_logger

from roomslot.api.schemas.base import ErrorBody, ErrorResponse
from roomslot.common.exceptions import AppError, DomainError, InfraError

logger = get_logger(__name__)


async def app_error_handler(request: Request, exc: AppError) -> Response:
    logger.warning(
        exc.event or "app_error",
        code=exc.code,
        status_code=exc.status_code,
        message=exc.message,
        details=exc.details,
    )
    response = ErrorResponse(
        error=ErrorBody(
            code=exc.code,
            message=exc.message,
        ),
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(mode="json"),
    )


async def domain_error_handler(request: Request, exc: DomainError) -> Response:
    logger.critical(
        "domain_error",
        path=str(request.url.path),
        exc=str(exc),
    )
    response = ErrorResponse(
        error=ErrorBody(
            code="internal_error",
            message=exc.message,
        ),
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(mode="json"),
    )


async def infra_error_handler(request: Request, exc: InfraError) -> Response:
    logger.error("infra_error", exc=str(exc))
    response = ErrorResponse(
        error=ErrorBody(
            code="infra_error",
            message=exc.message,
        ),
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(mode="json"),
    )


async def request_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> Response:
    errors: list[dict[str, Any]] = [
        {
            "field": " → ".join(str(part) for part in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        }
        for error in exc.errors()
    ]

    response = ErrorResponse(
        error=ErrorBody(
            code="validation_error",
            message="Validation error",
            details={"errors": errors},
        )
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=response.model_dump(mode="json"),
    )


def unexpected_exception_handler(request: Request, exc: Exception) -> Response:
    logger.critical("app.unexpected_error", exc=str(exc))

    response = ErrorResponse(
        error=ErrorBody(
            code="internal_error",
            message="Internal server error",
        )
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump(mode="json"),
    )
