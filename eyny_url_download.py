import logging
import os
from pathlib import Path

from StreamBot import BotType, URLDownloadBot, setup_logger

if __name__ == '__main__':
  log_dir = Path(__file__).parent.joinpath('logs')
  user_profile_dir = Path(os.environ['USERPROFILE'])
  src_dirs = [user_profile_dir.joinpath('Downloads'), 'D:/Download/']
  dst_dir = 'E:/Others/Study'
  setup_logger(__file__, log_dir.as_posix())
  logger = logging.getLogger(__file__)
  logger.setLevel(logging.DEBUG)
  for src_dir in src_dirs:
    if isinstance(src_dir, Path):
      src_dir = src_dir.as_posix()
    bot = URLDownloadBot(BotType.EYNY,
                         src_dir,
                         dst_dir,
                         max_queue=5,
                         max_threads=5)
    bot.run()
