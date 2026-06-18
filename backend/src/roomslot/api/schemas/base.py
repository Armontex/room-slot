from pydantic import BaseModel, ConfigDict, Field

_HARD_MODEL_CONFIG = ConfigDict(extra="forbid", frozen=True)


class BaseSchema(BaseModel):
    model_config = _HARD_MODEL_CONFIG


class BaseResponse(BaseSchema):
    success: bool = True


class ErrorBody(BaseSchema):
    code: str
    message: str
    details: dict[str, object] = Field(default_factory=dict)


class ErrorResponse(BaseResponse):
    success: bool = Field(default=False, init=False)
    error: ErrorBody


class PaginationQuery(BaseSchema):
    offset: int = Field(ge=0)
    limit: int = Field(ge=1, default=30)


class PaginatedResponse[T](BaseResponse):
    items: list[T]
    total: int
    limit: int
    offset: int
