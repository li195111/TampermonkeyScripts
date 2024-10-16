import asyncio
import os
import random
from asyncio import Semaphore
from collections import deque
from datetime import datetime
from logging import Logger
from pathlib import Path
from typing import Deque, Dict, Optional, Set

import aiofiles
from dotenv import load_dotenv
from telegram import Bot, InputFile
from telegram.error import NetworkError, RetryAfter, TimedOut
from telegram.request import HTTPXRequest

from handlers.mongo import MongoHandler
from models.base import (BackupChannel, BackupInfoTimeStamp, BackupMessage,
                         Error, MongoDoc)
from models.logger import logger

MAX_FILE_SIZE = 2000 * 1024 * 1024  # 2000 MB (adjust as needed)


def init_mongo_handler():
    h = MongoHandler()
    h.default_col = 'AVB_VIDEOS'
    h.default_sys_col = 'AVB_SYS'
    return h


def init_logger(name: str, log_filename: str, level: int = 10 if os.getenv("DEBUG") else 20):
    return logger(name=name, log_filename=log_filename, level=level)


async def download_file(file_path: Path, semaphore: Semaphore) -> Optional[Path]:
    async with semaphore:
        try:
            async with aiofiles.open(file_path, 'rb') as file:
                await file.read()  # 模擬文件讀取操作
            return file_path
        except FileNotFoundError:
            return file_path
        except Exception as e:
            err = Error.from_exc('download_file 發生錯誤 Exception: ', e)
            print(err.title)
            print(err.message)
            return None


class DownloadManager:
    def __init__(self, max_concurrent_downloads: int = 5):
        self.download_queue: Deque[Path] = deque()
        self.semaphore = Semaphore(max_concurrent_downloads)
        self.downloaded_files: Dict[Path, Path] = {}
        self.active_downloads: Set[asyncio.Task] = set()
        self.total_preload: int = 0
        self.completed_preload: int = 0
        self.preload_numbers: int = 1

    async def add_to_queue(self, file_path: Path):
        self.download_queue.append(file_path)
        self.total_preload += 1
        task = asyncio.create_task(self._process_queue())
        self.active_downloads.add(task)
        task.add_done_callback(self.active_downloads.discard)

    async def wait_all_downloads(self):
        while self.active_downloads or self.download_queue:
            await asyncio.sleep(0.1)

    async def _process_queue(self):
        while self.download_queue:
            file_path = self.download_queue.popleft()
            if file_path not in self.downloaded_files:
                downloaded_file = await download_file(file_path, self.semaphore)
                if downloaded_file:
                    self.downloaded_files[file_path] = downloaded_file
                    self.completed_preload += 1

    async def get_downloaded_file(self, file_path: Path) -> Optional[Path]:
        while file_path not in self.downloaded_files:
            await asyncio.sleep(0.1)
        return self.downloaded_files.pop(file_path)

    def get_preload_status(self):
        return self.completed_preload, self.total_preload


async def preload_videos(idx: int, docs: list[MongoDoc], dir_path: list[Path], log: Logger, download_manager: DownloadManager):
    total_docs = len(docs)
    preload_count = 0
    # 預先下載接下來的 N 個影片
    for i in range(1, download_manager.preload_numbers + 1):
        next_idx = idx + i
        if next_idx < total_docs:
            # log.info(f"預先下載影片: {docs[next_idx].dir_name[5:]}")
            next_av_path = get_av_file(docs[next_idx], dir_path, log)
            if next_av_path:
                await download_manager.add_to_queue(next_av_path)
                preload_count += 1
    return preload_count


