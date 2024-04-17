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
                             log_filename=f'{self.__class__.__name__}.log',
                             level=10 if os.getenv("DEBUG") else 20)


class LogThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        if 'logger' in kwargs:
            logger = kwargs.pop('logger')
        else:
            logger = None
        self.logger = logger or logger(name=self.__class__.__name__,
                             log_filename=f'{self.__class__.__name__}.log',
                             level=10 if os.getenv("DEBUG") else 20)
        super().__init__(*args, **kwargs)
