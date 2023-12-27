import logging
import os
import platform
from pathlib import Path

from StreamBot import BotType, URLDownloadBot, setup_logger

if __name__ == '__main__':
  log_dir = Path(__file__).parent.joinpath('logs')
  if platform.system().lower() == 'windows':
    user_profile_dir = Path(os.environ['USERPROFILE'])
    src_dirs = [user_profile_dir.joinpath('Downloads'), Path('D:/Download/')]
    dst_dir = Path('D:/QChoiceNAS/SynologyDrive/Others/Instagram')
    dst_dir.mkdir(parents=True, exist_ok=True)
  elif platform.system().lower() == 'linux':
    src_dirs = []
  setup_logger(__file__, log_dir.as_posix())
  logger = logging.getLogger(__file__)
  logger.setLevel(logging.DEBUG)
  for src_dir in src_dirs:
    if src_dir.exists():
      if isinstance(src_dir, Path):
        src_dir = src_dir.as_posix()
      bot = URLDownloadBot(BotType.IG,
                          src_dir,
                          dst_dir,
                          max_queue=10,
                          max_threads=10)
      bot.run()
