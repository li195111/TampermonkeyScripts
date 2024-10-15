import os
import threading
import uuid
from datetime import datetime
from enum import Enum
from typing import List, Optional

import pydantic
from bson import ObjectId

from models.logger import logger
from utils.general import error_msg


class IBase(pydantic.BaseModel):
    ...


class Error(IBase):
    '''Error Model'''
    title: str
    message: str

    @classmethod
    def from_exc(cls, exc_type_str: str, exc: Exception):
        title = f'{exc_type_str}: '
        msg = error_msg(exc)
        if isinstance(exc.args, (list, tuple)):
            args = [str(arg) for arg in exc.args]
            title += ';'.join(args)
        else:
            title += str(exc.args)
        return cls(title=title, message=msg)


class Log(object):
    def __init__(self, bot_type: Optional[Enum] = None, **kwargs) -> None:
        super().__init__()
        bot_type = f'{bot_type.value}_' if bot_type else ''
        if 'logger' in kwargs:
            log = kwargs.pop('logger')
        else:
            log = None
        self.logger = log or logger(name=self.__class__.__name__,
                                    log_filename=f'{bot_type}{self.__class__.__name__}.log',
                                    level=10 if os.getenv("DEBUG") else 20)


class LogThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        if 'logger' in kwargs:
            log = kwargs.pop('logger')
        else:
            log = None
        self.logger = log or logger(name=self.__class__.__name__,
                                    log_filename=f'{self.__class__.__name__}.log',
                                    level=10 if os.getenv("DEBUG") else 20)
        super().__init__(*args, **kwargs)


class BackupChannel(IBase):
    bot_id: str
    chat_id: str


class BackupMessage(BackupChannel):
    bot_id: str
    chat_id: str
    message_id: str


class BackupInfoTimeStamp(BackupMessage):
    message_timestamp: datetime


class Video(IBase):
    name: str
    type: str
    size: int
    width: int
    height: int


class MongoDoc(IBase):
    id: Optional[ObjectId] = pydantic.Field(alias="_id", default=None)
    dir_name: str
    parent: str
    source: str
    title: str
    videos: List[Video] = []
    snap_date: datetime
    doc_type: str
    tags: List[str] = []
    SN: Optional[str] = None
    tg_backup: Optional[List[BackupInfoTimeStamp]] = []
    on_local: Optional[bool] = True

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class History(IBase):
    '''Query History Document'''
    doc_type: str = 'query_history'
    query: str
    username: str
    history_id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    search_datetime: datetime = pydantic.Field(default_factory=datetime.now)
    count: Optional[int] = 1
