import os

from models.logger import logger


class Log(object):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logger(name=self.__class__.__name__,
                             level=10 if os.getenv("DEBUG") else 20)
