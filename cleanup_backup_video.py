import os
import shutil
from pathlib import Path

from dotenv import load_dotenv
from tqdm import tqdm

from handlers.mongo import MongoHandler
from models.logger import logger
from send_video_to_tg_channel import MongoDoc

if __name__ == '__main__':
    load_dotenv()
    file_path = Path(__file__)
    os.environ['LOG_DIR'] = file_path.parent.joinpath('logs').as_posix()
    log = logger(name=file_path.name,
                 log_filename=f'CleanupBackuped.log',
                 level=10 if os.getenv("DEBUG") else 20)

    dst_path = Path(os.getenv('EYNY_DOWNLOAD_DST_PATH'))
    old_dst_path = Path(os.getenv('OLD_EYNY_DOWNLOAD_DST_PATH'))
    dst_dirs = [dst_path, old_dst_path]

    h = MongoHandler()

    # 刪除已備份的影片
    results = list(h.aggregate([{'$match': {'doc_type': 'av_info',
                                            'tg_backup': {'$exists': True},
                                            '$expr': {'$gte': [{'$size': "$tg_backup"}, 2]},
                                            'on_local': {'$exists': False}}},
                                ], show_id=True))
    backuped_docs = [MongoDoc.model_validate(doc) for doc in results]
    for doc in tqdm(backuped_docs, desc="Remove Backuped"):
        if not doc.on_local:
            continue
        dst_dir = [dst for dst in dst_dirs if dst.name == doc.parent]
        if dst_dir:
            folder_path = dst_dir[0].joinpath(doc.dir_name)
            if folder_path.exists():
                shutil.rmtree(folder_path)
                h.update({'_id': doc.id}, {'$set': {'on_local': False}})
                log.debug("Removed: %s", folder_path)
