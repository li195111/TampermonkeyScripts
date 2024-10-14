import os
import re
from datetime import datetime, time
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from tqdm import tqdm

from handlers.mongo import MongoHandler
from models.logger import logger
from utils import get_video_infos, split_tags

if __name__ == '__main__':
    st = datetime.now()
    load_dotenv()
    log = logger(name='AV')
    h = MongoHandler()
    h.default_col = 'AVB_VIDEOS'
    h.default_sys_col = 'AVB_SYS'

    dir_path = [Path(p) for p in os.getenv('VID_DIR_PATH').split(',')]
    videos: List[Path] = []
    for dp in dir_path:
        log.info(f'Dir Path: {dp.exists()} {dp}')
        videos.extend(list(dp.glob('*')))
    snap_date = datetime.combine(datetime.today(), time.min)

    docs = []
    vid_types = ['mkv', 'mp4']
    tag_regs = [r"\(.*?\)", r"\[.*?\]"]
    regexs = [r'[a-zA-Z]?[a-zA-Z]?[a-zA-Z]?[a-zA-Z][a-zA-Z][ ]?[\-]?[0-9][0-9][0-9][0-9]?',
              r'[0-9]?[0-9]?[0-9]?[a-zA-Z]?[a-zA-Z]?[a-zA-Z]?[a-zA-Z][a-zA-Z][ ]?[\-]?[0-9][0-9][0-9][0-9]?',
              r'FC2[\-]?[\_]?[ ]?PPV[\-]?[ ]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?']
    title_filters = ['_無修正_口交.爆乳.中出.內射.流出.國產.本土.露臉',
                     '無修正.口交.爆乳.中出.內射.流出.國產.本土.露臉',
                     '專營FC2PPV_無碼無修.偷拍流出.本土國產',
                     '歐美日韓.無碼.偷拍.流出']
    try:
        for p in tqdm(videos, desc='Video Progress'):
            update = False
            dir_name = p.name
            parent = p.parent.name

            # Check Exists
            doc = h.query_one(
                {'dir_name': dir_name, 'parent': parent}, show_id=True) or {'doc_type': 'av_info'}

            old_docs = list(h.query({'$and': [{'dir_name': dir_name}]})) or []
            if len(old_docs) == 1:
                old_doc = old_docs[0]
            else:
                old_doc = {}
            exists_vids = doc.get('videos') or old_doc.get('videos') or []

            name_split = p.name.split('_')
            src = name_split[0]
            title = '_'.join(name_split[1:])
            for title_f in title_filters:
                if len(title_f) > 15:
                    for i in range(7):
                        title = title.replace(title_f[:-i], '')
                else:
                    title = title.replace(title_f, '')
            title = title.replace('_', ' ')

            # SN
            matches = [re.findall(reg, title) for reg in regexs]
            sn_code = None
            for m in matches:
                if m:
                    sn_code = m[0].replace(' ', '-').replace('_', '').upper()
            if sn_code:
                title = title.replace(sn_code, '')

            # Tag
            tags = []
            for r in tag_regs:
                pattern = re.compile(r)
                tag_ms = pattern.search(title)
                if tag_ms:
                    tag_barket = tag_ms.group()
                    title = title.replace(tag_barket, '')
                    tag = tag_barket[1:-1]
                    if tag and not tag.isnumeric():
                        split_tags(tag, tags)
            filted_tags = []
            for tag in tags:
                ms = []
                for reg in regexs:
                    ms.extend(re.findall(reg, tag))
                if ms:
                    continue
                filted_tags.append(tag)
            filted_tags.sort()

            # Video Infos
            exists_vid_names = [
                f"{v['name']}{v['type']}" for v in exists_vids if v.get('name')]
            exists_vid_names.sort()
            vids = []
            complete = list(p.glob(f'*.mkv'))
            if complete:
                for t in vid_types:
                    vs = list(p.glob(f'*.{t}'))
                    for v in vs:
                        v_name = v.stem
                        if f"{v_name}{v.suffix}" in exists_vid_names:
                            continue
                        v_p = v.as_posix()
                        vid_infos = get_video_infos(v_p)
                        size = os.path.getsize(v_p)
                        infos = {'name': v_name, 'type': v.suffix,
                                 'size': size, **vid_infos}
                        vids.append(infos)
            vid_names = [f"{v['name']}{v['type']}" for v in vids]
            vid_names.sort()

            # Special Title Filter
            chars = [' 00', '~', '»', '★']
            for char in chars:
                title = title.replace(char, '')

            while '  ' in title:
                title = title.replace('  ', ' ')
            title = title.strip()

            # log.info(f'obj size: {len(doc)}\n{doc}')
            # To Document Obj
            if doc.get('dir_name') != dir_name:
                log.info(
                    f'Update At dir_name: {doc.get("dir_name")}, {dir_name}')
                doc['dir_name'] = dir_name
                update = True

            if doc.get('parent') != parent:
                log.info(f'Update At parent: {doc.get("parent")} {parent}')
                doc['parent'] = parent
                update = True

            if doc.get('source') != src:
                log.info(f'Update At source: {doc.get("source")} {src}')
                doc['source'] = src
                update = True

            old_title = doc.get('title')
            if old_title != title:
                log.info(f'Update At title: {doc.get("title")} {title}')
                doc['title'] = title
                update = True

            if exists_vids and vid_names:
                if exists_vid_names != vid_names:
                    log.info(
                        f'Update At videos: {exists_vid_names} {vid_names}')
                    doc['videos'] = exists_vids + vids
                    update = True
                else:
                    # log.info(f'No Update At videos: {exists_vid_names}')
                    ...
            elif vid_names:
                log.info(f'Add At videos: {exists_vids} {vid_names} {vids}')
                doc['videos'] = vids
                update = True

            old_sn_code = doc.get('SN')
            if old_sn_code != sn_code:
                log.info(f'Update At SN: {doc.get("sn_code")} {sn_code}')
                doc['SN'] = sn_code
                update = True

            old_tags = doc.get('tags')
            if old_tags:
                old_tags = list(filter(None, old_tags))
                old_tags = list(filter(lambda x: x != '.', old_tags))
                old_tags.sort()
                new_tags = list(filter(None, set(filted_tags + old_tags)))
                new_tags = list(filter(lambda x: x != '.', new_tags))
                new_tags.sort()
                if filted_tags and old_tags != new_tags:
                    log.info(f'Update At Tags: {old_tags} {new_tags}')
                    doc['tags'] = new_tags
                    update = True
            elif filted_tags:
                log.info(f'Update At Tags: {old_tags} {filted_tags}')
                doc['tags'] = filted_tags
                update = True

            if update:
                doc['snap_date'] = snap_date
                docs.append(doc)
    except KeyboardInterrupt:
        log.info('Manual Interrupt')

    if docs:
        new_docs = []
        update_count = 0
        for ids, d in enumerate(docs):
            ids = d.pop('_id') if '_id' in d else None
            if ids:
                update_count += h.update({'_id': ids}, {'$set': d})
            else:
                new_docs.append(d)
        log.info(f'Update {update_count} documents from {h.default_col}')
        if new_docs:
            inserted_count = h.insert(new_docs)
        else:
            inserted_count = 0
        log.info(f'Insert {inserted_count} documents to {h.default_col}')

    n_docs = h.count_documents({})
    sys_doc = h.query_one({'snap_date': snap_date}, sys=True)
    update_count = 0
    inserted_count = 0
    if sys_doc:
        update_count = h.update({'snap_date': snap_date},
                                {'$set': {'n_videos': n_docs}}, sys=True)
    else:
        inserted_count = h.insert(
            [{'n_videos': n_docs, 'snap_date': snap_date}], sys=True)
    log.info(f'Update {update_count} documents from {h.default_sys_col}')
    log.info(f'Insert {inserted_count} documents to {h.default_sys_col}')

    log.info(f'Finished AV Time Cost: {datetime.now() - st}')
