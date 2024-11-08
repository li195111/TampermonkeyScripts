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
    media_infos = {'width': 0, 'height': 0}
    try:
        cap = cv2.VideoCapture(video_path)
        media_infos['width'] = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        media_infos['height'] = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        cap.release()
        return media_infos
    except Exception:
        return media_infos


def get_image_infos(image_path: str):
    media_infos = {'width': 0, 'height': 0}
    try:
        im = cv2.imread(image_path)
        if im is None:
            return media_infos
        media_infos['height'], media_infos['width'] = im.shape[:2]
        return media_infos
    except Exception:
        return media_infos


def get_image_infos_pil(image_path: str):
    media_infos = {'width': 0, 'height': 0}
    try:
        im: Image.Image = Image.open(image_path)
        media_infos['width'], media_infos['height'] = im.size
        return media_infos
    except Exception:
        return media_infos


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