async def main(log: Logger, h: MongoHandler):
    download_manager = DownloadManager()

    bot_token = os.getenv('TG_BOT_TOKEN')
    chat_ids = os.getenv('TG_CHANNEL_IDS').split(',')
    use_local_api = True
    max_retries = 3

    dir_path = [Path(p) for p in os.getenv('VID_DIR_PATH').split(',')]

    results = h.aggregate([
        {'$match': {'doc_type': 'av_info'}},
        {'$sort': {'snap_date': 1}}], show_id=True)
    docs = [MongoDoc.model_validate(doc)
            for doc in results]

    # 假設這是你的主要處理循環
    for idx, doc in enumerate(docs):
        av_path = get_av_file(doc, dir_path, log)
        if av_path:
            # log.info(f"預先下載影片: {av_path.absolute().parent.name[5:]}")
            await download_manager.add_to_queue(av_path)

        # 預先下載接下來的 N 個影片
        # 在後台啟動預加載任務
        preload_task = asyncio.create_task(preload_videos(
            idx, docs, dir_path, log, download_manager))

        if av_path:
            # 等待當前影片下載完成
            downloaded_file = await download_manager.get_downloaded_file(av_path)
            if downloaded_file and downloaded_file.exists():
                # 使用下載好的文件進行後續操作
                await process_video(h=h,
                                    doc=doc,
                                    file_path=downloaded_file,
                                    bot_token=bot_token,
                                    chat_ids=chat_ids,
                                    log=log,
                                    use_local_api=use_local_api,
                                    max_retries=max_retries)

        # 等待預加載任務完成
        preload_count = await preload_task

        # 獲取預加載狀態
        completed, total = download_manager.get_preload_status()

        # # 檢查：在處理下一個影片之前，確保至少有5個影片在隊列中
        # while len(download_manager.download_queue) < 5 and idx + 1 < len(docs):
        #     completed, total = download_manager.get_preload_status()
        #     log.info(f"已處理 {idx + 1}/{len(docs)} 個影片")
        #     await asyncio.sleep(1)

        # 添加一個進度日誌
        # log.info(f"已處理 {idx + 1}/{len(docs)} 個影片")

    # 等待所有下載任務完成
    await download_manager.wait_all_downloads()


