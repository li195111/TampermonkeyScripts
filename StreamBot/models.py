from __future__ import annotations

import copy
import logging
import os
import sys
import threading
from typing import List, Optional, Union
from urllib.parse import urlparse

import pydantic

from .enums import FileSizeLevel, FileState, MediaType
from .utils import count_bytes_level


class IBase(pydantic.BaseModel):
  pass


class ErrorMsg(IBase):
  result: str

  def __repr__(self) -> str:
    return self.result


class Error(IBase):
  message: ErrorMsg

  def __repr__(self) -> str:
    return self.message


class CacheInfo(IBase):
  file_name: str
  url: Optional[str]
  total: int = 0
  size: int = 0


class URL(object):

  def __init__(self, url: str, save_dir: str = '.') -> None:
    self.__url = url
    self.__parsed_result = urlparse(self.__url)
    self.__save_dir = os.path.abspath(save_dir)

  def __str__(self):
    return self.__url

  @property
  def url(self):
    return self.__url

  @property
  def path(self):
    return self.__parsed_result.path

  @property
  def save_file_name(self):
    return os.path.split(self.path)[-1]

  @property
  def file_path(self):
    return os.path.join(self.__save_dir, self.save_file_name)

  @property
  def file_dir(self):
    return self.__save_dir

  @property
  def dir_name(self):
    return os.path.basename(self.__save_dir)


class IURLs(object):

  def __init__(self,
               prefix: str,
               media_name: str,
               media_type: MediaType,
               urls: Union[str, List[str]],
               dst_dir: str = '.') -> None:
    self.logger = logging.getLogger(__name__)
    self.__prefix = prefix
    self.__media_name = media_name
    self.__media_type = media_type
    if isinstance(urls, str):
      if '\r\n' in urls:
        urls = urls.split('\r\n')
      elif '\n' in urls:
        urls = urls.split('\n')
      elif ',' in urls:
        urls = urls.split(',')
      elif ';' in urls:
        urls = urls.split(';')
      else:
        urls = urls.split()
    elif isinstance(urls, list):
      urls = urls
    else:
      raise ValueError('Input urls must be {} or {}'.format(
          type(str), type(list)))
    __urls = urls.split() if isinstance(urls, str) else urls
    self.__dst_dir = os.path.abspath(dst_dir)
    self.urls = [URL(url, self.save_dir) for url in __urls]
    try:
      os.makedirs(self.dowloaded_dir, exist_ok=True)
    except FileNotFoundError:
      self.logger.info(f'Not Found Dir: {self.dowloaded_dir}')

    self.__index = 0

  @property
  def prefix(self):
    return self.__prefix

  @property
  def media_name(self):
    return self.__media_name

  @property
  def media_type(self):
    return self.__media_type

  @property
  def save_dir_name(self):
    dir_prefix = self.prefix.replace('bot_', '')
    return f'{dir_prefix}{self.media_name}'.strip()

  @property
  def dst_dir(self):
    return self.__dst_dir

  @dst_dir.setter
  def dst_dir(self, value: str):
    self.__dst_dir = os.path.abspath(value)
    os.makedirs(self.save_dir, exist_ok=True)

  @property
  def save_dir(self):
    return os.path.join(self.__dst_dir, self.save_dir_name)

  @property
  def dowloaded_dir(self):
    return os.path.join(self.save_dir, 'downloaded')

  def __len__(self):
    return len(self.urls)

  def __iter__(self):
    return self

  def __next__(self):
    if self.__index < len(self.urls):
      result = self.urls[self.__index]
      self.__index += 1
      return result
    raise StopIteration

  @classmethod
  def from_file(cls,
                file_path: str,
                prefix: str,
                media_type: MediaType,
                dst_dir='.'):
    # Get Media Infos
    # Eyny: 'eyny_bot_[繁體中文]_[合集] [AT-X] [無修正] [無刪減]_20221014_vid_ee9686596d9b57d26ccfa227f590fca9.mp4.txt'
    # IG: 'ig_bot_wendy__624_20221014_imgs_p_Carl3ODPoKK.txt'
    doc_file_name = os.path.basename(file_path)
    # Eyny: '[繁體中文]_[合集] [AT-X] [無修正] [無刪減]_20221014_vid_ee9686596d9b57d26ccfa227f590fca9.mp4.txt'
    # IG: 'wendy__624_20221014_imgs_p_Carl3ODPoKK.txt'
    doc_file_name = doc_file_name.replace(prefix, '')
    # Eyny: ['[繁體中文]_[合集] [AT-X] [無修正] [無刪減]_20221014', 'ee9686596d9b57d26ccfa227f590fca9.mp4.txt']
    # IG: ['wendy__624_20221014','p_Carl3ODPoKK.txt']
    media_type_split = doc_file_name.split(f'_{media_type.value}_')
    # Eyny: ['[繁體中文]','[合集] [AT-X] [無修正] [無刪減]','20221014']
    # IG: ['wendy','','','624','20221014']
    media_time_split = media_type_split[0].split('_')
    # Eyny: '[繁體中文]_[合集] [AT-X] [無修正] [無刪減]'
    # IG: 'wendy__624'
    media_name = '_'.join(media_time_split[:-1])
    # if media_type == MediaType.VID or media_type == MediaType.VIDS:
    #   media_name = media_name.replace('.', '')
    # Eyny: '20221014'
    # IG: '20221014'
    # download_time_str = media_time_split[-1]
    # download_time = datetime.strptime(download_time_str, '%Y%m%d')

    # Get Url datas
    with open(file_path, 'r', encoding='utf-8') as fp:
      urls = fp.read()

    return cls(prefix, media_name, media_type, urls, dst_dir)


