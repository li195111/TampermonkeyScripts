from StreamBot import BotType, URLDownloadBot, setup_logger

if __name__ == '__main__':
  log_dir = './logs'
  src_dir = 'C:/Users/LIDESKTOP/Downloads'
  dst_dir = 'G:/Others/Study'
  setup_logger(log_dir)
  bot = URLDownloadBot(BotType.EYNY,
                       src_dir,
                       dst_dir,
                       max_queue=10,
                       max_threads=10)
  bot.run()
