from typing import Literal

from pydantic import BaseModel, ConfigDict

from roomslot.core.health import HealthStatus
from roomslot.schemas.base import BaseResponse


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
