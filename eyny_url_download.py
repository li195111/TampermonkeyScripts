from StreamBot import BotType, URLDownloadBot, setup_logger

if __name__ == '__main__':
  log_dir = './logs'
  src_dir = 'C:/Users/a0983/Downloads'
  dst_dir = 'F:/Study'
  setup_logger(log_dir)
  bot = URLDownloadBot(BotType.EYNY,
                       src_dir,
                       dst_dir,
                       max_queue=10,
                       max_threads=8)
  bot.run()
