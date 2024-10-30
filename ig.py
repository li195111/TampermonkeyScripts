import os
from datetime import datetime, time
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from tqdm import tqdm

from handlers.mongo import MongoHandler
from models.logger import logger
from utils import get_image_infos, get_video_infos

if __name__ == '__main__':
    st = datetime.now()
    log = logger(name='IG')
    load_dotenv()
    h = MongoHandler()
    h.default_col = 'IGB_IMAGES'
    h.default_sys_col = 'IGB_SYS'

    dir_path = [Path(p) for p in os.getenv('IG_DIR_PATH').split(',')]
    ig_users: List[Path] = []
    for dp in dir_path:
        log.info(f'Dir Path: {dp.exists()}, {dp}')
        ig_users.extend(list(dp.glob('*')))
    snap_date = datetime.combine(datetime.today(), time.min)

    docs = []
    media_types = ['*']
    for p in tqdm(ig_users, desc='IG User Progress'):
        update = False
        dir_name = p.name
        parent = p.parent.name

        name_split = p.name.split('_')
        src = name_split[0]
        title = '_'.join(name_split[1:])

        for t in media_types:
            fs = list(p.glob(f'*.{t}'))
            for f in tqdm(fs, desc='IG User Medias', leave=False):
                fname = f.stem
                ftype = f.suffix
                if ftype.lower() not in ['.jpg', '.jpeg', '.png', '.mp4']:
                    continue

                # Check Exists
                doc = h.query_one({'dir_name': dir_name,
                                   'parent': parent,
                                   'title': title,
                                   'name': fname,
                                   'type': ftype}) or {}
                old_docs = list(h.query({'dir_name': dir_name,
                                         'title': title,
                                         'name': fname,
                                         'type': ftype})) or []
                if len(old_docs) == 1:
                    old_doc = old_docs[0]
                else:
                    old_doc = {}
                if doc.get('width') and doc.get('height') and doc.get('size'):
                    media_infos = {'width': doc.get('width'), 'height': doc.get(
                        'height'), 'size': doc.get('size')}
                elif old_doc.get('width') and old_doc.get('height') and old_doc.get('size'):
                    media_infos = {'width': old_doc.get('width'), 'height': old_doc.get(
                        'height'), 'size': old_doc.get('size')}
                else:
                    media_infos = {}
                if len(media_infos) == 0:
                    fp = f.as_posix()
                    try:
                        if ftype in ['.mp4']:
                            media_infos = get_video_infos(fp)
                        else:
                            media_infos = get_image_infos(fp)
                    except Exception as err:
                        log.info(err)
                    media_infos['size'] = os.path.getsize(fp)

                # To Document Obj
                if doc.get('dir_name') != dir_name:
                    log.info(
                        f'Update At dir_name: {doc.get("dir_name")} {dir_name}')
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

                old_name = doc.get('name')
                if old_name != fname:
                    log.info(f'Update At name: {doc.get("name")}, {fname}')
                    doc['name'] = fname
                    update = True

                old_type = doc.get('type')
                if old_type != ftype:
                    log.info(f'Update At type: {doc.get("type")} {ftype}')
                    doc['type'] = ftype
                    update = True

                old_width = doc.get('width')
                if old_width != media_infos.get('width'):
                    log.info(
                        f'Update At width: {doc.get("width")} {media_infos.get("width")}')
                    doc['width'] = media_infos.get('width')
                    update = True

                old_height = doc.get('height')
                if old_height != media_infos.get('height'):
                    log.info(
                        f'Update At height: {doc.get("height")} {media_infos.get("height")}')
                    doc['height'] = media_infos.get('height')
                    update = True

                old_size = doc.get('size')
                if old_size != media_infos.get('size'):
                    log.info(
                        f'Update At size: {doc.get("size")} {media_infos.get("size")}')
                    doc['size'] = media_infos.get('size')
                    update = True

                if update:
                    doc['snap_date'] = snap_date
                    docs.append(doc)

    if docs:
        new_docs = []
        update_count = 0
        inserted_count = 0
        for ids, d in enumerate(docs):
            ids = d.pop('_id') if '_id' in d else None
            if ids:
                update_count += h.update({'_id': ids}, {'$set': d})
            else:
                new_docs.append(d)
        log.info(f'Update {update_count} documents from {h.default_col}')
        if new_docs:
            inserted_count = h.insert(new_docs)
        log.info(f'Insert {inserted_count} documents to {h.default_col}')

    n_docs = h.count_documents({})
    sys_doc = h.query_one({'snap_date': snap_date}, sys=True)
    update_count = 0
    inserted_count = 0
    if sys_doc:
        update_count = h.update({'snap_date': snap_date},
                                {'$set': {'n_ig_medias': n_docs}}, sys=True)
    else:
        inserted_count = h.insert(
            [{'n_videos': n_docs, 'snap_date': snap_date}], sys=True)
    log.info(f'Update {update_count} documents from {h.default_sys_col}')
    log.info(f'Insert {inserted_count} documents to {h.default_sys_col}')

    log.info(f'Finished IG Time Cost: {datetime.now() - st}')
