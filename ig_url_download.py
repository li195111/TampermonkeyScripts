import logging
import os
from StreamBot import BotType, URLDownloadBot, setup_logger

if __name__ == '__main__':
  log_dir = os.path.join(os.path.dirname(__file__), 'logs')
  src_dirs = ['C:/Users/LIDESKTOP/Downloads/','G:/Download/']
  dst_dir = 'G:/Others/Instagram'
  setup_logger(__file__, log_dir)
  logger = logging.getLogger(__file__)
  logger.setLevel(logging.DEBUG)
  for src_dir in src_dirs:
    bot = URLDownloadBot(BotType.IG,
                        src_dir,
                        dst_dir,
                        max_queue=10,
                        max_threads=30)
    bot.run()
