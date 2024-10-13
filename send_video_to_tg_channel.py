import asyncio
import os
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import List, Optional

from bson import ObjectId
from dotenv import load_dotenv
from pydantic import Field
from telegram import Bot, InputFile
from telegram.error import NetworkError, RetryAfter, TimedOut
from telegram.request import HTTPXRequest
from tqdm import tqdm

from handlers.mongo import MongoHandler
from models.base import IBase
from models.logger import logger
from StreamBot.utils import error_msg


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
    id: Optional[ObjectId] | None = Field(alias="_id", default=None)
    dir_name: str
    parent: str
    source: str
    title: str
    videos: List[Video] = []
    snap_date: datetime
    doc_type: str
    tags: List[str] = []
    SN: Optional[str] | None = None
    tg_backup: Optional[List[BackupInfoTimeStamp]] = []
    on_local: Optional[bool] = True

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


async def send_mkv_video(bot_token: str, chat_id: str, video_path: str | Path, sn: str, log: Optional[Logger] = None):
    if not log:
        log = print
    else:
        log = log.debug

    bot_api_url = "https://api.telegram.org/bot"
    local_bot_api_url = 'http://localhost:8089/bot'
    # 使用自定義的 base_url 創建 Bot 實例
    request = HTTPXRequest(connection_pool_size=8,
                           read_timeout=3600,
                           write_timeout=3600,
                           connect_timeout=60,
                           media_write_timeout=3600,
                           )
    bot = Bot(token=bot_token,
              request=request,
              base_url=local_bot_api_url if use_local_api else bot_api_url)
    await bot.initialize()

    if isinstance(video_path, str):
        video_path = Path(video_path)
    file_path = video_path.absolute()

    try:
        title = file_path.parent.name[5:]
        log(f"上傳至 Channel: {chat_id} ...")
        st = datetime.now()
        with open(file_path, 'rb') as fp:
            fp.seek(0)
            input_file = InputFile(fp.read(), filename=file_path.name)
            message_timestamp = datetime.now()
            video_message = await bot.send_video(
                chat_id=chat_id,
                video=input_file,
                filename=file_path.name,
                caption=f'番號: {sn or ""}\n片名：{title}\nBackup At: {message_timestamp.strftime("%Y-%m-%d")}',
                parse_mode=None,
                supports_streaming=True,
            )
        et = datetime.now()
        log(f"\n上傳成功！ 費時: {et - st}")
        backup_info = {'bot_id': str(bot.id),
                       'chat_id': str(chat_id),
                       'message_id': str(video_message.id),
                       'message_timestamp': message_timestamp
                       }
        return BackupInfoTimeStamp(**backup_info)
    except TimedOut:
        log("\n上傳超時。可能需要更長的 timeout 時間或更好的網絡連接。")
    except RetryAfter as e:
        log(f"\n超過速率限制。建議等待 {e.retry_after} 秒後重試。")
    except NetworkError as e:
        log(f"\n網絡錯誤：{e}. 請檢查你的網絡連接和本地 Bot API 服務器狀態。")
    except KeyboardInterrupt:
        log("\n用戶中斷了程序。")
    except Exception as e:
        log(f"\n上傳視頻時發生錯誤: {type(e).__name__}: {e}")

if __name__ == "__main__":
    load_dotenv()

    file_path = Path(__file__)
    os.environ['LOG_DIR'] = file_path.parent.joinpath('logs').as_posix()
    log = logger(name=file_path.name,
                 log_filename=f'TGBackup.log',
                 level=10 if os.getenv("DEBUG") else 20)

    bot_token = os.getenv('TG_BOT_TOKEN')
    chat_ids = os.getenv('TG_CHANNEL_IDS').split(',')
    use_local_api = True

    try:
        h = MongoHandler()
        h.default_col = 'AVB_VIDEOS'
        h.default_sys_col = 'AVB_SYS'

        dir_path = [Path(p) for p in os.getenv('VID_DIR_PATH').split(',')]

        results = h.aggregate([
            {'$match': {'doc_type': 'av_info'}},
            {'$sort': {'snap_date': 1}}], show_id=True)
        docs = [MongoDoc.model_validate(doc)
                for doc in results]
        for doc in tqdm(docs, desc="Backup Video to TG"):
            video_dir_path = [d for d in dir_path if d.name == doc.parent]
            if len(video_dir_path) > 0:
                video_dir_path = video_dir_path[0]
            if isinstance(doc.videos, list):
                for video in doc.videos:
                    if video.type == '.mkv':
                        video_name = f"{video.name}{video.type}"
                        if video_dir_path:
                            av_dir_path = video_dir_path.joinpath(doc.dir_name)
                            av_dir_exists = av_dir_path.exists()
                            if av_dir_exists:
                                av_path = av_dir_path.joinpath(video_name)

                                backup_channels = []
                                backup_messages = []
                                if doc.tg_backup:
                                    for backup in doc.tg_backup:
                                        backup_channels.append(BackupChannel(
                                            **backup.model_dump(exclude=['message_timestamp', 'message_id'])))
                                        backup_messages.append(BackupMessage(
                                            **backup.model_dump(exclude=['message_timestamp'])))

                                title = av_path.absolute().parent.name[5:]
                                log.debug(f"開始上傳 {title} ...")

                                for chat_id in tqdm(chat_ids, desc=f"Backup {title} to TG Group", leave=False):
                                    bot_id = str(bot_token.split(':')[0])
                                    backup_channel = BackupChannel(
                                        bot_id=bot_id, chat_id=chat_id)
                                    if backup_channel in backup_channels:
                                        log.debug(
                                            f'Skip: {title} at: {backup_channel}')
                                        continue

                                    backup_info_timestamp = asyncio.run(
                                        send_mkv_video(bot_token, chat_id, av_path, doc.SN, log))
                                    if backup_info_timestamp is not None:
                                        backup_info = BackupMessage(
                                            **backup_info_timestamp.model_dump(exclude=['message_timestamp']))
                                        if backup_info not in backup_messages:
                                            log.debug('更新 TG Backup 資訊')
                                            h.update({'_id': doc.id},
                                                     {'$push': {'tg_backup': backup_info_timestamp.model_dump()}})
    except KeyboardInterrupt:
        log.debug("\n用戶中斷了程序。")
    except Exception as e:
        log.error(f"發生錯誤：{error_msg(e)}")
