from __future__ import annotations

from collections.abc import Callable
from typing import Any

import attrs_validation as v
from attrs import Attribute
from attrs.validators import and_

type AttrsValidator[T] = Callable[[Any, Attribute[T], T], None]

int_validator = and_(
    v.instance_of(int),
    v.not_(v.instance_of(bool)),
)
