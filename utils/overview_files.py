import glob
import os
import re
import shutil
from pathlib import Path
from typing import List


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


def clean_string(filter_list: List[str], cleaned_name: str):
  is_unclean = sum([s in cleaned_name for s in filter_list]) > 0
  while is_unclean:
    for s in filter_list:
      if s == ' ':
        cleaned_name = cleaned_name.replace(s, '_')
      else:
        cleaned_name = cleaned_name.replace(s, '')
    is_unclean = sum([s in cleaned_name for s in filter_list]) > 0

  if cleaned_name.startswith('_'):
    cleaned_name = cleaned_name[1:]
  return cleaned_name


if __name__ == "__main__":
  name = 'Study'
  dir_paths = [Path(f'D:/{name}'), Path(f'F:/{name}')]

  # 1 MB
  min_size = 1024**4
  for dir_path in dir_paths:
    for vid_file in dir_path.glob('*/*.mp4'):
      vid_folder = vid_file.parent
      vid_folder_name = vid_folder.name
      code = re.findall(
          r'[a-zA-Z]?[a-zA-Z]?[a-zA-Z]?[a-zA-Z][a-zA-Z]-[0-9][0-9][0-9][0-9]?',
          vid_folder_name)
      fcppv_code = re.findall(
          r'FC2[\-]?PPV[\-]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?',
          vid_folder_name)
      size = folder_size(vid_folder)
      prefix = vid_folder_name[:5]
      suffix = vid_folder_name[5:]
      if size < min_size and (len(code) > 0 or len(fcppv_code) > 0):
        vid_code = code
        if len(fcppv_code) != 0:
          vid_code = fcppv_code
        vid_code = vid_code[0]

        suffix = suffix.replace(vid_code, '')
        suffix = f'{vid_code}_{suffix}'

        # filter_strs = ['巨乳','魔鏡號','人妻','巨乳','無水印','高清','有碼','本土','無碼','__',' ','…','●','[]','()','%3F','HD','jpg','≪','≫','-','◆','[野外_露出]','MOODYZDIVA','罩杯','胸圍','腰圍','臀圍','中出,巨乳,黑絲,亂倫,近親相姦','專營無修偷拍流出國產','SEX,巨乳,多P,按摩','巨乳,人妻',',學生妹,制服,運動服,多P,亂']
        # chinese_tags = ['中文字幕','繁體中字','中國語字幕','繁體','中字','中文']
      suffix = clean_string([' ', '__'], suffix)
      new_name = f'{prefix}{suffix}'
      print(new_name)
