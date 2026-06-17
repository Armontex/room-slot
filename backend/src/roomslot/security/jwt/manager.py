from datetime import timedelta

import jwt as pyjwt

from roomslot.common.exceptions import (
    ExpiredTokenError,
    InvalidTokenError,
    MissingClaimError,
)
from roomslot.common.providers import SystemClock
from roomslot.security.jwt.token_claims import JsonValue, TokenClaims

REQUIRE_CLAIMS = frozenset({"sub", "iat", "exp", "roles"})
ALGORITHM = "HS256"
JWT_TYPE = "JWT"


class JWTManager:
    def __init__(
        self,
        private_key: str,
        *,
        clock: SystemClock,
    ) -> None:
        self._clock = clock
        self._private_key = private_key
        self._headers: dict[str, object] = {
            "alg": ALGORITHM,
            "typ": JWT_TYPE,
        }

    def issue_token(
        self,
        subject: str,
        ttl: timedelta = timedelta(
            days=36500  # FIX: https://github.com/Armontex/room-slot/issues/2
        ),
        roles: tuple[str, ...] = (),
    ) -> str:
        now = self._clock.now()
        payload: dict[str, JsonValue] = {
            "sub": subject,
            "iat": now.timestamp(),
            "exp": (now + ttl).timestamp(),
            "roles": list(roles),
        }

        return pyjwt.encode(  # pyright: ignore[reportUnknownMemberType]
            payload=payload,
            key=self._private_key,
            algorithm=ALGORITHM,
            headers=self._headers,
        )

    def verify(self, token: str) -> TokenClaims:
        try:
            payload: dict[str, JsonValue] = pyjwt.decode(  # pyright: ignore[reportUnknownMemberType]
                token,
                key=self._private_key,
                algorithms=ALGORITHM,
                options={
                    "require": list(REQUIRE_CLAIMS),
                },
            )
        except pyjwt.ExpiredSignatureError as e:
            raise ExpiredTokenError() from e
        except pyjwt.MissingRequiredClaimError as e:
            raise MissingClaimError(e.claim) from e
        except pyjwt.InvalidTokenError as e:
            raise InvalidTokenError() from e

        return TokenClaims.from_payload(payload)
