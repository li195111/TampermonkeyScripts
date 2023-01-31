import os
import re
import shutil
from datetime import datetime
import platform
import dataclasses
from typing import Union


@dataclasses.dataclass
class FileInfo:
  path: str
  create: Union[float, datetime]
  modify: Union[float, datetime]

  def __post_init__(self):
    self.create = datetime.fromtimestamp(self.create)
    self.modify = datetime.fromtimestamp(self.modify)


def file_infos(file_path):
  stat = os.stat(file_path)
  if platform.system() == 'Windows':
    return FileInfo(path=file_path, create=stat.st_ctime, modify=stat.st_mtime)
  else:
    try:
      return FileInfo(path=file_path,
                      create=stat.st_birthtime,
                      modify=stat.st_mtime)
    except AttributeError:
      return FileInfo(path=file_path, create=None, modify=stat.st_mtime)


if __name__ == '__main__':
  dst_dir = 'F:/Study'
  prefix = 'eyny_'
  vid_names_with_prefix = os.listdir(dst_dir)
  vid_names_without_prefix = [
      vid_name[len(prefix):] for vid_name in vid_names_with_prefix
      if vid_name.startswith(prefix)
  ]
  vid_names_without_prefix.sort()

  for idx, vid_name in enumerate(vid_names_without_prefix):
    vid_path = os.path.join(dst_dir, vid_names_with_prefix[idx])
    code = re.findall(
        r'[a-zA-Z]?[a-zA-Z]?[a-zA-Z][a-zA-Z]-[0-9][0-9][0-9][0-9]?', vid_name)
    fc_series = re.findall(r'FC2*', vid_name)
    if len(code) > 0 or len(fc_series) > 0:
      # code = code[0][0].strip().replace('_','')
      # print(code)
      ...
    else:
      ...
      # print(vid_name)
    # print(code, len(code))
    file = file_infos(vid_path)
    if isinstance(file.create, datetime):
      time_diff = datetime.now() - file.create
    else:
      time_diff = datetime.now() - datetime.fromtimestamp(file.create)
    if time_diff.days > 30:
      print(f'Remove: {code} {vid_name}')
      shutil.rmtree(file.path)
