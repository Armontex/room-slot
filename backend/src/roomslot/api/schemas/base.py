from pydantic import BaseModel, ConfigDict

_HARD_MODEL_CONFIG = ConfigDict(extra="forbid", frozen=True)


class BaseSchema(BaseModel):
    model_config = _HARD_MODEL_CONFIG


class BaseResponse(BaseSchema):
    success: bool = True
