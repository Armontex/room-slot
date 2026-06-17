import logging
import sys

import structlog
from structlog.typing import Processor

from roomslot.config.logging import LogFormat, LoggingSettings


def setup_logging(settings: LoggingSettings) -> None:
    timestamper = structlog.processors.TimeStamper(
        fmt="iso",
        utc=True,
    )
    format_exc_info = structlog.processors.format_exc_info

    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.ExtraAdder(),
        timestamper,
        structlog.processors.StackInfoRenderer(),
    ]

    renderer = (
        structlog.dev.ConsoleRenderer()
        if settings.log_format == LogFormat.CONSOLE
        else structlog.processors.JSONRenderer()
    )

    if settings.log_format == LogFormat.JSON:
        shared_processors.append(format_exc_info)  # pyright: ignore[reportArgumentType]

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(settings.log_level)
