import os
from urllib.parse import quote_plus

import cv2
from PIL import Image
from pymongo import MongoClient


def get_collection(db_name: str, col_name: str):
    username = os.getenv('MONGO_USERNAME')
    if not username:
        uri = os.getenv('MONGODB_URI')
    else:
        hosts = os.getenv('MONGO_HOSTS')
        pswd = os.getenv('MONGO_PSWD')
        pswd = quote_plus(f'{pswd}')
        uri = f'mongodb://{username}:{pswd}@{hosts}/'
    client = MongoClient(uri)
    return client.get_database(db_name).get_collection(col_name)


def get_video_infos(video_path: str):
    try:
        cap = cv2.VideoCapture(video_path)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        cap.release()
        return {'width': width, 'height': height}
    except Exception:
        return {'width': 0, 'height': 0}


def get_image_infos(image_path: str):
    im = cv2.imread(image_path)
    if im is None:
        return {'width': 0, 'height': 0}
    height, width = im.shape[:2]
    return {'width': width, 'height': height}


def get_image_infos_pil(image_path: str):
    try:
        im: Image.Image = Image.open(image_path)
        width, height = im.size
        return {'width': width, 'height': height}
    except Exception:
        return {'width': 0, 'height': 0}


def split_tags(ts, results=[]):
    if isinstance(ts, str) and '_' in ts:
        ts = ts.split('_')
    if isinstance(ts, str) and ' ' in ts:
        ts = ts.split(' ')
    if isinstance(ts, list) and len(ts) > 1:
        for st in ts:
            split_tags(st, results)
    else:
        results.extend([ts])
