import logging


def access_log_level_for_status(
    status_code: int,
) -> int:
    if status_code >= 500:
        return logging.ERROR

    return logging.INFO
