from __future__ import annotations

import logging
import sys
from typing import Literal

import structlog
from pydantic_settings import BaseSettings, SettingsConfigDict

LOG_LEVELS = Literal["CRITICAL", "FATAL", "ERROR", "WARN", "WARNING", "INFO", "DEBUG", "NOTSET"]


class NortechLoggerSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NORTECH_LOG_", env_file=(".env", ".env.prod"), extra="ignore")

    LEVEL: LOG_LEVELS = "INFO"


def get_logger(
    level: LOG_LEVELS = "INFO",
):
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(processor=structlog.dev.ConsoleRenderer(colors=sys.stdout.isatty()))

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = structlog.stdlib.get_logger(nortech_sdk=True)
    logger.addHandler(handler)
    logger.setLevel(logging.getLevelName(level))
    return logger


logger = get_logger(NortechLoggerSettings().LEVEL)
