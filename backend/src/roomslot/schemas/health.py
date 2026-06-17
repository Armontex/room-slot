from pydantic import BaseModel, ConfigDict

from roomslot.core.health import HealthStatus


class HealthCheckResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    status: HealthStatus
    error: str | None = None


class HealthReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: HealthStatus
    checks: tuple[HealthCheckResultResponse, ...]
