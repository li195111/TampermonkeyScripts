import os
import shutil
import subprocess as sp
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from tqdm import tqdm

from handlers.mongo import MongoHandler
from models.base import IBase, MongoDoc
from models.logger import logger
from playground import History


class CleanUp(IBase):
    docs: List[MongoDoc | History]


if __name__ == '__main__':
    load_dotenv()
    file_path = Path(__file__)
    os.environ['LOG_DIR'] = file_path.parent.joinpath('logs').as_posix()
    log = logger(name=file_path.name,
                 log_filename=f'CleanupDup.log',
                 level=10 if os.getenv("DEBUG") else 20)

    dst_path = Path(os.getenv('EYNY_DOWNLOAD_DST_PATH'))
    old_dst_path = Path(os.getenv('OLD_EYNY_DOWNLOAD_DST_PATH'))
    dst_dirs = [dst_path, old_dst_path]

    h = MongoHandler()

    new_docs = []
    need_cleanup = False
    # av_info 8442 > 8125 (317) > 8103 (19)
    origin_av_info_list = list(h.aggregate(
        [{'$match': {'doc_type': "av_info"}},]))
    drop_dup_aggs = [
        {'$match': {'doc_type': "av_info"}},
        {'$group': {'_id': {'dir_name': '$dir_name',
                            'parent': '$parent',
                            'title': '$title'},
                    'docs': {'$push': '$$ROOT'},
                    'count': {'$sum': 1}}},
        {'$project': {'unique_doc': {'$reduce': {'input': '$docs',
                                                 'initialValue': {'$arrayElemAt': ['$docs', 0]},
                                                 'in': {'$cond': [{'$and': [{'$ifNull': ['$$this.tg_backup', False]},
                                                                            {'$not': {'$ifNull': ['$$value.tg_backup', False]}}]},
                                                                  '$$this', '$$value']}}},
                      'count': 1}},
        {'$addFields': {"unique_doc.count": "$count"}},
        {'$replaceRoot': {'newRoot': "$unique_doc"}},
    ]
    drop_dup_av_info_list = [MongoDoc.model_validate(
        doc) for doc in h.aggregate(drop_dup_aggs)]
    if len(origin_av_info_list) != len(drop_dup_av_info_list):
        need_cleanup = True

    # query_history 64 > 29 (35)
    origin_history_list = list(h.aggregate(
        [{'$match': {'doc_type': "query_history"}},]))
    drop_dup_aggs = [
        {'$match': {'doc_type': "query_history"}},
        {'$group': {'_id': {'query': "$query"},
                    'unique_doc': {'$last': "$$ROOT", },
                    'count': {'$sum': 1, }}},
        {'$addFields': {"unique_doc.count": "$count"}},
        {'$replaceRoot': {'newRoot': "$unique_doc"}},
    ]
    drop_dup_query_history_list = [History.model_validate(
        doc) for doc in h.aggregate(drop_dup_aggs)]
    if (len(origin_history_list) != len(drop_dup_query_history_list)):
        need_cleanup = True

    if need_cleanup:
        result = h.delete({})
        print('Delete Origin Result:', result)
        new_docs = drop_dup_av_info_list + drop_dup_query_history_list
        result = h.insert(CleanUp(docs=new_docs).model_dump()['docs'])
        print('Insert Result:', result)

    # 刪除重複的影片(有.mp4, .mkv)
    mp4_files = list(h.aggregate([{'$match': {'doc_type': "av_info"}},
                                  {'$unwind': {
                                      'path': '$videos', 'includeArrayIndex': 'idx', 'preserveNullAndEmptyArrays': True}},
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
                h.update({'_id': file['_id']}, {
                    '$pull': {'videos': {'type': '.mp4'}}})
            else:
                h.delete({'_id': file['_id']})
                log.warning("Folder not found, At: %s %s",
                            folder_path.parent, folder_path.name)
    log.info("Number of MP4: %s, Remove: %s", len(mp4_files), remove_count)

    # 刪除無影片的資料夾
    empty_files = list(h.aggregate(
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
            h.delete({'_id': file['_id']})
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
    old_dst_files = list(h.aggregate(
        [{'$match': {'doc_type': "av_info", 'parent': "Study_old"}}], show_id=True))

    proc = tqdm(old_dst_files, desc='Remove Old Files', unit='file')
    for old_file in proc:
        dst_files = list(h.aggregate([{'$match': {'doc_type': "av_info",
                                                  'parent': "Study",
                                                  'dir_name': old_file['dir_name']
                                                  }}], show_id=True))
        if len(dst_files) > 0:
            for dst_file in dst_files:
                if not 'videos' in dst_file:
                    dst_path = dst_path.joinpath(dst_file["dir_name"])
                    if len(list(dst_path.rglob('*.mkv'))) == 0:
                        proc.set_description(
                            f"Remove Empty: {dst_file['_id']}")
                        if dir_path.exists():
                            shutil.rmtree(dir_path)
                        h.delete({'_id': dst_file['_id']})
                else:
                    # Remove old dup file
                    old_dst_path = old_dst_path.joinpath(
                        old_file["dir_name"])
                    proc.set_description(f'Remove: {old_file["dir_name"]}')
                    if old_dst_path.exists():
                        shutil.rmtree(old_dst_path)
                    h.delete({'_id': old_file['_id']})
        else:
            # Move old file to new folder
            old_dst_path = old_dst_path.joinpath(old_file["dir_name"])
            if old_dst_path.exists():
                dst_path = dst_path.joinpath(old_file["dir_name"])
                proc.set_description(f'Move: {old_file["dir_name"]}')
                shutil.move(old_dst_path, dst_path)
            else:
                # Remove old not exists file
                h.delete({'_id': old_file['_id']})
