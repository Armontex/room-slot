class DomainError(Exception):
    message: str

    def __init__(self, message: str) -> None:
        super().__init__(message)
