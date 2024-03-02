import os
import platform
from pathlib import Path

from dotenv import load_dotenv

from handlers.mongo import MongoHandler
from StreamBot import BotType, URLDownloadBot

if __name__ == '__main__':
    load_dotenv()
    os.environ['MONGO_COLLECTION'] = 'IGB_IMAGES'
    os.environ['MONGO_SYS_COLLECTION'] = 'IGB_SYS'
    handler = MongoHandler()

    if platform.system().lower() == 'windows':
        user_profile_dir = Path(os.environ['USERPROFILE'])
        src_dirs = [user_profile_dir.joinpath('Downloads')]
        dst_dir = Path(os.getenv('IG_DOWNLOAD_DST_PATH'))
        dst_dir.mkdir(parents=True, exist_ok=True)
    elif platform.system().lower() == 'linux':
        src_dirs = []
    for src_dir in src_dirs:
        if src_dir.exists():
            if isinstance(src_dir, Path):
                src_dir = src_dir.as_posix()
            bot = URLDownloadBot(BotType.IG,
                                 src_dir,
                                 dst_dir,
                                 max_queue=10,
                                 max_threads=10)
            bot.run()
