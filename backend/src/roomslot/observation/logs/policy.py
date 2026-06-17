import logging

DEFAULT_EXCLUDED_ACCESS_LOG_PATHS = frozenset(
    {
        "/health/live",
        "/health/ready",
        "/metrics",
    }
)

EXCLUDED_ACCESS_LOG_METHODS = frozenset({"OPTIONS"})


def access_log_level_for_status(
    status_code: int,
) -> int:
    if status_code >= 500:
        return logging.ERROR

    return logging.INFO
