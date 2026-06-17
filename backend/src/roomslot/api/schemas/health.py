from typing import Literal

from pydantic import BaseModel, ConfigDict

from roomslot.api.schemas.base import BaseResponse
from roomslot.core.health import HealthStatus


class HealthCheckResultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    status: HealthStatus
    error: str | None = None


class HealthReportResponse(BaseResponse):
    model_config = ConfigDict(from_attributes=True)

    status: HealthStatus
    checks: tuple[HealthCheckResultResponse, ...]


class LiveResponse(BaseResponse):
    status: Literal["ok"] = "ok"
