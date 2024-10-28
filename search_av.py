import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from handlers.mongo import MongoHandler
from models.base import History, MongoDoc
from utils.mongo_op import search_string_to_mongodb_pipeline

if __name__ == '__main__':
    st = datetime.now()
    load_dotenv()
    h = MongoHandler()
    h.default_col = 'AVB_VIDEOS'  # 'AVB_VIDEOS_CLEANUP'
    h.default_sys_col = 'AVB_SYS'
    search = None
    docs = list(
        h.aggregate([{'$match': {'doc_type': 'query_history'}},
                     {'$sort': {'search_datetime': -1}},]))
    history_docs = [History.model_validate(his) for his in docs]
    query_list = [doc.query for doc in history_docs]

    if len(sys.argv) > 1:
        search = sys.argv[1]
    else:
        print('Search History:')
        for idx, doc in enumerate(history_docs):
            print(
                f'{f"{idx + 1}.":>3s} {doc.query.ljust(20," "):<20s}\t{doc.search_datetime.strftime("%Y-%m-%d"):<10s}')

        search = input('Search: ')
        if not search:
            print('No Search Query.')
            sys.exit(0)

        if search.isdigit():
            search = history_docs[int(search) - 1].query

    if search in ['|', ',', '&']:
        print('Invalid Search Query.')
        sys.exit(0)
    if search not in query_list:
        print('Add Search Query to History.')
        h.insert(History(query=search,
                         username='admin').model_dump())
    else:
        print('Search Query Exists in History.')
        h.update_one({'doc_type': 'query_history',
                      'query': search,
                      'username': 'admin'},
                     {'$inc': {'count': 1}})

    print(f'Search Query: {search}')
    search_agg = search_string_to_mongodb_pipeline(search)
    search_agg.update({'doc_type': 'av_info'})
    print('Search Match query: ', search_agg)
    result = list(h.aggregate([{'$match': search_agg},
                               #    {'$project': {'_id': 0}},
                               {'$sort': {'snap_date': 1}},
                               ], show_id=True))

    docs = [MongoDoc.model_validate(doc) for doc in result]
    df = pd.DataFrame(result)
    dir_path = [Path(p) for p in os.getenv('VID_DIR_PATH').split(',')]
    local_docs = []
    tg_channel_docs = []
    for doc in docs:
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
                        if not av_dir_exists or not doc.on_local:
                            if not doc.on_local:
                                tg_channel_docs.append(doc.dir_name[5:])
                            else:
                                print(f'Not Exists: {doc.dir_name}')
                        else:
                            local_docs.append(av_dir_path.as_posix())
        result = h.update_one({'_id': doc.id},
                              {'$set': {'tags': list(set(doc.tags + [search]))}})

    for doc in tg_channel_docs:
        print('On TG Channel: ', doc)
    for doc in local_docs:
        print(f'Start-Process "{doc}"')

    print(f'Finished AV Time Cost: {datetime.now() - st}')
