import json
import logging
import os
import time
import random
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests

from models.ig_feed_user import FeedUser
from models.ig_user_profile import UserProfile
from models.ig_username import InsUsername
from models.ig_reels import InsReels
from models.ig_reels_tray import ReelsTray
from StreamBot import MediaType, setup_logger


def parse_reels(user_name: str, headers):
  logger = logging.getLogger(__file__)
  logger.setLevel(logging.DEBUG)
  # Get User Profile
  # parse data.user.id to get <user_id>
  user_profile_url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={user_name}'
  # parse tag <script type="application/json" data-content-len="154021" data-sjs> to get <user_id> lower case
  # ig_user_url = f'https://www.instagram.com/{user_name}/'

  timestamp = datetime.now().strftime('%Y%m%dT%H')
  prefix = f'ig_{user_name}_{timestamp}'
  payload_history_dir = Path('./history')
  payload_history_dir.mkdir(parents=True, exist_ok=True)
  save_path = Path('C:/Users/LIDESKTOP/Downloads/')
  output_prefix = f'ig_bot_{user_name}_{timestamp}'

  temp_file = payload_history_dir.joinpath(
      f'{prefix}_profile_test.json').as_posix()
  url = user_profile_url
  if not os.path.exists(temp_file):
    resp = requests.get(url, headers=headers)
    logger.info('Parse State: %s', resp.status_code)
    with open(temp_file, 'w', encoding='utf-8') as fp:
      payload = resp.json()
      fp.write(json.dumps(payload, indent=2))
  else:
    logger.warning(f'Parse Exists: {Path(temp_file).name}')
    with open(temp_file, 'r', encoding='utf-8') as fp:
      payload = json.loads(fp.read())
  userprofile = UserProfile(**payload)
  user_id = str(userprofile.data.user.id)
  logger.info('User: %s', userprofile.data.user.full_name)
  logger.info('User ID: %s', user_id)

  # # Get Username Payload
  # ig_username_payload_url = f'https://www.instagram.com/api/v1/feed/user/{user_name}/username/?count=12'
  # temp_file = payload_history_dir.joinpath(
  #     f'{prefix}_username_payload_test.json').as_posix()
  # url = ig_username_payload_url
  # if not os.path.exists(temp_file):
  #   resp = requests.get(url, headers=headers)
  #   logger.info('Parse State: %s', resp.status_code)
  #   with open(temp_file, 'w', encoding='utf-8') as fp:
  #     payload = resp.json()
  #     fp.write(json.dumps(payload, indent=2))
  # else:
  #   logger.info(f'Parse Exists: {Path(temp_file).name}')
  #   with open(temp_file, 'r', encoding='utf-8') as fp:
  #     payload = json.loads(fp.read())
  # ins_username = InsUsername(**payload)
  # for item in ins_username.items:
  #   logger.info('User Location: %s', item.location)

  # Get Reels Tray Payload
  # 取得 Reels 資料 get story id
  ig_reels_tray_url = f'https://www.instagram.com/api/v1/feed/reels_tray/?is_following_feed=true'
  temp_file = payload_history_dir.joinpath(
      f'{prefix}_reels_tray_payload_following_test.json').as_posix()
  url = ig_reels_tray_url
  if not os.path.exists(temp_file):
    resp = requests.get(url, headers=headers)
    logger.info('Parse State: %s', resp.status_code)
    rm_file = False
    with open(temp_file, 'w', encoding='utf-8') as fp:
      try:
        payload = resp.json()
      except Exception as err:
        logger.warning('Parse Failed, Please Check Headers')
        rm_file = True
      fp.write(json.dumps(payload, indent=2))
    if rm_file:
      os.remove(temp_file)
      exit()
  else:
    with open(temp_file, 'r', encoding='utf-8') as fp:
      payload = json.loads(fp.read())
  reels_tray = ReelsTray(**payload)
  story_id = None
  for tray in reels_tray.tray:
    if tray.id == user_id:
      logger.info('ReelsTray ID: %s', tray.id)
      logger.info('ReelsTray User: %s', tray.user.full_name)
      logger.info('ReelsTray Username: %s', tray.user.username)
      logger.info('Media Ids: %s', tray.media_ids)
      if len(tray.media_ids) > 0:
        story_id = tray.media_ids[-1]
        logger.info('Lastest Story ID: %s', story_id)
  if story_id is not None:
    ig_stories_url = f'https://www.instagram.com/stories/{user_name}/{story_id}/'
    ig_media_url = f'https://www.instagram.com/api/v1/feed/reels_media/?media_id={story_id}&reel_ids={user_id}'
    temp_file = payload_history_dir.joinpath(
        f'{prefix}_media_payload.json').as_posix()
    url = ig_media_url
    if not os.path.exists(temp_file):
      resp = requests.get(url, headers=headers)
      logger.info('Parse State: %s', resp.status_code)
      with open(temp_file, 'w', encoding='utf-8') as fp:
        payload = resp.json()
        fp.write(json.dumps(payload, indent=2))
    else:
      with open(temp_file, 'r', encoding='utf-8') as fp:
        payload = json.loads(fp.read())
    insta_reels = InsReels(**payload)
    for idx, item in enumerate(insta_reels.reels_media[0].items):
      img_url = item.image_versions2.candidates[0].url
      img_name = urlparse(img_url).path.split('/')[-1]
      img_file_name = f'{output_prefix}_{MediaType.IMG.value}_{img_name}.txt'
      with open(save_path.joinpath(img_file_name).as_posix(),
                'w',
                encoding='utf-8') as img_fp:
        img_fp.write(img_url)
      logger.info('%s Image: %s', idx, img_name)
      if item.video_versions is not None and len(item.video_versions) > 0:
        vid_url = item.video_versions[0].url
        vid_name = urlparse(vid_url).path.split('/')[-1]
        vid_file_name = f'{output_prefix}_{MediaType.VID.value}_{vid_name}.txt'
        with open(save_path.joinpath(vid_file_name).as_posix(),
                  'w',
                  encoding='utf-8') as vid_fp:
          vid_fp.write(vid_url)
        logger.info('%s Video: %s', idx, vid_name)
  else:
    logger.warning('Story ID is None')
    # # 精選
    # ig_feed_user_url = f'https://www.instagram.com/api/v1/feed/user/{user_id}/?count=12&max_id={ins_username.next_max_id}'
    # temp_file = payload_history_dir.joinpath(f'{prefix}_{next_max_id}_feed_user_payload.json').as_posix()
    # url = ig_feed_user_url
    # if not os.path.exists(temp_file):
    #   resp = requests.get(url, headers=headers)
    #   logger.info('Parse State: %s', resp.status_code)
    #   with open(temp_file, 'w', encoding='utf-8') as fp:
    #     payload = resp.json()
    #     fp.write(json.dumps(payload,indent=2))
    # else:
    #   with open(temp_file, 'r', encoding='utf-8') as fp:
    #     payload = json.loads(fp.read())
    # print(payload)

  # 限時動態
  ig_feed_user_url = f'https://www.instagram.com/api/v1/feed/user/{user_id}/?count=12'
  temp_file = payload_history_dir.joinpath(
      f'{prefix}_feed_user_payload.json').as_posix()
  url = ig_feed_user_url
  if not Path(temp_file).exists():
    resp = requests.get(url, headers=headers)
    logger.info('Parse State: %s', resp.status_code)
    with open(temp_file, 'w', encoding='utf-8') as fp:
      payload = resp.json()
      fp.write(json.dumps(payload, indent=2))
  else:
    logger.warning(f'Parse Exists: {Path(temp_file).name}')
    with open(temp_file, 'r', encoding='utf-8') as fp:
      payload = json.loads(fp.read())
  feed_user = FeedUser(**payload)
  if feed_user.user is None:
    logger.warning(f'No Avaliable User Found: {user_name}')
    return
  for idx, feed in enumerate(feed_user.items):
    img_url = feed.image_versions2.candidates[0].url
    img_name = urlparse(img_url).path.split('/')[-1]
    img_file_name = f'{output_prefix}_{MediaType.IMG.value}_{img_name}.txt'
    img_file = save_path.joinpath(img_file_name)
    if not img_file.exists():
      with open(img_file.as_posix(), 'w', encoding='utf-8') as img_fp:
        img_fp.write(img_url)
    logger.info('%s Image: %s', idx, img_name)
    if feed.video_versions is not None:
      vid_url = feed.video_versions[0].url
      vid_name = urlparse(vid_url).path.split('/')[-1]
      vid_file_name = f'{output_prefix}_{MediaType.VID.value}_{vid_name}.txt'
      vid_file = save_path.joinpath(vid_file_name)
      if not vid_file.exists():
        with open(vid_file.as_posix(), 'w', encoding='utf-8') as vid_fp:
          vid_fp.write(vid_url)
      logger.info('%s Video: %s', idx, vid_name)


