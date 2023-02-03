import os
from datetime import datetime
from pathlib import Path
import shutil
from multiprocessing import Process
from typing import Dict, List, Optional


def folder_size(folder_path: str):
  '''Get Folder Size'''
  if os.path.isdir(folder_path):
    size = 0
    for path, dirs, files in os.walk(folder_path):
      for f in files:
        fp = os.path.join(path, f)
        size += os.path.getsize(fp)
  else:
    raise ValueError(f'"{folder_path}" is not a folder')
  return size


def move_folder(folder_name: str, src_path: Path, dst_path: Path,
                src_size_map: Dict[str, int], dst_size_map: Dict[str, int]):
  src_folder = src_path.joinpath(folder_name)
  dst_folder = dst_path.joinpath(folder_name)
  if dst_folder in dst_size_map:
    if src_size_map[src_folder] > dst_size_map[dst_folder]:
      shutil.copytree(src_folder, dst_folder, dirs_exist_ok=True)
  else:
    shutil.copytree(src_folder, dst_folder, dirs_exist_ok=True)


class MoveProcess(Process):

  def __init__(self, timeout: Optional[int] = None, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.timeout = timeout
    self.start_time = datetime.now()

  @property
  def is_timeout(self):
    return self.timeout is not None and (
        datetime.now() - self.start_time).seconds > self.timeout


def show_size(size: int):
  show = f'{size:.2f} B'
  if size / 1024 > 0:
    show = f'{size / 1024:.2f} KB'
  if size / 1024**2 > 0:
    show = f'{size / 1024**2:.2f} MB'
  if size / 1024**3 > 0:
    show = f'{size / 1024**3:.2f} GB'
  return show


def calc_trans_size(trans_names: List[str], src_path: Path,
                    src_folder_paths_size: Dict[Path, int]):
  ttl_n = len(trans_names)
  # Total Bytes
  ttl_size = sum([
      src_folder_paths_size[src_path.joinpath(folder_name)]
      for folder_name in trans_names
  ])
  show = show_size(ttl_size)
  print(f'移轉 {ttl_n} 個資料夾共: {show}')
  return ttl_size, show, trans_names


def setup_trans_size(inp_txt: str, src_path: Path, src_folder_names: List[str],
                     src_folder_paths_size: Dict[Path, int]):
  trans_size = input(inp_txt)
  trans_size = eval(trans_size)
  trans_names = src_folder_names[:trans_size]
  return calc_trans_size(trans_names, src_path, src_folder_paths_size)


if __name__ == '__main__':
  # TODO: Get File Infos
  # name = 'Instagram'
  name = 'Study'
  src_path = Path(f'F:/{name}')
  dst_path = Path(f'D:/{name}')
  free_size = shutil.disk_usage(dst_path).free

  dst_folders = os.listdir(dst_path)
  dst_folders.sort()

  dst_folder_paths_size: Dict[Path, int] = {}
  dst_folder_paths = []
  for folder_name in dst_folders:
    folder_path = dst_path.joinpath(folder_name)
    dst_folder_paths_size[folder_path] = folder_size(folder_path)

  src_folder_names = os.listdir(src_path)
  src_folder_names.sort()

  src_folder_paths_size: Dict[Path, int] = {}
  src_folder_paths = []
  for folder_name in src_folder_names:
    folder_path = src_path.joinpath(folder_name)
    src_folder_paths_size[folder_path] = folder_size(folder_path)

  # Check if translate needed
  trans_names = []
  for src_folder_path, src_size in src_folder_paths_size.items():
    folder_name = src_folder_path.name
    if folder_name in dst_folders:
      dst_size = dst_folder_paths_size[dst_path.joinpath(folder_name)]
      if src_size > dst_size:
        trans_names.append(folder_name)
    else:
      trans_names.append(folder_name)

  # TODO: Setup Translate Files
  ttl_n = len(trans_names)

  ttl_size, show, trans_names = calc_trans_size(trans_names, src_path,
                                                src_folder_paths_size)
  if ttl_size > free_size:
    print('空間不足')
    exit(0)

  # ttl_size, show, trans_names = setup_trans_size(f'總數: {ttl_n} 請輸入移轉數量:',
  #                                                src_path, src_folder_names,
  #                                                src_folder_paths_size)

  # while ttl_size > free_size:
  #   ttl_size, show, trans_names = setup_trans_size(f'總數: {ttl_n} 空間不足 請重新輸入:',
  #                                                  src_path, src_folder_names,
  #                                                  src_folder_paths_size)

  # TODO: Translate Files
  threads_map: Dict[str, MoveProcess] = {}
  while ttl_n > 0:
    nxt_names = trans_names.copy()
    for idx, folder_name in enumerate(nxt_names):
      if not folder_name in threads_map and len(threads_map) < 2:
        print(f'剩餘: {ttl_n} Process - {folder_name}')
        threads_map[folder_name] = MoveProcess(
            timeout=60 * 5,
            target=move_folder,
            args=(folder_name, src_path, dst_path, src_folder_paths_size,
                  dst_folder_paths_size))
        threads_map[folder_name].start()
      else:
        if folder_name in threads_map:
          if threads_map[folder_name].is_timeout:
            print(f'Timeout - {folder_name}')
            threads_map[folder_name].terminate()
            threads_map.pop(folder_name)
          elif not threads_map[folder_name].is_alive():
            threads_map[folder_name].join()
            threads_map.pop(folder_name)
            trans_names.remove(folder_name)
    ttl_n = len(trans_names)
