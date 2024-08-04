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
                 log_filename=f'CleanupDup.log',
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
    empty_files = list(handler.aggregate(
        [{'$match': {"doc_type": "av_info", 'videos': {'$size': 0}}}], show_id=True))
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

    proc = tqdm(incomplete_vids, desc='Process Incomplete Videos', unit='file')
    for cache_path in proc:
        dir_path = cache_path.parent
        vid_path = cache_path
        mkv_path = dir_path.joinpath(vid_path.name.replace('mp4', 'mkv'))
        # proc.set_description(f'Process: {cache_path.parent.name}')
        if vid_path.exists() and not mkv_path.exists():
            print(f'Process: {cache_path.parent}')
            if os.stat(vid_path).st_size == 0:
                shutil.rmtree(dir_path)
            # Convert mp4 to mkv
            cmd = f'avidemux_cli.exe --load "{vid_path}" --output-format MKV --save "{mkv_path}"'
            try:
                out = sp.check_output(cmd,
                                      shell=True,
                                      cwd=os.getenv('AVIDEMUX_CLI_PATH'),
                                      stderr=sp.STDOUT)
            except sp.CalledProcessError as e:
                log.warning('Remove Error File: %s', dir_path)
                shutil.rmtree(dir_path)

    # 刪除重複的影片(有.mkv)
    old_dst_path = Path(os.getenv('OLD_EYNY_DOWNLOAD_DST_PATH'))
    dst_path = Path(os.getenv('EYNY_DOWNLOAD_DST_PATH'))

    old_dst_files = list(handler.aggregate(
        [{'$match': {'parent': "Study_old"}}], show_id=True))

    proc = tqdm(old_dst_files, desc='Remove Old Files', unit='file')
    for old_file in proc:
        dst_files = list(handler.aggregate([{'$match': {'parent': "Study",
                                                        'dir_name': old_file['dir_name']
                                                        }}], show_id=True))
        for dst_file in dst_files:
            if not 'videos' in dst_file:
                dst_dir_path = dst_path.joinpath(dst_file["dir_name"])
                if len(list(dst_dir_path.rglob('*.mkv'))) == 0:
                    proc.set_description(f"Remove Empty: {dst_file['_id']}")
                    if dir_path.exists():
                        shutil.rmtree(dir_path)
                    handler.delete({'_id': dst_file['_id']})
            else:
                # Remove old dup file
                old_dst_dir_path = old_dst_path.joinpath(old_file["dir_name"])
                proc.set_description(f'Remove: {old_file["dir_name"]}')
                if old_dst_dir_path.exists():
                    shutil.rmtree(old_dst_dir_path)
                handler.delete({'_id': old_file['_id']})
