def optional_strip_str(value: str | None) -> str | None:
    if value is None:
        return None
    return value.strip()
