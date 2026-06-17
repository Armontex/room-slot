import asyncio
from collections.abc import Awaitable, Callable, Iterable
from dataclasses import dataclass
from enum import StrEnum

HealthCheckCallable = Callable[[], Awaitable[None]]
DEFAULT_HEALTH_CHECK_TIMEOUT_SECONDS = 3.0


class HealthStatus(StrEnum):
    OK = "ok"
    FAILED = "failed"


@dataclass(slots=True, frozen=True)
class HealthCheck:
    name: str
    check: HealthCheckCallable


@dataclass(slots=True, frozen=True)
class HealthCheckResult:
    name: str
    status: HealthStatus
    error: str | None = None


@dataclass(slots=True, frozen=True)
class HealthReport:
    status: HealthStatus
    checks: tuple[HealthCheckResult, ...]

    @property
    def is_ok(self) -> bool:
        return self.status == HealthStatus.OK


async def run_health_checks(
    checks: Iterable[HealthCheck],
    *,
    timeout_seconds: float = DEFAULT_HEALTH_CHECK_TIMEOUT_SECONDS,
) -> HealthReport:
    results = await asyncio.gather(
        *(
            _run_health_check(health_check, timeout_seconds=timeout_seconds)
            for health_check in checks
        )
    )

    status = HealthStatus.OK
    if any(result.status == HealthStatus.FAILED for result in results):
        status = HealthStatus.FAILED

    return HealthReport(
        status=status,
        checks=tuple(results),
    )


async def _run_health_check(
    health_check: HealthCheck,
    *,
    timeout_seconds: float,
) -> HealthCheckResult:
    try:
        await asyncio.wait_for(health_check.check(), timeout=timeout_seconds)
    except Exception as exc:
        return HealthCheckResult(
            name=health_check.name,
            status=HealthStatus.FAILED,
            error=f"{type(exc).__name__}: {exc}",
        )

    return HealthCheckResult(
        name=health_check.name,
        status=HealthStatus.OK,
    )
