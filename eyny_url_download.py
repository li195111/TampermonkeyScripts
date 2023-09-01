import logging
import os

from StreamBot import BotType, URLDownloadBot, setup_logger

if __name__ == '__main__':
  log_dir = os.path.join(os.path.dirname(__file__), 'logs')
  src_dir = 'C:/Users/LIDESKTOP/Downloads'
  dst_dir = 'G:/Others/Study'

  setup_logger(__file__, log_dir)

  logger = logging.getLogger(__file__)
  logger.setLevel(logging.DEBUG)

  bot = URLDownloadBot(BotType.EYNY,
                       src_dir,
                       dst_dir,
                       max_queue=10,
                       max_threads=10)
  bot.run()
