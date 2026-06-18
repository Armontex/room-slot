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
