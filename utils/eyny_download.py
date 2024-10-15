import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

from models.base import Error

LEVEL = {0: 'Kb', 1: 'Mb', 2: 'Gb'}


def count_bytes_level(bts):
    numb = bts / 1024
    level = 0
    while numb > 1024 and level < 2:
        numb /= 1024
        level += 1
    return numb, level


def connect(file_name, url, start_bytes, total, chunk_size, data, timeout, st,
            padding):
    header = {
        'Range':
        f'bytes={start_bytes}-',
        'Referer':
        url,
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
        if sys.platform == 'darwin' else
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'
    }
    ts = time.time()
    with requests.get(url, stream=True, headers=header, timeout=timeout) as r:
        total = start_bytes + int(r.headers.get('Content-Length', 0))
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=chunk_size):
            data += chunk
            dsize = len(data)
            te = time.time()
            while te - ts == 0:
                te += 1e-4
            total_numb, total_level = count_bytes_level(total)
            speed_numb, speed_level = count_bytes_level(dsize)

            percentage = f"{dsize * 100 / total:.2f}%"
            percentage_GB = f"{dsize/(1024**(total_level+1)):.2f}/{total_numb:.2f} {LEVEL[total_level]}"
            speed = f"{speed_numb/(te-ts):.2f} {LEVEL[speed_level]}/s"

            update_time = f"{datetime.now().strftime('%m-%d T%H:%M:%S')}"
            status_string = f"{st:20s} Download {file_name} {percentage:7s} {percentage_GB:10s} {speed:15s} {update_time:15s}"
            n_pad = padding - len(status_string)
            pad = " " * n_pad
            print(status_string + pad, end='\r')
    return data, total


def downloader(file_name,
               url,
               start_time,
               data,
               start_bytes=0,
               total=-1,
               chunk_size=10240,
               padding=130,
               timeout_min=0,
               timeout_sec=0.5):
    timeout = 60 * timeout_min + timeout_sec
    while len(data) < total or total == -1:
        try:
            data, total = connect(file_name, url, start_bytes, total, chunk_size,
                                  data, timeout, start_time, padding)
        except requests.HTTPError:
            start_bytes = len(data)
        except requests.Timeout:
            start_bytes = len(data)
        except TimeoutError:
            start_bytes = len(data)
        except requests.ConnectionError:
            start_bytes = len(data)
        except Exception as e:
            err = Error.from_exc('Exception Error: ', e)
            print(err.title)
            print(err.message)
            start_bytes = len(data)
            print(f"\nReconnecting Start Bytes: {start_bytes}")
    return bytes(data), total


def download(cwd: Path,
             nm: str,
             vid_name: str,
             url: str,
             leave=False,
             failed=False):
    vid_name = vid_name.replace('.', '_').replace('-', '_')
    VIDEO_DIR = cwd.joinpath(nm)
    FILES = []
    if VIDEO_DIR.exists():
        FILES = [
            '_'.join(p.name.split('.')[0].split('_')[-2:])
            for p in VIDEO_DIR.glob(r'*[!.txt|!.vscode|!.py]')
        ]
    SN = '_'.join(vid_name.split('_')[-2:])
    OUTPUT = VIDEO_DIR.joinpath(f"{vid_name}.mp4")
    if not SN in FILES:
        finished = False
        connecting = f'Connecting {nm} {SN}'
        connect_wait = ''
        padding = 30
        os.makedirs(VIDEO_DIR, exist_ok=True)
        with open(OUTPUT, 'wb') as f:
            f.write(bytes(0))
        failed = False
        while not finished:
            try:
                downloaded = bytearray()
                st = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                downloaded, total = downloader(f"{nm} {SN}",
                                               url,
                                               start_time=st,
                                               data=downloaded,
                                               start_bytes=0,
                                               total=-1)
                with open(OUTPUT, 'wb') as f:
                    f.write(downloaded)
                finished = True
                failed = False
                leave = True
            except KeyboardInterrupt:
                print(f"\nInterrupted")
                finished = True
                failed = True
                leave = True
                time.sleep(0.01)
            except Exception as e:
                err = Error.from_exc('Exception Error: ', e)
                print(err.title)
                print(err.message)
                failed = True
                if (len(connect_wait) + 1) % 7 == 0:
                    connect_wait = ''
                else:
                    connect_wait += '.'
                n_pad = padding - len(connecting) + len(connect_wait) + 2
                pad = ' ' * n_pad
                print(f'{connecting} {connect_wait+pad}', end='\r', flush=True)
                time.sleep(0.01)
        if failed:
            if OUTPUT.exists():
                os.remove(OUTPUT)
    return leave, failed


def main(opts):
    CUR_DIR = Path(os.path.abspath(opts.cwd))
    if opts.d is None and opts.n is None and opts.url is None:
        with open(opts.q, 'r', encoding='utf-8') as fp:
            datas = fp.read().split('# ')
        leave = False
        failed = False
        while not leave:
            for data in datas:
                if data:
                    ds = data.split()
                    nm = ds[0]
                    video_names = ds[1::2]
                    urls = ds[2::2]
                    for vid_name, url in zip(video_names, urls):
                        leave, failed = download(
                            CUR_DIR, nm, vid_name, url, leave, failed)
                        if leave:
                            break
                if leave:
                    break
            if not failed:
                leave = True
    elif not opts.d is None and not opts.n is None and not opts.url is None:
        download(CUR_DIR, opts.d, opts.n, opts.url)
    else:
        print(
            f"Need '-d' for directory name, '-n' for file name, '-url' for video url."
        )


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d')
    parser.add_argument('-n')
    parser.add_argument('-url')
    parser.add_argument('-cwd', default='.', help='Current Work Directory')
    parser.add_argument('-q', default='query.txt', help='query.txt file path')
    return parser.parse_args()


if __name__ == "__main__":
    main(parse())
    # ffmpeg -err_detect ignore_err -hwaccel_output_format cuda -c:v h264_cuvid -i <input> -c:v h264_nvenc <output>
    # Mpeg4 To HEVC
    # ffmpeg -err_detect ignore_err -hwaccel_output_format cuda -c:v h264_cuvid -i <input> -c:v hevc_nvenc -crf <quality> <output>
