from StreamBot import URLDownloadBot, BotType, setup_logger

if __name__ == '__main__':
  log_dir = './logs'
  src_dir = 'C:/Users/a0983/Downloads/'
  dst_dir = 'F:/Instagram'
  setup_logger(log_dir)
  bot = URLDownloadBot(BotType.IG,
                       src_dir,
                       dst_dir,
                       max_queue=10,
                       max_threads=10)
  bot.run()
