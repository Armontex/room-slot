import json
from typing import Any


def parse_env_list(v: Any) -> Any:
    if isinstance(v, str):
        v = v.strip()
        if not v:
            return []
        if v.startswith("[") and v.endswith("]"):
            return json.loads(v)
        return [item.strip() for item in v.split(",") if item.strip()]
    return v
