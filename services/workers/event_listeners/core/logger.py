import os

log_path = os.path.join("/", "src/logs/event_listeners.json")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "ecs_logging.StdlibFormatter",
        },
    },
    "handlers": {
        "app_handler": {
            "level": "INFO",
            "formatter": "json",
            "class": "logging.FileHandler",
            "filename": log_path,
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "auth_service": {
            "handlers": ["app_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "ugc_service": {
            "handlers": ["app_handler"],
            "level": "INFO",
            "propagate": False,
        },
        "websocket_service": {
            "handlers": ["app_handler"],
            "level": "INFO",
            "propagate": False,
        },
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console",
        ],
    },
}
