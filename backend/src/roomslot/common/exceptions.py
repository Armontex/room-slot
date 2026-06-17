from fastapi import status


class BaseError(Exception):
    message: str

    def __init__(self, message: str) -> None:
        super().__init__(message)


class DomainError(BaseError): ...


class InfraError(BaseError): ...


class AppError(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str = "internal_error"
    message: str = "Internal server error"


class DatabaseMigrationError(Exception):
    "Database migration error"


class AlreadyExistsError(AppError):
    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "already_exists"
    message: str = "Resource already exists"


class EmailAlreadyExistsError(AlreadyExistsError):
    message: str = "Email already exists"
