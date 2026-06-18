# pyright: reportArgumentType=false

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from roomslot.api.exception_handlers import (
    app_error_handler,
    domain_error_handler,
    infra_error_handler,
    request_validation_error_handler,
    unexpected_exception_handler,
)
from roomslot.common.exceptions import AppError, DomainError, InfraError


def register_exception_handlers(app: FastAPI) -> None:

    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(DomainError, domain_error_handler)
    app.add_exception_handler(InfraError, infra_error_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(Exception, unexpected_exception_handler)
