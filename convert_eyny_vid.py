import logging
import os
import shutil
import subprocess as sp
from pathlib import Path
from typing import List

from StreamBot import setup_logger

if __name__ == '__main__':
  log_dir = os.path.join(os.path.dirname(__file__), 'logs')
  setup_logger(__file__, log_dir, debug=True)

  logger = logging.getLogger(__file__)
  logger.setLevel(logging.DEBUG)

  avidemux_dir = 'C:/Program Files/Avidemux 2.8 VC++ 64bits'
  dst_dirs = [
      Path('D:/QChoiceNAS/SynologyDrive/Others/Study'),
      Path('D:/QChoiceNAS/SynologyDrive/Others/Study_old'),
  ]
  finished_vids: List[Path] = []
  for dst_dir in dst_dirs:
    if dst_dir.exists():
      finished_vids.extend(list(dst_dir.rglob('*.cache')))
  logger.info('Total: %s', len(finished_vids))

  for cache_path in finished_vids:
    base_name = cache_path.stem
    dir_path = cache_path.parent
    vid_path = dir_path.joinpath(base_name)
    mkv_path = dir_path.joinpath(base_name.replace('mp4', 'mkv'))
    # logger.info('Process: %s', dir_path.stem)
    if vid_path.exists() and not mkv_path.exists():
      cmd = f'avidemux_cli.exe --load "{vid_path}" --output-format MKV --save "{mkv_path}"'
      out = sp.check_output(cmd,
                            shell=True,
                            cwd=avidemux_dir,
                            stderr=sp.STDOUT)
      try:
        is_error = ('Error' in out.decode())
      except UnicodeDecodeError:
        is_error = ('Error' in out)
      if is_error:
        logger.warning('Remove Error File: %s', dir_path)
        shutil.rmtree(dir_path.as_posix())
    else:
      ...
    # logger.info('Finished: %s', dir_path.stem)
