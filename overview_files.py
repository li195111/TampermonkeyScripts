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
  print(f'Min Size: {min_size}')
  for dir_path in dir_paths:
    for vid in glob.glob(f'{dir_path}/*/*.mp4', recursive=True):
      vid_dir_path = os.path.dirname(vid)
      vid_name = os.path.basename(vid_dir_path)
      code = re.findall(
          r'[a-zA-Z]?[a-zA-Z]?[a-zA-Z]?[a-zA-Z][a-zA-Z]-[0-9][0-9][0-9][0-9]?',
          vid_name)
      fc_series = re.findall(r'FC2*', vid_name)
      if len(code) > 0 or len(fc_series) > 0:
        if (os.path.exists(vid)):
          if os.path.getsize(vid) < min_size:
            print(code, vid_dir_path)
            # shutil.rmtree(vid_dir_path)
  # vid_dir_names = os.listdir(dir_path)
  # for vid_dir_name in vid_dir_names:
  #   vid_dir_path = os.path.join(dir_path,vid_dir_name)
