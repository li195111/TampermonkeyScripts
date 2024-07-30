import os
import sys
import uuid
from datetime import datetime
from pathlib import Path

import pandas as pd
import pydantic
from dotenv import load_dotenv
from pydantic import BaseModel

from handlers.mongo import MongoHandler
from utils.mongo_op import search_string_to_mongodb_pipeline


class History(BaseModel):
    '''Query History Document'''
    doc_type: str = 'query_history'
    query: str
    username: str
    history_id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    search_datetime: datetime = pydantic.Field(default_factory=datetime.now)


if __name__ == '__main__':
    st = datetime.now()
    load_dotenv()
    h = MongoHandler()
    h.default_col = 'AVB_VIDEOS'
    h.default_sys_col = 'AVB_SYS'
    search = None
    if len(sys.argv) > 1:
        search = sys.argv[1]
    else:
        histories = list(
            h.query({'doc_type': 'query_history'}, {'query': 1, '_id': 0}))
        histories = list(set([h['query'] for h in histories]))
        print('Search History:')
        for idx, history in enumerate(histories):
            print(f'{idx + 1}. {history}')
        search = input('Search: ')
        if not search:
            print('No Search Query.')
            sys.exit(0)
        if search.isdigit():
            search = histories[int(search) - 1]
    if search in ['|', ',', '&']:
        print('Invalid Search Query.')
        sys.exit(0)
    h.insert(History(query=search, username='admin').dict())

    search_agg = search_string_to_mongodb_pipeline(search)
    print('Search Match query: ', search_agg)

    agg = [{'$match': search_agg},
           {'$project': {'_id': 0}},
           {'$sort': {'snap_date': 1}},
           ]
    result = list(h.aggregate(agg))
    df = pd.DataFrame(result)
    dir_path = [Path(p) for p in os.getenv('VID_DIR_PATH').split(',')]

    for idx, row in df.iterrows():
        video_dir_path = [d for d in dir_path if d.name == row['parent']]
        if len(video_dir_path) > 0:
            video_dir_path = video_dir_path[0]
        dir_name = row['dir_name']
        if isinstance(row['videos'], list):
            for video in row['videos']:
                if video['type'] == '.mkv':
                    video_name = f"{video['name']}{video['type']}"
                    if video_dir_path:
                        av_dir_path = video_dir_path.joinpath(dir_name)
                        av_dir_exists = av_dir_path.exists()
                        if not av_dir_exists:
                            print(f"Not Exists: {dir_name}")
                        else:
                            print(f'Start-Process "{video_dir_path.joinpath(dir_name)}"')
    print(f'Finished AV Time Cost: {datetime.now() - st}')
