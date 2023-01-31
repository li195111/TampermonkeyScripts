from enum import Enum, IntEnum

class BotType(Enum):
  IG = 'ig'
  EYNY = 'eyny'

class MediaType(Enum):
  IMGS = 'imgs'
  IMG = 'img'
  VIDS = 'vids'
  VID = 'vid'

class FileSizeLevel(IntEnum):
  KB = 0
  MB = 1
  GB = 2

class FileState(IntEnum):
  QUEUE = 0
  DOWNLOAD = 1
  FINISHED = 2