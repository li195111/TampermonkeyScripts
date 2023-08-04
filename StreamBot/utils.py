import logging
import os
import sys
import traceback
from datetime import datetime

from .enums import FileSizeLevel


def setup_logger(save_dir: str = './logs', debug: bool = False):
  os.makedirs(save_dir, exist_ok=True)
  formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
  logger_name = os.path.basename(__file__)
  log_time = datetime.now().strftime('%Y%m%d_%H%M%S')
  log_file_name = f'{logger_name.split(".")[0]}_{log_time}.log'
  log_file_path = os.path.join(save_dir, log_file_name)

  file_hdl = logging.FileHandler(log_file_path)
  file_hdl.setFormatter(formatter)
  file_hdl.setLevel(logging.DEBUG)

  stream_hdl = logging.StreamHandler(sys.stdout)
  stream_hdl.setFormatter(formatter)
  stream_hdl.setLevel(logging.DEBUG if debug else logging.INFO)

  logging.basicConfig(level=logging.DEBUG, handlers=[stream_hdl])


def error_msg(err):
  error_class = err.__class__.__name__
  if len(err.args) > 0:
    detail = err.args[0]
  else:
    detail = ''
  cl, exc, tb = sys.exc_info()
  details = '\n'.join([
      f"File \"{s[0]}\", line {s[1]} in {s[2]}"
      for s in traceback.extract_tb(tb)
  ])
  errMsg = f"\n[{error_class}] {detail}"
  return f"\n{details}{errMsg}\n"


def count_bytes_level(bts: int):
  numb = bts / 1024
  level = 0
  while numb > 1024 and level < 2:
    numb /= 1024
    level += 1
  return numb, FileSizeLevel(level)
