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
    status_code: int = status.HTTP_409_CONFLICT
    code: str = "already_exists"
    message: str = "Resource already exists"


class NotFoundError(AppError):
    status_code: int = status.HTTP_404_NOT_FOUND
    code: str = "not_found"
    message: str = "Resource not found"


class EmailAlreadyExistsError(AlreadyExistsError):
    message: str = "Email already exists"


class InvalidCredentials(AppError):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    code: str = "invalid_credentials"
    message: str = "Invalid credentials"


class TokenError(AppError):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    code: str = "invalid_token"
    message: str = "Invalid token"


class ExpiredTokenError(TokenError):
    code: str = "expired_token"
    message: str = "Token has expired"


class MissingClaimError(TokenError):
    code: str = "missing_token_claim"
    message: str = "Missing required token claim"

    def __init__(self, claim: str) -> None:
        self.message = f"Missing required token claim: {claim}"


class InvalidTokenError(TokenError):
    code: str = "invalid_token"
    message: str = "Invalid token"
