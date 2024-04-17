import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union
from urllib.request import urlretrieve

import requests

from .models import URL, Error, IMedia, IStream, Log
from .utils import error_msg


class Stream(IStream):

    def __init__(self,
                 url: URL,
                 max_connect: int = 3,
                 chunk_size: int = int(1024 * 1024 * 0.5),
                 progress_length: int = 80,
                 timeout: float = 0.5,
                 is_load_cache: bool = True,
                 *args,
                 **kwargs) -> None:
        super().__init__(url, max_connect, *args, **kwargs)
        self.chunk_size = chunk_size
        self.progress_length = progress_length
        self.timeout = timeout
        self.is_load_cache = is_load_cache
        self.start_time: Union[datetime, None] = None
        self.status_string = ''

    def get_headers(self, user_name: str):
        proj_dir = Path(__file__).parent.parent
        headers_folder_path = proj_dir.joinpath('headers')
        with open(headers_folder_path.joinpath(f'{user_name}.json'),
                  'r',
                  encoding='utf-8') as hfp:
            header_data = json.load(hfp)
        headers = {
            'Host': 'video.eyny.com',
            'Accept': '*/*',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
            'DNT': '1',
            'Alt-Used': 'video.eyny.com',
            'Connection': 'keep-alive',
            **header_data
        }
        return headers

    def connect(self, url: str, timeout: Optional[float] = None):
        if self.start_time is None:
            self.start_time = datetime.now()
        start_time_str = self.start_time.strftime('%m/%d %H:%M:%S')

        header = {}  # self.get_headers('as852852sa')
        header.update({
            'Referer': url,
            'Range': f'bytes={self.size}-',
        })

        with requests.get(
                url,
                stream=True,
                headers=header,
                timeout=timeout if not timeout is None else self.timeout) as resp:

            content_length = resp.headers.get('Content-Length', 0)
            self.total_size = self.size + int(content_length)
            if self.total_size == 0:
                print(f'No Size Received')
                return
            if content_length == 0:
                print('No Content Received')
                return
            resp.raise_for_status()
            for received_data_chunk in resp.iter_content(self.chunk_size):
                if self.is_interrupt:
                    raise KeyboardInterrupt
                self.data_bytes += received_data_chunk

                curr_time = datetime.now()
                curr_time_str = curr_time.strftime('%m/%d %H:%M:%S')

                time_delta = (curr_time -
                              self.start_time) + timedelta(milliseconds=0.1)
                speed_ratio = self.datas_numb / time_delta.total_seconds()

                pct_len = 7
                pct_str = f"{self.percentage:02.2f}%"
                pct_str = f'{pct_str}{" " * (pct_len - len(pct_str))}'
                ratio_str = f"{self.size/(1024**(int(self.total_level)+1)):03.2f}/{self.total_numb:03.2f} {self.total_level.name}"
                speed_str = f"{speed_ratio:02.2f} {self.datas_level.name}/s"

                status_string = f"{start_time_str:15s} {pct_str:7s} {ratio_str:10s} {speed_str:10s} {curr_time_str:15s} {self.url.dir_name[5:20]:15}"
                num_pad = self.progress_length - len(status_string)
                pad_str = " " * num_pad
                self.status_string = status_string + pad_str
                if self.save_remainder == 0:
                    self.save()
            if self.status_string == '':
                status_string = f'{resp.status_code} {resp.url}'
                num_pad = self.progress_length - len(status_string)
                pad_str = " " * num_pad
                self.status_string = status_string + pad_str

    def run(self):
        if self.is_load_cache and not self.url.file_path is None and os.path.exists(
                self.url.file_path):
            self.load()
        else:
            # Create New Empty File
            self.save()
        if not self.pass_exists:
            timeout = 60 * 0 + self.timeout
            while self.no_stop:
                try:
                    self.connect(self.url.url, timeout)
                    if self.is_failed and not self.is_leave:
                        self.logger.info(
                            f'Connecting {self.url.save_file_name} ...')
                    if self.is_finished:
                        self.complete()
                        self.save()
                except TimeoutError as err:
                    msg = f"TimeoutError: {err.args[0]}"
                    self.logger.warning(msg)
                    error = Error(message={"result": error_msg(err)})
                    self.logger.warning(error)
                except requests.ConnectionError as err:
                    pass
                except requests.HTTPError as err:
                    if str(err.args[0])[:3] == '410':
                        # URL Gone
                        self.connect_count = self.max_connect
                        # Remove Expired File
                        self.logger.warning(
                            f'URL Expired: {self.url.dir_name}')
                        # os.remove(self.url.file_path)
                        self.failed()
                    elif str(err.args[0])[:3] == '416':
                        # Complete
                        self.total_size = self.size
                        self.logger.warning(f'Complete: {self.url.file_dir}')
                        self.complete()
                    else:
                        error = Error(message={"result": error_msg(err)})
                        self.logger.warning(error)
                except requests.Timeout as err:
                    pass
                except KeyboardInterrupt:
                    msg = "Interrupt"
                    self.logger.warning(msg)
                    self.interrupt()
                    self.save()
                except requests.exceptions.ChunkedEncodingError as err:
                    self.logger.warning(
                        f"ChunkedEncodingError: {self.url.dir_name} {err.args}")
                    self.failed()
                except Exception as err:
                    self.logger.warning(
                        f"Failed: {self.url.dir_name} {err.args}")
                    error = Error(message={"result": error_msg(err)})
                    self.logger.warning(error)
                    self.failed()
                    self.connect_count += 1
                finally:
                    self.cache_info.total = self.tota_size
                    self.cache_info.size = self.size
                    self.save_cache()
                    time.sleep(0.01)


class Media(IMedia):

    def run(self) -> None:
        if not self.pass_exists:
            os.makedirs(self.url.file_dir, exist_ok=True)
            try:
                urlretrieve(self.url.url, self.url.file_path)
                time.sleep(0.5)
                self.complete()
            except Exception as err:
                error = Error(message={"result": error_msg(err)})
                self.logger.info(error)


class StreamDownloader(Log):

    def __init__(self,
                 timeout: float = 0.5,
                 chunk_size: int = int(1024 * 1024 * 0.5),
                 progress_length: int = 80,
                 max_connect: int = 3,
                 *args,
                 **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.timeout = timeout
        self.chunk_size = chunk_size
        self.progress_length = progress_length
        self.max_connect = max_connect
        self.is_interrupt = False

    def download_stream_file(self, url: URL, load_cache: bool = True):
        self.media = Stream(url, 3, self.chunk_size, self.progress_length, self.timeout,
                            load_cache, logger=self.logger)
        self.media.start()
        return self.media

    def download_retrieve(self, url: URL):
        self.media = Media(url, logger=self.logger)
        self.media.start()
        return self.media
