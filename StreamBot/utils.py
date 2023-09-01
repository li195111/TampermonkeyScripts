import glob
import logging
import os
import sys
import traceback
from datetime import datetime, timedelta

from .enums import FileSizeLevel


def clean_up_logs(save_dir: str, log_keep_days: int):
  logs = glob.glob(os.path.join(save_dir, '*.log'), recursive=True)
  for log in logs:
    fn = os.path.basename(log)
    date_str = fn.split('.')[0].split('_')[-2]
    date = datetime.strptime(date_str, '%Y%m%d')
    if date < datetime.today() - timedelta(days=log_keep_days):
      os.remove(log)

def setup_logger(logger_name: str,
                 save_dir: str,
                 log_keep_days: int = 7,
                 ext_name: str = '',
                 log_file: bool = True,
                 debug: bool = False):
  save_dir = os.path.abspath(save_dir)
  os.makedirs(save_dir, exist_ok=True)
  clean_up_logs(save_dir, log_keep_days)

  formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
  log_time = datetime.now().strftime('%Y%m%d_%H%M%S')
  logger_name = os.path.basename(logger_name)

  hdls = []
  if log_file:
    log_file_name = f'{logger_name.split(".")[0]}'
    if ext_name is not None and ext_name != '':
      log_file_name = f'{log_file_name}_{ext_name}'
    log_file_name = f'{log_file_name}_{log_time}.log'
    log_file_path = os.path.join(save_dir, log_file_name)

    file_hdl = logging.FileHandler(log_file_path, encoding='utf-8')
    file_hdl.setFormatter(formatter)
    file_hdl.setLevel(logging.DEBUG)
    hdls.append(file_hdl)

  stream_hdl = logging.StreamHandler(sys.stdout)
  stream_hdl.setFormatter(formatter)
  log_level = logging.INFO
  if debug:
    log_level = logging.DEBUG
  stream_hdl.setLevel(log_level)
  hdls.append(stream_hdl)

  logging.basicConfig(handlers=hdls)


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
