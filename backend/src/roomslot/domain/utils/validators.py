from __future__ import annotations

import attrs_validation as v
from attrs.validators import and_

is_int = and_(
    v.instance_of(int),
    v.not_(v.instance_of(bool)),
)
