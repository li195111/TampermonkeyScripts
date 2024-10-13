import asyncio
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from telegram import Bot, InputFile, Update
from telegram.error import NetworkError, RetryAfter, TelegramError, TimedOut
from telegram.ext import CallbackContext, MessageHandler, Updater
from telegram.request import HTTPXRequest

from StreamBot.utils import error_msg


async def get_all_messages():
    bot_token = os.getenv('TG_BOT_TOKEN')
    chat_id = os.getenv('TG_CHANNEL_ID')
    local_bot_api_url = 'http://localhost:8089/bot'

    # 使用自定義的 base_url 創建 Bot 實例
    request = HTTPXRequest(connection_pool_size=8,
                           read_timeout=3600,
                           write_timeout=3600,
                           connect_timeout=60,
                           media_write_timeout=3600,
                           )
    bot = Bot(token=bot_token, request=request, base_url=local_bot_api_url)

    update_id = 0

    try:
        # 使用getUpdates方法獲取最新的訊息
        updates = await bot.get_updates(offset=update_id, timeout=50)
    except TelegramError as e:
        print(f"發生錯誤：{e}")
        updates = []


    for update in updates:
        print('Update')
        print(update)
        update_id = update.update_id + 1

        try:
            user_command = update.message.text
            print('User Command:', user_command)
        except Exception as e:
            print(error_msg(e))

        try:
            video = update.message.video
            name = "{}-{}-{}x{}.mp4".format(video.file_name,update.update_id,video.width,video.height)
            tfile = await bot.getFile(video.file_id)
            print('File Name:', name)
            print('File Path:', tfile.file_path)
            # filename.append(name)
            # urls.append(tfile.file_path)
        except Exception as e:
            print(error_msg(e))

    # messages = []
    # async for update in updates:
        
    #     if update.channel_post and update.channel_post.chat.id == chat_id:
    #         print(update.channel_post.text)
    #         messages.append(update.channel_post.text)
    # return messages

if __name__ == "__main__":
    load_dotenv()
    asyncio.run(get_all_messages())
