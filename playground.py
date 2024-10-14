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
