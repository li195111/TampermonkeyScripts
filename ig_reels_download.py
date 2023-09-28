import json
import logging
import os

import requests

from models.ig_reels import InsReels
from models.ig_reels_tray import ReelsTray
from models.ig_user_profile import UserProfile
from models.ig_username import InsUsername
from StreamBot import setup_logger

if __name__ == '__main__':
  log_dir = os.path.join(os.path.dirname(__file__), 'logs')
  setup_logger(__file__, log_dir)
  logger = logging.getLogger(__file__)
  logger.setLevel(logging.DEBUG)
  headers = {
    'Host':'www.instagram.com',
    'Accept':'*/*',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
    'Cookie':'csrftoken=ZrG4Ro5Zj0ANxxFHDxvppNuoRwfQ33TG; mid=ZGx-UAALAAGSkfJX_Cy6x_5-U6bW; ig_did=ADD2C94D-59D5-47ED-8096-D3F73EE265E0; ig_nrcb=1; datr=T35sZByHaOXF9DFvw59cmhFK; ds_user_id=38513711810; sessionid=38513711810%3AO1KzZZMVbRj2By%3A24%3AAYeNTAymjA_iVIeByL3c9e2_Hy-fkTksBO4TkYEyR8se; shbid="853\05438513711810\0541727163657:01f76cbd6ccf74cadf1bb30aa5914af44e8f21ece78890edffa9f861b7e9ff575aa10e82"; shbts="1695627657\05438513711810\0541727163657:01f797be338d12a2f482270c30cc7497994e26c17b8d7260490732838ae54a5168fc54f8"; rur="CCO\05438513711810\0541727398178:01f7ca032c3284110720a06d59f4f95e2ea85e1d7c2f18b659171fd17290acc6046febef"',
    'X-CSRFToken':'ZrG4Ro5Zj0ANxxFHDxvppNuoRwfQ33TG',
    'X-IG-App-ID':'936619743392459',
    'X-ASBD-ID':'129477',
    'X-IG-WWW-Claim':'hmac.AR0fc_YLexJMTnYtt-Fy-06eg0CJtO2eeIodEO1YwMhvh46S',
    'X-Requested-With':'XMLHttpRequest',
    'DNT':'1',
    'Alt-Used': 'www.instagram.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'TE':'trailers',
  }

  user_name = 'joanne_722'

  # Get User Profile
  # parse data.user.id to get <user_id>
  user_profile_url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={user_name}'
  # parse tag <script type="application/json" data-content-len="154021" data-sjs> to get <user_id> lower case
  ig_user_url = f'https://www.instagram.com/{user_name}/'
  temp_file = 'ig_profile_test.json'
  url = user_profile_url
  if not os.path.exists(temp_file):
    resp = requests.get(url, headers=headers)
    logger.info('Parse State: %s', resp.status_code)
    with open(temp_file, 'w', encoding='utf-8') as fp:
      payload = resp.json()
      fp.write(json.dumps(payload,indent=2))
  else:
    with open(temp_file, 'r', encoding='utf-8') as fp:
      payload = json.loads(fp.read())
  userprofile = UserProfile(**payload)
  user_id = str(userprofile.data.user.id)
  logger.info('User: %s', userprofile.data.user.full_name)
  logger.info('User ID: %s', user_id)

  # Get Username Payload
  ig_username_payload_url = f'https://www.instagram.com/api/v1/feed/user/{user_name}/username/?count=12'
  temp_file = 'ig_username_payload_test.json'
  url = ig_username_payload_url
  if not os.path.exists(temp_file):
    resp = requests.get(url, headers=headers)
    logger.info('Parse State: %s', resp.status_code)
    with open(temp_file, 'w', encoding='utf-8') as fp:
      payload = resp.json()
      fp.write(json.dumps(payload,indent=2))
  else:
    with open(temp_file, 'r', encoding='utf-8') as fp:
      payload = json.loads(fp.read())
  ins_username = InsUsername(**payload)
  for item in ins_username.items:
    logger.info('User Location: %s', item.location)

  # Get Reels Tray Payload
  # 取得 Reels 資料 get story id 
  ig_reels_tray_url = f'https://www.instagram.com/api/v1/feed/reels_tray/?is_following_feed=true'
  temp_file = 'ig_reels_tray_payload_following_test.json'
  url = ig_reels_tray_url
  if not os.path.exists(temp_file):
    resp = requests.get(url, headers=headers)
    logger.info('Parse State: %s', resp.status_code)
    with open(temp_file, 'w', encoding='utf-8') as fp:
      payload = resp.json()
      fp.write(json.dumps(payload,indent=2))
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
    temp_file = 'ig_media_payload.json'
    url = ig_media_url
    if not os.path.exists(temp_file):
      resp = requests.get(url, headers=headers)
      logger.info('Parse State: %s', resp.status_code)
      with open(temp_file, 'w', encoding='utf-8') as fp:
        payload = resp.json()
        fp.write(json.dumps(payload,indent=2))
    else:
      with open(temp_file, 'r', encoding='utf-8') as fp:
        payload = json.loads(fp.read())
    insta_reels = InsReels(**payload)
    for idx, item in enumerate(insta_reels.reels_media[0].items):
      logger.info('%s Image: %s', idx, item.image_versions2.candidates[0].url)
      if item.video_versions is not None:
        logger.info('%s Video: %s', idx, item.video_versions[0].url)
