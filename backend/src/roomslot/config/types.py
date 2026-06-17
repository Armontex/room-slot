from typing import Annotated, TypeVar

from pydantic import BeforeValidator
from pydantic_settings import NoDecode

from roomslot.config.utils import parse_env_list

T = TypeVar("T")

EnvList = Annotated[
    list[T],
    NoDecode,
    BeforeValidator(parse_env_list),
]
