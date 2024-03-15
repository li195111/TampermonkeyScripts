"""
logger object
"""
import logging
import os
import sys
import time
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

log_config = {
    "version": 1,
    "formatters": {
        "file": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "[%(levelname)s] %(asctime)s %(name)s:%(filename)s:%(lineno)d %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": None,
        }
    },
    "handlers": {
        "file": {
            "formatter": "file",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/StreamDownloader.log",
            "when": "D",  # Daily rotation
            "interval": 1,  # Rotate once a day
            "backupCount": 30,  # Keep last 7 days logs
        }
    },
    "loggers": {
        "uvicorn": {"handlers": ["file"], "level": "INFO", "propagate": False},
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["file"], "level": "INFO", "propagate": False},
    },
}

class CustTimedRotatingFileHandler(TimedRotatingFileHandler):

    def rotate(self, source: str, dest: str) -> None:
        try:
            return super().rotate(source, dest)
        except PermissionError:
            ...

class logger:
    """
    name: name of logger, must
    level: log msg level.
    log_filename: filename of log file(do note include dates), default None
    std_out: whether to log to stdout, default True
    """

    def __new__(self,
                name,
                level: int = 20,
                log_filename: str = 'StreamDownloader.log',
                std_out: bool = True,
                interval=log_config['handlers']['file']['interval'],
                when=log_config['handlers']['file']['when'],
                backupCount=log_config['handlers']['file']['backupCount'],
                **kwargs):
        lg = logging.getLogger(name)
        lg.setLevel(level)
        handlers = []
        fmt = log_config["formatters"]['file']['fmt']
        formatter = logging.Formatter(fmt=fmt)
        if std_out:
            stream_handler = logging.StreamHandler(stream=sys.stdout)
            stream_handler.setFormatter(formatter)
            handlers.append(stream_handler)
        self.time_rotate_hanlder = None
        if log_filename:
            log_dir = Path(os.getenv("LOG_DIR") or "logs")
            log_dir.mkdir(exist_ok=True)
            log_config['handlers']['file']['filename'] = log_dir.joinpath(
                log_filename).as_posix()

            self.time_rotate_hanlder = CustTimedRotatingFileHandler(
                # housekeeping is delete file by this filename as prefix
                filename=log_config['handlers']['file']['filename'],
                interval=interval,
                when=when,  # one file every {interval} Day
                backupCount=backupCount,  # keep latest 30 files
                encoding="utf-8")
            self.time_rotate_hanlder.doRollover()
            self.time_rotate_hanlder.setFormatter(formatter)
            handlers.append(self.time_rotate_hanlder)

        for h in handlers:
            lg.addHandler(h)
        return lg


if __name__ == "__main__":
    test_logger = logger(name="test", level=20)
    test_logger.info("test log out msg")
