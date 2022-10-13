import logging


logger_config = {
    "version": 1,
    "disable_existing_loggers": False,
    # Formatters
    "formatters": {
        "std_format": {
            "format": "{levelname}: {asctime} [{name}] | {message} | File {module}.py, Func {funcName}() on {lineno} line",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
        "serv_format": {
            "format": "{levelname}: {asctime} [{name}] | {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
    # Handlers
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "std_format",
        },
        "uvicorn": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "serv_format",
        },
    },
    # Loggers
    "loggers": {
        "Accounts": {"level": "DEBUG", "handlers": ["console"]},
        "Ydx_storage": {"level": "DEBUG", "handlers": ["console"]},
        "uvicorn.access": {"level": "DEBUG", "handlers": ["console"]},
        "Server": {"level": "DEBUG", "handlers": ["uvicorn"]},
        "Utils": {"level": "DEBUG", "handlers": ["console"]},
    },
}

logging.config.dictConfig(logger_config)


def get_logger(name):
    logger = logging.getLogger(name)
    return logger
