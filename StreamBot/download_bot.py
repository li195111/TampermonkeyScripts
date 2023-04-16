import glob
import logging
import os
import shutil
import time
from datetime import datetime, timedelta
from typing import List

import pandas as pd

from .downloader import StreamDownloader
from .enums import BotType, FileState, MediaType
from .models import URL, Error, QueueItem, URLs
from .utils import error_msg


class IURLDownloadBot:

  def __init__(self,
               bot_type: BotType,
               src_dir: str,
               dst_dir: str,
               max_queue: int = 5,
               max_threads: int = 3) -> None:
    self.logger = logging.getLogger(__name__)

    self.__type = bot_type
    self.__prefix = f'{self.type.value}_bot_'
    self.__src = src_dir
    self.__dst = dst_dir
    os.makedirs(self.__src, exist_ok=True)
    os.makedirs(self.__dst, exist_ok=True)
    self.queue: List[QueueItem] = []
    self.remove_queue: List[QueueItem] = []
    self.max_queue = max_queue

    self.progress_length = 80
    self.downloader = StreamDownloader(timeout=0.5,
                                       chunk_size=int(1024 * 1024 * 0.5),
                                       progress_length=self.progress_length,
                                       max_connect=3)
    self.file_manager_cols = list(QueueItem.__fields__.keys())
    self.max_threads = max_threads

  @property
  def type(self):
    return self.__type

  @property
  def prefix(self):
    return self.__prefix

  @property
  def src(self):
    return self.__src

  @property
  def dst(self):
    return self.__dst

  @property
  def queue_size(self):
    return len(self.queue)

  @property
  def file_manager(self):
    return pd.DataFrame(self.queue, columns=self.file_manager_cols)

  @property
  def thread_size(self):
    threads = []
    for item in self.queue:
      threads.extend(item.threads)
    return len(threads)

  def queue_infos(self, title: str = ''):
    state_str = f'{title}\n'
    for item in self.queue:
      for t in item.threads:
        if t.status_string:
          state_str += f'{t.status_string}\n'
    state_str += '\33[K'
    self.flush_counts = state_str.count('\n')
    if self.max_flush_counts < self.flush_counts or self.flush_counts == 1:
      self.max_flush_counts = self.flush_counts
    state_str += '\n\33[K' * (self.max_flush_counts - self.flush_counts)
    print(state_str, end=self.flush_end, flush=True)
    return state_str

  @property
  def flush_end(self):
    return '\33[F' * (self.max_flush_counts)

  @property
  def queue_paths(self):
    return [item.file_path for item in self.queue]

  def download_stream(self, url: URL, load_cache: bool = True):
    return self.downloader.download_stream_file(url, load_cache)

  def download(self, url: URL):
    return self.downloader.download_retrieve(url)

  def add_queue(self, item):
    self.queue.append(item)

  def get_queue(self):
    if len(self.queue) > 0:
      return self.queue[-1]

  def log(self, *args, **kwargs):
    self.logger.info(*args, **kwargs)

  def warn(self, *args, **kwargs):
    self.logger.warning(*args, **kwargs)


