import json
import os
import random
import time
from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests

from models.ig_feed_user import FeedUser
from models.ig_reels import InsReels
from models.ig_reels_tray import ReelsTray
from models.ig_user_profile import UserProfile
from models.logger import logger
from StreamBot import MediaType

'https://scontent.cdninstagram.com/o1/v/t16/f1/m78/E64C45E092150B48564A6127B0DB5494_video_dashinit.mp4?efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uc3RvcnkuYzIuNzIwLmJhc2VsaW5lIn0&_nc_ht=scontent.cdninstagram.com&_nc_cat=102&vs=25792572827000404_598503070&_nc_vs=HBksFQIYUWlnX3hwdl9wbGFjZW1lbnRfcGVybWFuZW50X3YyL0U2NEM0NUUwOTIxNTBCNDg1NjRBNjEyN0IwREI1NDk0X3ZpZGVvX2Rhc2hpbml0Lm1wNBUAAsgBABUCGDpwYXNzdGhyb3VnaF9ldmVyc3RvcmUvR0NQVW9BTDhCTkJoLUVnSUFNa21mdnc3d25ZeGJwUjFBQUFGFQICyAEAKAAYABsBiAd1c2Vfb2lsATEVAAAm8K787qyQtT8VAigCQzMsF0AJU\u00252FfO2RaHGBJkYXNoX2Jhc2VsaW5lXzFfdjERAHXoBwA\u00253D&_nc_rid=35a97dcc8c&ccb=9-4&oh=00_AfCLEbpo8_DE97Gn1giTgg_UNeNQ-WTAKV9BADg2VALErQ&oe=662C0290&_nc_sid=10d13b'
'https://scontent.cdninstagram.com/v/t51.29350-15/440656225_949972736615440_7573897684140411047_n.jpg?stp=dst-jpg_e15&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi42NDB4MTEzNi5zZHIuZjI5MzUwIn0&_nc_ht=scontent.cdninstagram.com&_nc_cat=104&_nc_ohc=xlyrO9MMuNwQ7kNvgHcQb4W&edm=APs17CUBAAAA&ccb=7-5&ig_cache_key=MzM1Mzg3NzY2OTMwMDc1MDM4MQ\u00253D\u00253D.2-ccb7-5&oh=00_AfCjBSvGqrUKj9C3Jfls1hcjWpoCM_Za8fxp9XC9FlR94Q&oe=662BF5AC&_nc_sid=10d13b'

'https://www.instagram.com/stories/freyaachuang/3353877669300750381/' # 302
'https://www.instagram.com/stories/freyaachuang/3353877669300750381/?r=1' # 200

# 2024/06/26 Update
# https://scontent.cdninstagram.com/o1/v/t16/f1/m78/124A27C2C651511BAEEAA04A0360B589_video_dashinit.mp4?efg=eyJ2aWRlb19pZCI6bnVsbCwidmVuY29kZV90YWciOiJpZy14cHZkcy5zdG9yeS5jMi1DMy5kYXNoX2Jhc2VsaW5lXzFfdjEifQ&_nc_ht=scontent.cdninstagram.com&_nc_cat=102&ccb=9-4&oh=00_AYAVHEdfqTIjW8TLGGzPKhkJTCcOQ0j4liO0LtwCVu32ZQ&oe=667D3C7A&_nc_sid=9ca052&bytestart=0
# https://scontent.cdninstagram.com/v/t66.30100-16/46638189_1149217949689833_8365826383080174344_n.mp4?_nc_cat=100&ccb=1-7&_nc_sid=9a5d50&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLnN0b3J5LmMyLUMzLmRhc2hfYmFzZWxpbmVfMTA4MHBfdjEiLCJ2aWRlb19pZCI6bnVsbH0=&_nc_ohc=HQaoAbWip1oQ7kNvgE0EfVo&_nc_ht=scontent.cdninstagram.com&oh=00_AYAD9N_XDspduo4EX5WbkLwGYnONJjxF7llflkL__mtFTQ&oe=668147A3&bytestart=0
# Small Video
# https://scontent.cdninstagram.com/o1/v/t16/f1/m78/5E41B9EA12A6B27DCEB341F4556ECD86_video_dashinit.mp4?efg=eyJ2aWRlb19pZCI6bnVsbCwidmVuY29kZV90YWciOiJpZy14cHZkcy5zdG9yeS5jMi1DMy5kYXNoX2Jhc2VsaW5lXzNfdjEifQ&_nc_ht=scontent.cdninstagram.com&_nc_cat=105&ccb=9-4&oh=00_AYDPELPwsvXtnyK1X-7-ausMqA4oQpTApXj2APUFiQ7Lcg&oe=667D375C&_nc_sid=9ca052&bytestart=0
# Large Video
# https://scontent.cdninstagram.com/o1/v/t16/f1/m78/904687046B5AA97BC75C6CBD67BEA8B2_video_dashinit.mp4?efg=eyJ2aWRlb19pZCI6bnVsbCwidmVuY29kZV90YWciOiJpZy14cHZkcy5zdG9yeS5jMi1DMy5kYXNoX2Jhc2VsaW5lXzFfdjEifQ&_nc_ht=scontent.cdninstagram.com&_nc_cat=111&ccb=9-4&oh=00_AYAmo3Rf06x6vYUI7kqNRS64IW1hH38VaSfz2xvGM1m05A&oe=667D5C4F&_nc_sid=9ca052&bytestart=0

