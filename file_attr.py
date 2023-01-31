import os

if __name__ == '__main__':
  dir_path = 'H:/Instagram'
  with os.scandir(dir_path) as dir_entries:
    for entry in dir_entries:
      info = entry.stat()
      print(info)
