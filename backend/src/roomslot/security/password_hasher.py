import asyncio

from argon2 import PasswordHasher as ph
from argon2.exceptions import InvalidHashError, VerificationError


class PasswordHasher:
    def __init__(self) -> None:
        self._hasher = ph()

    async def hash(self, password: str) -> str:
        result = await asyncio.to_thread(self._hasher.hash, password=password)
        return result

    async def verify(self, hash: str, password: str) -> bool:
        try:
            await asyncio.to_thread(self._hasher.verify, hash=hash, password=password)
        except (VerificationError, InvalidHashError):
            return False
        return True
