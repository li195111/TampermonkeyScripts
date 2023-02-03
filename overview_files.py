import os
import re
import glob
import shutil
from pathlib import Path

if __name__ == "__main__":
  name = 'Study'
  src_path = Path(f'D:/{name}')
  dir_paths = [src_path]

  # 1 MB
  min_size = 1024**2
  for dir_path in dir_paths:
    for vid in glob.glob(f'{dir_path}/*/*.mp4', recursive=True):
      vid_dir_path = os.path.dirname(vid)
      vid_name = os.path.basename(vid_dir_path)
      code = re.findall(
          r'[a-zA-Z]?[a-zA-Z]?[a-zA-Z]?[a-zA-Z][a-zA-Z]-[0-9][0-9][0-9][0-9]?',
          vid_name)
      fcppv_code = re.findall(r'FC2[\-]?PPV[\-]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?[0-9]?', vid_name)
      if len(code) > 0 or len(fcppv_code) > 0:
        if (os.path.exists(vid)):
          if os.path.getsize(vid) < min_size:
            if len(fcppv_code) == 0:
              print(code, vid_dir_path)
            else:
              print(fcppv_code, vid_dir_path)