class URLs(IURLs):

  def __init__(self,
               prefix: str,
               media_name: str,
               media_type: MediaType,
               urls: Union[str, List[str]],
               dst_dir: str = '.') -> None:
    super().__init__(prefix, media_name, media_type, urls, dst_dir)

  @classmethod
  def from_file(cls,
                file_path: str,
                bot_prefix: str,
                media_type: MediaType,
                dst_dir: str = '.') -> URLs:
    return super().from_file(file_path, bot_prefix, media_type, dst_dir)


class IStream(threading.Thread):

  def __init__(self, url: URL, max_connect: int = 3, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.logger = logging.getLogger(__name__)
    self.__datas = bytearray(bytes(0))
    self.__datas_numb, self.__datas_level = count_bytes_level(self.size)
    self.__total_size = 0
    self.__total_numb, self.__total_level = count_bytes_level(
        self.__total_size)
    self.url = url
    self.cache_path = os.path.join(
        self.url.file_dir, f'{self.url.save_file_name}.cache.download')
    if not self.cache_path is None and os.path.exists(self.cache_path):
      self.load_cache()
    else:
      self.__cache_info = CacheInfo(file_name=self.url.save_file_name,
                                    url=self.url.url)

    self.save_cache()

    UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0'
    UA_APPLE = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'
    self.base_header = {
        'User-Agent': UA_APPLE if sys.platform == 'darwin' else UA
    }

    self.is_failed = False
    self.is_leave = False
    self.is_interrupt = False
    self.size_thresh_level = 1024.0**(int(FileSizeLevel.MB) + 1)
    self.size_thresh = 10
    self.max_connect = max_connect
    self.connect_count = 0

  def __len__(self):
    return len(self.__datas)

  @property
  def tota_size(self):
    return self.__total_size

  @tota_size.setter
  def total_size(self, value: int):
    self.__total_size = value
    self.__total_numb, self.__total_level = count_bytes_level(self.tota_size)

  @property
  def total_numb(self):
    return self.__total_numb

  @property
  def total_level(self):
    return self.__total_level

  @property
  def data_bytes(self):
    return bytes(self.__datas)

  @property
  def size(self):
    return len(self.__datas)

  @data_bytes.setter
  def data_bytes(self, value: bytearray):
    self.__datas = value
    self.__datas_numb, self.__datas_level = count_bytes_level(self.size)

  @property
  def datas_numb(self):
    return self.__datas_numb

  @property
  def datas_level(self):
    return self.__datas_level

  @property
  def percentage(self):
    return self.size * 100 / self.total_size

  @property
  def cache_info(self):
    return self.__cache_info

  @cache_info.setter
  def cache_info(self, value: CacheInfo):
    self.__cache_info = value
    self.total_size = self.__cache_info.total

  @property
  def is_finished(self):
    return self.size >= self.tota_size and self.tota_size != 0 and self.size != 0

  @property
  def cache_exists(self):
    return os.path.exists(self.cache_path)

  @property
  def pass_exists(self):
    if self.cache_exists:
      self.load_cache()
      pass_exists = self.cache_info.size >= self.cache_info.total and self.cache_info.total != 0
      if self.cache_path.endswith('cache') and not pass_exists:
        old_cache_path = copy.copy(self.cache_path)
        self.cache_path += '.download'
        self.save_cache()
        if os.path.exists(old_cache_path):
          os.remove(old_cache_path)
      self.is_leave = pass_exists
      if pass_exists:
        self.complete()
      return pass_exists
    return False

  @property
  def save_remainder(self):
    size_divisor = self.size // self.size_thresh_level
    return int(size_divisor % self.size_thresh)

  @property
  def no_stop(self):
    return not self.is_finished and not self.is_leave\
           and self.connect_count < self.max_connect\
           and not self.is_interrupt and not self.pass_exists

  def save_bytes(self, file_path: str, data: Union[bytearray, bytes]):
    with open(file_path, 'wb') as f:
      f.write(data)

  def save(self):
    os.makedirs(self.url.file_dir, exist_ok=True)
    self.save_bytes(self.url.file_path, self.data_bytes)

  def load(self):
    with open(self.url.file_path, 'rb') as fp:
      self.data_bytes = bytearray(fp.read())

  def save_cache(self):
    os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
    with open(self.cache_path, 'wb') as fp:
      json_str = self.cache_info.json().encode('utf-8')
      fp.write(json_str)

  def load_cache(self):
    cache_name = os.path.basename(self.cache_path)
    if not cache_name.endswith('.cache'):
      complete_cache_name = '.'.join(cache_name.split('.')[:-1])
    else:
      complete_cache_name = cache_name
    complete_cache_path = os.path.join(self.url.file_dir, complete_cache_name)
    if os.path.exists(complete_cache_path):
      new_cache_info = CacheInfo.parse_file(complete_cache_path)
      if os.path.exists(self.cache_path):
        old_cache_info = CacheInfo.parse_file(self.cache_path)
        new_cache_info.total = old_cache_info.total
        new_cache_info.size = old_cache_info.size
      self.cache_path = complete_cache_path
      self.cache_info = new_cache_info
      if cache_name.endswith('.cache'):
        incomplete_cache_name = cache_name + '.download'
        incomplete_cache_path = os.path.join(self.url.file_dir,
                                             incomplete_cache_name)
        if os.path.exists(incomplete_cache_path):
          os.remove(incomplete_cache_path)
    else:
      self.cache_info = CacheInfo.parse_file(self.cache_path)

  def failed(self):
    self.is_failed = True

  def complete(self):
    self.is_leave = True
    cache_name = os.path.basename(self.cache_path)
    if not cache_name.endswith('.cache'):
      complete_cache_name = '.'.join(cache_name.split('.')[:-1])
    else:
      complete_cache_name = cache_name
    complete_cache_path = os.path.join(self.url.file_dir, complete_cache_name)
    os.rename(self.cache_path, complete_cache_path)
    if complete_cache_name.endswith('.cache'):
      incomplete_cache_name = complete_cache_name + '.download'
      incomplete_cache_path = os.path.join(self.url.file_dir,
                                           incomplete_cache_name)
      if os.path.exists(incomplete_cache_path):
        os.remove(incomplete_cache_path)

  def interrupt(self):
    self.is_failed = True
    self.is_leave = True
    self.is_interrupt = True


class IMedia(threading.Thread):

  def __init__(self, url: URL, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.logger = logging.getLogger(__name__)
    self.url = url
    self.is_finished = False
    self.is_failed = False
    self.is_leave = False
    self.is_interrupt = False
    self.status_string = ''

  @property
  def pass_exists(self):
    return os.path.exists(self.url.file_path)

  def complete(self):
    self.is_finished = True


class QueueItem(IBase):
  file_path: str
  file_name: str
  media_type: MediaType
  urls: Optional[URLs]
  threads: List[threading.Thread] = []
  state: Union[FileState, int] = FileState.QUEUE

  class Config:
    arbitrary_types_allowed = True

  @property
  def is_finished(self):
    finish = True
    for t in self.threads:
      finish = finish and not t.is_alive()
    return finish