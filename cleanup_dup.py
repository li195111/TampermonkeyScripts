import os
import shutil
import subprocess as sp
from pathlib import Path
from typing import List

from tqdm import tqdm
from dotenv import load_dotenv

from models.logger import logger
from handlers.mongo import MongoHandler


if __name__ == '__main__':
    load_dotenv()
    file_path = Path(__file__)
    os.environ['LOG_DIR'] = file_path.parent.joinpath('logs').as_posix()
    log = logger(name=file_path.name,
                 log_filename=f'HouseKeepVideos.log',
                 level=10 if os.getenv("DEBUG") else 20)
    dst_dirs = [
        Path(os.getenv('EYNY_DOWNLOAD_DST_PATH')),
        Path(os.getenv('OLD_EYNY_DOWNLOAD_DST_PATH')),
    ]

    handler = MongoHandler()

    # 刪除重複的影片(有.mp4, .mkv)
    mp4_files = list(handler.aggregate([{'$unwind': {'path': '$videos', 'includeArrayIndex': 'idx', 'preserveNullAndEmptyArrays': True}},
                                        {'$match': {'videos.type': '.mp4'}}], show_id=True))
    remove_count = 0
    for file in tqdm(mp4_files, desc="Remove MP4"):
        dst_dir = [dst for dst in dst_dirs if dst.name == file['parent']]
        if dst_dir:
            dst_dir = dst_dir[0]
            folder_path = dst_dir.joinpath(file['dir_name'])
            if folder_path.exists():
                mp4_path = folder_path.joinpath(
                    f"{file['videos']['name']}{file['videos']['type']}")
                if mp4_path.exists():
                    log.info("Remove: %s", mp4_path)
                    os.remove(mp4_path)
                    remove_count += 1
                log.info("Update: %s", file['_id'])
                handler.update({'_id': file['_id']}, {
                               '$pull': {'videos': {'type': '.mp4'}}})
            else:
                handler.delete({'_id': file['_id']})
                log.warning("Folder not found, At: %s %s",
                            folder_path.parent, folder_path.name)
    log.info("Number of MP4: %s, Remove: %s", len(mp4_files), remove_count)

    # 刪除無影片的資料夾
    empty_files = list(handler.aggregate([{'$match': {"doc_type":"av_info", 'videos': {'$size': 0}}}], show_id=True))
    remove_count = 0
    for file in tqdm(empty_files, desc="Remove Empty"):
        dst_dir = [dst for dst in dst_dirs if dst.name == file['parent']]
        if dst_dir:
            dst_dir = dst_dir[0]
            folder_path = dst_dir.joinpath(file['dir_name'])
            if folder_path.exists():
                shutil.rmtree(folder_path)
                remove_count += 1
                log.info("Update: %s", file['_id'])
            handler.delete({'_id': file['_id']})
    log.info("Number of Empty: %s, Remove: %s", len(empty_files), remove_count)

    # 列出所有.mp4檔案
    incomplete_vids: List[Path] = []
    for dst_dir in dst_dirs:
        if dst_dir.exists():
            incomplete_vids.extend(list(dst_dir.rglob('*.mp4')))
    log.info('Total Incomplete: %s', len(incomplete_vids))

    for cache_path in incomplete_vids:
        dir_path = cache_path.parent
        vid_path = cache_path
        mkv_path = dir_path.joinpath(vid_path.name.replace('mp4', 'mkv'))
        print('Process: %s', cache_path.parent)
        print('\tMKV Path: %s', mkv_path.exists())
        print('\tMP4 Path: %s', vid_path.exists())
        if vid_path.exists() and not mkv_path.exists():
            # Convert mp4 to mkv
            cmd = f'avidemux_cli.exe --load "{vid_path}" --output-format MKV --save "{mkv_path}"'
            out = sp.check_output(cmd,
                                  shell=True,
                                  cwd=os.getenv('AVIDEMUX_CLI_PATH'),
                                  stderr=sp.STDOUT)
            
        #     try:
        #         is_error = ('Error' in out.decode())
        #     except UnicodeDecodeError:
        #         is_error = ('Error' in out)
        #     if is_error:
        #         log.warning('Remove Error File: %s', dir_path)
        #         shutil.rmtree(dir_path.as_posix())
        # else:
        #     ...
