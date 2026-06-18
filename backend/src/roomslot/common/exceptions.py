from typing import Any

from fastapi import status


class BaseError(Exception):
    message: str = "Error"

    def __init__(self, message: str | None = None) -> None:
        if message is not None:
            self.message = message
        super().__init__(self.message)


class DomainError(BaseError):
    message: str = "Internal server error"


class InfraError(BaseError):
    message: str = "Internal server error"


class DatabaseMigrationError(BaseError):
    message: str = "Database migration error"


class AppError(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str = "internal_error"
    message: str = "Internal server error"
    event: str | None = None
    details: dict[str, Any] | None = None

    def __init__(
        self,
        event: str,
        message: str | None = None,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.event = event
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if details is not None:
            self.details = details
        super().__init__(self.message)


class AlreadyExistsError(AppError):
    status_code: int = status.HTTP_409_CONFLICT
    code: str = "already_exists"
    message: str = "Resource already exists"


class NotFoundError(AppError):
    status_code: int = status.HTTP_404_NOT_FOUND
    code: str = "not_found"
    message: str = "Resource not found"


class UnauthorizedError(AppError):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    code: str = "unauthorized"
    message: str = "Unauthorized"


class ForbiddenError(AppError):
    status_code: int = status.HTTP_403_FORBIDDEN
    code: str = "forbidden"
    message: str = "Forbidden"


class ConflictError(AppError):
    status_code: int = status.HTTP_409_CONFLICT
    code: str = "conflict"
    message: str = "Conflict"


# =============================================


class InvalidCredentials(UnauthorizedError):
    code: str = "invalid_credentials"
    message: str = "Invalid credentials"


class EmailAlreadyExistsError(AlreadyExistsError):
    message: str = "Email already exists"


class TokenError(UnauthorizedError):
    code: str = "invalid_token"
    message: str = "Invalid token"


class ExpiredTokenError(TokenError):
    code: str = "expired_token"
    message: str = "Token has expired"


class MissingClaimError(TokenError):
    code: str = "missing_token_claim"
    message: str = "Missing required token claim"

    def __init__(self, claim: str) -> None:
        super().__init__(
            event="auth.token.missing_claim",
            message=f"Missing required token claim: {claim}",
        )


class InvalidTokenError(TokenError):
    code: str = "invalid_token"
    message: str = "Invalid token"


class RoomNotFoundError(NotFoundError):
    message: str = "Room not found"


class BookingAlreadyExists(AlreadyExistsError):
    message: str = "Booking already exists"


class BookingNotFoundError(NotFoundError):
    message: str = "Booking not found"


class BookingAccessDeniedError(ForbiddenError):
    code: str = "booking_access_denied"
    message: str = "You are not allowed to manage this booking"


class BookingAlreadyCancelled(ConflictError):
    code: str = "already_cancelled"
    message: str = "Booking already cancelled"
