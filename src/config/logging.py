import logging
import sys
from typing import Any, Dict

import structlog

def get_logging_config(log_level: str = "INFO", is_enabled: bool = True) -> Dict[str, Any]:
    """
    Returns a logging configuration dictionary for dictConfig.
    Configures structlog with standard processors.
    """
    if not is_enabled:
        return {
            "version": 1,
            "disable_existing_loggers": True,
            "handlers": {},
            "loggers": {}
        }

    level = getattr(logging, log_level.upper(), logging.INFO)
    
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": structlog.stdlib.ProcessorFormatter,
                "processor": structlog.processors.JSONRenderer(),
            },
            "console": {
               "()": structlog.stdlib.ProcessorFormatter,
               "processor": structlog.dev.ConsoleRenderer(),
            }
        },
        "handlers": {
            "default": {
                "level": level,
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "console",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": level,
                "propagate": True,
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["default"],
                "propagate": False,
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["default"],
                "propagate": False,
            },
        },
    }
