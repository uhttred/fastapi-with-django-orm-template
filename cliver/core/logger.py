from logging.config import dictConfig

from cliver.settings import config


loggers: list[str] = ['default']


def configure_logger():
    """Configure logging for all aplication"""
    dictConfig({
        "disable_existing_loggers": False,
        "version": 1,
        "filters": {
            "correlation_id": {
                "()": "asgi_correlation_id.CorrelationIdFilter",
                "uuid_length": 8 if config.in_devmode else 20,
                "default_value": "-"
            }
        },
        "formatters": {
            "console": {
                "class": "logging.Formatter",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
                "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s"
            },
            "file": {
                "class": "logging.Formatter",
                "datefmt": "%Y-%m-%dT%H:%M:%S",
                "format": "%(asctime)s.%(msecs)03dZ | %(levelname)-8s | (%(correlation_id)s) %(name)s:%(lineno)d - %(message)s"
            }
        },
        "handlers": {
            "default": {
                "class": "rich.logging.RichHandler",
                "level": "DEBUG",
                "formatter": "console",
                "filters": ['correlation_id']
            }
        },
        "loggers": {
            "cliver": {
                "handlers": loggers,
                "level": 'DEBUG' if config.in_devmode else 'INFO',
                "propagate": False
            },
            "uvicorn": {
                "handlers": loggers,
                "level": 'INFO'
            }
        }
    })