def calculate_transfer_time(file_size_mb, upload_speed_mbps):
    # 轉換檔案大小為 bits
    file_size_bits = file_size_mb * 8 * 1024 * 1024

    # 計算傳輸時間（秒）
    transfer_time_seconds = file_size_bits / (upload_speed_mbps * 1024 * 1024)

    # 轉換為分鐘和秒
    minutes = int(transfer_time_seconds // 60)
    seconds = int(transfer_time_seconds % 60)

    return transfer_time_seconds, minutes, seconds


async def process_video(h: MongoHandler, doc: MongoDoc, file_path: Path, bot_token: str, chat_ids: list[str], log: Logger, use_local_api: bool = False, max_retries: int = 3):
    # 這裡放置你的影片處理和上傳邏輯
    backup_channels = []
    backup_messages = []
    if doc.tg_backup:
        for backup in doc.tg_backup:
            backup_channels.append(BackupChannel(
                **backup.model_dump(exclude=['message_timestamp', 'message_id'])))
            backup_messages.append(BackupMessage(
                **backup.model_dump(exclude=['message_timestamp'])))
    if file_path.exists():
        h.update({'_id': doc.id}, {'$set': {'on_local': True}})

    title = file_path.absolute().parent.name[5:]
    if file_path.stat().st_size > MAX_FILE_SIZE:
        log(f"文件大小超過限制：{file_path}")
        return  # Skip this file
    file_size_mb = file_path.stat().st_size / (1024 * 1024)
    upload_speed_mbps = 30  # 30 Mbps
    buffer_factor = 1.2  # 增加 20% 的緩衝時間
    ttl_seconds, minutes, seconds = calculate_transfer_time(
        file_size_mb, upload_speed_mbps)
    log.info(f"開始 Backup {title} to TG Group")
    log.info(f"大小：{file_size_mb:.2f} MB")
    log.info(f'預估傳輸時間：{minutes} 分 {seconds} 秒, 共 {ttl_seconds:.0f} 秒')
    max_ttl_seconds, max_minutes, max_seconds = calculate_transfer_time(
        file_size_mb, upload_speed_mbps / buffer_factor)
    log.info(f"考慮網絡波動，預估傳輸時間範圍：")
    log.info(
        f"{minutes}分{seconds}秒 - {max_minutes}分{max_seconds}秒, 共 {max_ttl_seconds:.0f} 秒")

    for chat_id in chat_ids:
        bot_id = str(bot_token.split(':')[0])
        backup_channel = BackupChannel(
            bot_id=bot_id, chat_id=chat_id)
        if backup_channel in backup_channels:
            log.info(f'Skip at: {backup_channel}')
            continue

        async with aiofiles.open(file_path, 'rb') as file:
            file_content = await file.read()
            input_file = InputFile(file_content, filename=file_path.name)

        backup_info_timestamp = await send_mkv_video(bot_token,
                                                     chat_id,
                                                     title=title,
                                                     filename=file_path.name,
                                                     input_file=input_file,
                                                     sn=doc.SN,
                                                     log=log,
                                                     use_local_api=use_local_api,
                                                     max_retries=max_retries)
        if backup_info_timestamp is not None:
            backup_info = BackupMessage(
                **backup_info_timestamp.model_dump(exclude=['message_timestamp']))
            if backup_info not in backup_messages:
                log.info('更新 TG Backup 資訊')
                h.update({'_id': doc.id},
                         {'$push': {'tg_backup': backup_info_timestamp.model_dump()}})


async def send_mkv_video(bot_token: str, chat_id: str, title: str, filename: str, input_file: InputFile, sn: str, log: Optional[Logger] = None, use_local_api: bool = False, max_retries: int = 3) -> Optional[BackupInfoTimeStamp]:
    if not log:
        log = print
    else:
        log = log.info

    bot_api_url = "https://api.telegram.org/bot"
    local_bot_api_url = 'http://localhost:8089/bot'
    # 使用自定義的 base_url 創建 Bot 實例
    request = HTTPXRequest(connection_pool_size=12,  # 最大連接數
                           read_timeout=1*60*60,  # 1 小時
                           write_timeout=1*60*60,  # 1 小時
                           connect_timeout=1*60*15,  # 15 分鐘
                           media_write_timeout=1*60*60,  # 1 小時
                           )
    bot = Bot(token=bot_token,
              request=request,
              base_url=local_bot_api_url if use_local_api else bot_api_url)
    await bot.initialize()

    finished = False
    tries = 0
    retry_delay = 1

    while not finished and tries < max_retries:
        try:
            log(f"上傳至 Channel: {chat_id} ...")
            st = datetime.now()
            video_message = await bot.send_video(
                chat_id=chat_id,
                video=input_file,
                filename=filename,
                caption=f'番號: {sn or ""}\n片名: {title}\nBackup At: {st.strftime("%Y-%m-%d %H:%M:%S.%f")}',
                parse_mode=None,
                supports_streaming=True,
            )
            et = datetime.now()
            log(f"上傳成功！ 費時: {et - st}")
            backup_info = {'bot_id': str(bot.id),
                           'chat_id': str(chat_id),
                           'message_id': str(video_message.id),
                           'message_timestamp': st
                           }
            return BackupInfoTimeStamp(**backup_info)
        except (TimedOut, NetworkError) as e:
            err = Error.from_exc('Network Error: ', e)
            log(err.title)
            log(err.message)
            log(
                f"網絡錯誤: 請檢查你的網絡連接和本地 Bot API 服務器狀態。 重試... {tries + 1}/{max_retries}")
            tries += 1

            retry_delay *= 2  # Exponential backoff
            jitter = random.uniform(0, 0.1 * retry_delay)  # Add jitter
            wait_time = retry_delay + jitter

            log(f"將在 {wait_time:.2f} 秒後重試 (重試 {tries}/{max_retries})...")
            await asyncio.sleep(wait_time)
        except KeyboardInterrupt:
            log("用戶中斷了程序。")
            finished = True
        except Exception as e:
            err = Error.from_exc('上傳影片時發生錯誤 Exception: ', e)
            log(err.title)
            log(err.message)
            finished = True
    return None


def get_av_file(doc: MongoDoc, dir_path: list[Path], log: Logger):
    try:
        video_dir_path = [d for d in dir_path if d.name == doc.parent]
        if len(video_dir_path) > 0:
            video_dir_path = video_dir_path[0]
        if isinstance(doc.videos, list):
            for video in doc.videos:
                if video_dir_path and video.type == '.mkv':
                    av_dir_path = video_dir_path.joinpath(doc.dir_name)
                    if av_dir_path.exists():
                        return av_dir_path.joinpath(f"{video.name}{video.type}")
    except Exception as e:
        err = Error.from_exc('get_av_file 發生錯誤 Exception: ', e)
        log(err.title)
        log(err.message)
        return


if __name__ == "__main__":
    load_dotenv()
    file_path = Path(__file__)
    os.environ['LOG_DIR'] = file_path.parent.joinpath('logs').as_posix()
    log_config = {
        'name': file_path.name,
        'log_filename': 'TGBackup.log',
    }
    log = init_logger(**log_config)
    h = init_mongo_handler()

    try:
        asyncio.run(main(log, h))
    except KeyboardInterrupt:
        log.info("用戶中斷了程序。")
    except Exception as e:
        err = Error.from_exc('主程序發生錯誤 Exception: ', e)
        log.error(err.title)
        log.error(err.message)
    finally:
        h.client.close()
        log.info("程序結束。")
