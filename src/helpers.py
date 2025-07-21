import logging.config
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path

from aiohttp import ClientSession, BasicAuth

from src.config import get_settings
from src.enums import Color

settings = get_settings()


async def blink1_color(color: Color):
    async with ClientSession() as session:
        auth = BasicAuth(
            settings.NGROK_USER.get_secret_value(),
            settings.NGROK_PASS.get_secret_value(),
        )
        ngrok_url = settings.NGROK_URL.get_secret_value()
        await session.get(ngrok_url + f"blink/{color}", auth=auth)


class CustomFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created).astimezone()
        if datefmt:
            base_time = ct.strftime("%d.%m.%Y %H:%M:%S")
            msecs = f"{int(record.msecs):03d}"
            tz = ct.strftime("%z")
            return f"{base_time}.{msecs}{tz}"
        return super().formatTime(record, datefmt)


main_template = {
    "format": "%(asctime)s | %(message)s",
    "datefmt": "%d.%m.%Y %H:%M:%S%z",
}
error_template = {
    "format": "%(asctime)s [%(levelname)8s] [%(module)s:%(funcName)s:%(lineno)d] %(message)s",
    "datefmt": "%d.%m.%Y %H:%M:%S%z",
}


def setup_logs(app_name: str):
    Path("logs").mkdir(parents=True, exist_ok=True)
    logging_config = get_logging_config(app_name)
    logging.config.dictConfig(logging_config)


def get_logging_config(app_name: str):
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "main": {
                "()": CustomFormatter,
                "format": main_template["format"],
                "datefmt": main_template["datefmt"],
            },
            "errors": {
                "()": CustomFormatter,
                "format": error_template["format"],
                "datefmt": error_template["datefmt"],
            },
        },
        "handlers": {
            "stdout": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "main",
                "stream": sys.stdout,
            },
            "stderr": {
                "class": "logging.StreamHandler",
                "level": "WARNING",
                "formatter": "errors",
                "stream": sys.stderr,
            },
            "file": {
                "()": RotatingFileHandler,
                "level": "INFO",
                "formatter": "main",
                "filename": f"logs/{app_name}.log",
                "maxBytes": 50000000,
                "backupCount": 3,
                "encoding": "utf-8",
            },
        },
        "loggers": {
            "root": {
                "level": "DEBUG",
                "handlers": ["stdout", "stderr", "file"],
            },
        },
    }
