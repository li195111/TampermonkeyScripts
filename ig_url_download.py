from StreamBot import URLDownloadBot, BotType, setup_logger

if __name__ == '__main__':
  log_dir = './logs'
  src_dirs = ['C:/Users/a0983/Downloads/','G:/Download/']
  dst_dir = 'F:/Instagram'
  setup_logger(log_dir)
  for src_dir in src_dirs:
    bot = URLDownloadBot(BotType.IG,
                        src_dir,
                        dst_dir,
                        max_queue=10,
                        max_threads=10)
    bot.run()
