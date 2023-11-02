import glob
import logging
import os
import subprocess as sp
from pathlib import Path
import shutil

from StreamBot import setup_logger

if __name__ == '__main__':
  log_dir = os.path.join(os.path.dirname(__file__), 'logs')
  setup_logger(__file__, log_dir, debug=True)

  logger = logging.getLogger(__file__)
  logger.setLevel(logging.DEBUG)

  avidemux_dir = "C:/Program Files/Avidemux 2.8 VC++ 64bits"
  src_dir = 'C:/Users/LIDESKTOP/Downloads'
  dst_dir = 'G:/Others/Study'
  finished_vids = glob.glob(f'{dst_dir}/*/*.cache')
  for vid in finished_vids:
    cache_path = Path(vid)
    base_name = cache_path.stem
    dir_path = cache_path.parent
    vid_path = dir_path.joinpath(base_name)
    mkv_path = dir_path.joinpath(base_name.replace('mp4','mkv'))
    logger.info('Process: %s', dir_path.stem)
    if vid_path.exists() and not mkv_path.exists():
      cmd = f'avidemux_cli.exe --load "{vid_path}" --output-format MKV --save "{mkv_path}"'
      out = sp.check_output(cmd, shell=True, cwd=avidemux_dir, stderr=sp.STDOUT)
      is_error = ('Error' in out.decode())
      if is_error:
        logger.warning('Remove Error File: %s', dir_path)
        shutil.rmtree(dir_path.as_posix())
    else:
      ...
    # logger.info('Finished: %s', dir_path.stem)
