from fastapi import status


class AppError(Exception):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    code: str = "internal_error"
    message: str = "Internal server error"


class DatabaseMigrationError(Exception):
    "Database migration error"