def get_headers(user_name: str):
  headers_folder_path = Path('headers')
  with open(headers_folder_path.joinpath(f'{user_name}.json'),
            'r',
            encoding='utf-8') as hfp:
    header_data = json.load(hfp)
  headers = {
      'Host': 'www.instagram.com',
      'Accept': '*/*',
      'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
      'Accept-Encoding': 'gzip, deflate, br',
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
      'DNT': '1',
      'Alt-Used': 'www.instagram.com',
      'Connection': 'keep-alive',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-origin',
      'TE': 'trailers',
      **header_data
  }
  return headers


if __name__ == '__main__':
  log_dir = os.path.join(os.path.dirname(__file__), 'logs')
  setup_logger(__file__, log_dir)

  bot_user_name = 'li195111'
  bot_user_name = '__j__a.s'

  user_names = [
      'joanne_722',
      'rosso.tw',
      'we_love_mius',
      'fang_cen0130',
      'estherx118',
      'gg_851214',
      '_vickymouse',
      'purple._pov',
      '__t.i.f.f.a.n.y__',
      'hsinyu_c__',
      'hsuan0711',
      'yueh_0720',
      # 'freyaachuang',
      '95_mizuki',
      '1105ya',
      'chuchu.5299',
      'chu.eight',
      '99chu2023',
      'wendy__624',
      'yuchinjou',
      'superlisa821',
      'lovelynnboo',
      'sandy.118',
      'amber_travelholic',
      'lynnwu0219',
      'dodo.ra_h',
      'miaooomm',
      'y.3.1.4',
      'nanaciaociao',
      't40533',
      'vivihsu0317',
      'pyoapple',
      'pinpinponpon627',
      'cawaiiun',
      'sincere_1109',
  ]

  headers = get_headers(bot_user_name)
  for user_ in user_names:
    parse_reels(user_name=user_, headers=headers)
    time.sleep(random.random() + random.random() + 0.5)
