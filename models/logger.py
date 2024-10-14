"""
logger object
"""
import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class logger:
    """
    name: name of logger, must
    level: log msg level.
    log_filename: filename of log file(do note include dates), default None
    std_out: whether to log to stdout, default True
    """

    def __new__(self,
                name,
                level: int = 10 if os.getenv("DEBUG") else 20,
                log_filename: str = None,
                std_out: bool = True,
                interval=1,
                when="D",
                backupCount=30,
                **kwargs):
        lg = logging.getLogger(name)
        lg.setLevel(level)
        handlers = []
        fmt = "[%(levelname)s] %(asctime)s %(filename)s:%(lineno)d %(message)s"
        formatter = logging.Formatter(fmt=fmt)
        if std_out:
            stream_handler = logging.StreamHandler(stream=sys.stdout)
            stream_handler.setFormatter(formatter)
            handlers.append(stream_handler)

        if log_filename:
            log_dir = Path(os.getenv("LOG_DIR") or "logs")
            log_dir.mkdir(exist_ok=True)

            time_rotate_hanlder = TimedRotatingFileHandler(
                # housekeeping is delete file by this filename as prefix
                filename=log_dir.joinpath(log_filename),
                interval=interval,
                when=when,  # one file every {interval} Day
                backupCount=backupCount,  # keep latest 30 files
                encoding="utf-8")
            time_rotate_hanlder.setFormatter(formatter)
            handlers.append(time_rotate_hanlder)

        for h in handlers:
            lg.addHandler(h)
        return lg


if __name__ == "__main__":
    test_logger = logger(name="test", level=20)
    test_logger.info("test log out msg")
