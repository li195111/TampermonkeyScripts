import os
import threading

import pydantic

from models.logger import logger


class IBase(pydantic.BaseModel):
    ...


class Log(object):
    def __init__(self) -> None:
        super().__init__()
        self.logger = logger(name=self.__class__.__name__,
                             level=10 if os.getenv("DEBUG") else 20)


class LogThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger(name=self.__class__.__name__,
                             level=10 if os.getenv("DEBUG") else 20)