def parse_reels(user_name: str, headers):
    file_path = Path(__file__)
    proj_dir = file_path.parent
    os.environ['LOG_DIR'] = proj_dir.joinpath('logs').as_posix()
    log = logger(name='ReelsDLR', log_filename='ReelsDLR.log', level=10 if os.getenv("DEBUG") else 20)

    user_profile_dir = Path(os.environ['USERPROFILE'])
    # Get User Profile
    # parse data.user.id to get <user_id>
    user_profile_url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={user_name}'
    # parse tag <script type="application/json" data-content-len="154021" data-sjs> to get <user_id> lower case
    # ig_user_url = f'https://www.instagram.com/{user_name}/'

    timestamp = datetime.now().strftime('%Y%m%dT%H')
    prefix = f'ig_{user_name}_{timestamp}'
    payload_history_dir = proj_dir.joinpath('history', user_name)
    payload_history_dir.mkdir(parents=True, exist_ok=True)
    save_path = user_profile_dir.joinpath('Downloads')
    output_prefix = f'ig_bot_{user_name}_{timestamp}'

    temp_file = payload_history_dir.joinpath(
        f'{prefix}_profile_test.json').as_posix()
    url = user_profile_url
    if not os.path.exists(temp_file):
        resp = requests.get(url, headers=headers)
        log.info('Parse State: %s', resp.status_code)
        with open(temp_file, 'w', encoding='utf-8') as fp:
            payload = resp.json()
            fp.write(json.dumps(payload, indent=2))
    else:
        log.warning(f'Parse Exists: {Path(temp_file).name}')
        with open(temp_file, 'r', encoding='utf-8') as fp:
            payload = json.loads(fp.read())
    userprofile = UserProfile(**payload)
    user_id = str(userprofile.data.user.id)
    log.info('User: %s', userprofile.data.user.full_name)
    log.info('User ID: %s', user_id)

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
        log.info('Parse State: %s', resp.status_code)
        rm_file = False
        with open(temp_file, 'w', encoding='utf-8') as fp:
            try:
                payload = resp.json()
            except Exception as err:
                log.warning('Parse Failed, Please Check Headers')
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
            log.info('ReelsTray ID: %s', tray.id)
            log.info('ReelsTray User: %s', tray.user.full_name)
            log.info('ReelsTray Username: %s', tray.user.username)
            log.info('Media Ids: %s', tray.media_ids)
            if len(tray.media_ids) > 0:
                story_id = tray.media_ids[-1]
                log.info('Lastest Story ID: %s', story_id)
    if story_id is not None:
        ig_stories_url = f'https://www.instagram.com/stories/{user_name}/{story_id}/'
        ig_media_url = f'https://www.instagram.com/api/v1/feed/reels_media/?media_id={story_id}&reel_ids={user_id}'
        temp_file = payload_history_dir.joinpath(
            f'{prefix}_media_payload.json').as_posix()
        url = ig_media_url
        if not os.path.exists(temp_file):
            resp = requests.get(url, headers=headers)
            log.info('Parse State: %s', resp.status_code)
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
            log.info('%s Image: %s', idx, img_name)
            if item.video_versions is not None and len(item.video_versions) > 0:
                vid_url = item.video_versions[0].url
                vid_name = urlparse(vid_url).path.split('/')[-1]
                vid_file_name = f'{output_prefix}_{MediaType.VID.value}_{vid_name}.txt'
                with open(save_path.joinpath(vid_file_name).as_posix(),
                          'w',
                          encoding='utf-8') as vid_fp:
                    vid_fp.write(vid_url)
                log.info('%s Video: %s', idx, vid_name)
    else:
        log.warning('Story ID is None')
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
        log.info('Parse State: %s', resp.status_code)
        with open(temp_file, 'w', encoding='utf-8') as fp:
            payload = resp.json()
            fp.write(json.dumps(payload, indent=2))
    else:
        log.warning(f'Parse Exists: {Path(temp_file).name}')
        with open(temp_file, 'r', encoding='utf-8') as fp:
            payload = json.loads(fp.read())
    feed_user = FeedUser(**payload)
    if feed_user.user is None:
        log.warning(f'No Avaliable User Found: {user_name}')
        return
    for idx, feed in enumerate(feed_user.items):
        img_url = feed.image_versions2.candidates[0].url
        img_name = urlparse(img_url).path.split('/')[-1]
        img_file_name = f'{output_prefix}_{MediaType.IMG.value}_{img_name}.txt'
        img_file = save_path.joinpath(img_file_name)
        if not img_file.exists():
            with open(img_file.as_posix(), 'w', encoding='utf-8') as img_fp:
                img_fp.write(img_url)
        log.info('%s Image: %s', idx, img_name)
        if feed.video_versions is not None:
            vid_url = feed.video_versions[0].url
            vid_name = urlparse(vid_url).path.split('/')[-1]
            vid_file_name = f'{output_prefix}_{MediaType.VID.value}_{vid_name}.txt'
            vid_file = save_path.joinpath(vid_file_name)
            if not vid_file.exists():
                with open(vid_file.as_posix(), 'w', encoding='utf-8') as vid_fp:
                    vid_fp.write(vid_url)
            log.info('%s Video: %s', idx, vid_name)


def get_headers(user_name: str):
    proj_dir = Path(__file__).parent
    headers_folder_path = proj_dir.joinpath('headers')
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


def options():
    parser = ArgumentParser()
    parser.add_argument('--bot', '-b', type=str,
                        default='__j__a.s', help='Bot User')
    parser.add_argument('--user', '-u', type=str, help='User Name')
    return parser.parse_args()


if __name__ == '__main__':
    opts = options()
    bot_user_name = 'li195111'
    bot_user_name = '__j__a.s'

    user_names = [
        #   'freyaachuang',
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
        'akaonikou',
    ]

    headers = get_headers(opts.bot)
    if not opts.user:
        for user_ in user_names:
            parse_reels(user_name=user_, headers=headers)
            time.sleep(random.random() + random.random() + 0.5)
    else:
        parse_reels(user_name=opts.user, headers=headers)