class URLDownloadBot(IURLDownloadBot):

  def __init__(self,
               bot_type: BotType,
               src_dir: str,
               dst_dir: str,
               max_queue: int = 5,
               max_threads: int = 3) -> None:
    super().__init__(bot_type, src_dir, dst_dir, max_queue, max_threads)
    self.flush_counts = 1
    self.max_flush_counts = 0

  def add_to_queue(self, file_path: str, media_type: MediaType):
    # Add suffix and to queue
    file_name = os.path.basename(file_path)
    queue_file_path = file_path + '.download'
    if os.path.exists(file_path):
      if not os.path.exists(queue_file_path):
        os.rename(file_path, queue_file_path)
      if os.path.exists(file_path):
        # Remove Duplicate
        os.remove(file_path)
      if file_path not in self.queue_paths:
        self.add_queue(
            QueueItem(file_path=queue_file_path,
                      file_name=file_name,
                      media_type=media_type))

  def search_queue_files(self, media_type: MediaType):
    file_name_regex = f'{self.prefix}*_{media_type.value}_*.txt.download'
    regex_string = os.path.join(self.src, file_name_regex)
    file_paths = glob.glob(regex_string)
    return file_paths

  def search_files(self, media_type: MediaType):
    file_name_regex = f'{self.prefix}*_{media_type.value}_*.txt'
    regex_string = os.path.join(self.src, file_name_regex)
    file_paths = glob.glob(regex_string)
    for file_path in file_paths:
      if self.queue_size < self.max_queue:
        # Add to queue
        time.sleep(1)
        self.add_to_queue(file_path, media_type)

  def searching(self):
    for media_type in MediaType:
      self.search_files(media_type)
    return len(self.queue)

  def clean_threads(self, force: bool = False):
    for item in self.queue:
      new_ts = []
      for t in item.threads:
        if not t.is_alive() or t.is_finished or t.is_failed:
          t.join()
        else:
          if force:
            t.is_interrupt = True
          new_ts.append(t)
      item.threads = new_ts

  def process_item(self, item: QueueItem):
    if item.state == FileState.QUEUE and os.path.exists(item.file_path):
      item.urls = URLs.from_file(item.file_path, self.prefix, item.media_type,
                                 self.dst)
      if len(item.urls) == 0:
        self.remove_queue.append(item)
      for url in item.urls:
        if self.thread_size < self.max_threads:
          item.state = FileState.DOWNLOAD
          self.log(f'{url.dir_name[:15]}')
          if self.type == BotType.EYNY:
            media = self.download_stream(url, True)
          elif self.type == BotType.IG:
            media = self.download(url)
          if media.pass_exists:
            self.log(f'Already Exists: {url.dir_name[:15]}')
          else:
            item.threads.append(media)
            time.sleep(0.1)

  def complete_item(self, item: QueueItem):
    # End Process
    item.state = FileState.FINISHED
    dst_path = os.path.join(item.urls.dowloaded_dir, item.file_name)
    if os.path.exists(item.file_path) and not os.path.exists(dst_path):
      file_path = item.file_path
      try:
        shutil.move(file_path, dst_path)
      except FileNotFoundError:
        try:
          os.rename(file_path, dst_path)
        except FileNotFoundError:
          os.remove(file_path)

  def run(self):
    self.log('Start Downloader')
    current_item = None
    st = datetime.now()
    try:
      self.log('Searching ...')

      while self.searching() > 0:

        for current_item in self.queue:
          if current_item.state == FileState.DOWNLOAD or current_item.state == FileState.FINISHED:
            continue
          if not os.path.exists(current_item.file_path):
            self.remove_queue.append(current_item)
            continue
          self.process_item(current_item)

        ct = datetime.now()
        running_secs = (ct - st).seconds
        if running_secs > 0 and running_secs % 30 == 0:
          # Update Threads Log
          info_str = f'\33[KThreads: {self.thread_size}, Queues: {self.queue_size}'
          self.queue_infos(info_str)

        for current_item in self.queue:
          if current_item.state == FileState.DOWNLOAD and current_item.is_finished:
            print(end='\n\33[K\33[F')
            self.log(
                f'Download completed..!! {current_item.urls.save_dir_name[:15]}'
            )
            self.complete_item(current_item)

        for current_item in self.remove_queue:
          if os.path.exists(current_item.file_path):
            os.remove(current_item.file_path)
          if current_item in self.queue:
            self.queue.remove(current_item)
        for current_item in self.queue:
          if current_item.state == FileState.FINISHED:
            if os.path.exists(current_item.file_path):
              os.remove(current_item.file_path)
            self.queue.remove(current_item)

        self.clean_threads()

    except Exception as err:
      print(end='\n\33[K\33[F')
      self.warn('Error')
      error = Error(message={"result": error_msg(err)})
      self.warn(error)
      self.log(f'Current Item: {current_item}')
      for item in self.queue:
        for t in item.threads:
          t.is_failed = True
      raise err

    except KeyboardInterrupt:
      print(end='\n\33[K\33[F')
      self.warn('Shutdown Program')
      self.log(f'Current Item: {current_item}')
      for item in self.queue:
        for t in item.threads:
          t.is_interrupt = True

    finally:
      while self.thread_size > 0:
        # Shutdown Threads
        self.clean_threads(force=True)
        info_str = f'\33[KStop Threads & Queues\n\33[KThreads: {self.thread_size}, Queues: {self.queue_size}'
        self.queue_infos(info_str)
        time.sleep(0.1)

      self.log(f'Clean All Queue File include Queue')
      # Clean All Queue File include Queue
      for item in self.queue:
        if os.path.exists(item.file_path):
          file_path = item.file_path
          # remove '.download' suffix
          if item.file_path.endswith('.download'):
            file_path = '.'.join(file_path.split('.')[:-1])
          if not os.path.exists(file_path):
            os.rename(item.file_path, file_path)
          else:
            os.remove(item.file_path)
      self.queue.clear()

      self.log(f'Stop Threads & Queues')
      self.log(f'Threads: {self.thread_size}, Queues: {self.queue_size}')

      self.log(f'Clearn All Queue File exclude Queue')
      # Clearn All Queue File exclude Queue
      for media_type in MediaType:
        for queue_file in self.search_queue_files(media_type):
          if os.path.exists(queue_file):
            # remove '.download' suffix
            file_path = '.'.join(queue_file.split('.')[:-1])
            if os.path.exists(file_path):
              os.remove(file_path)
            os.rename(queue_file, file_path)
    self.log('Finished Program')
