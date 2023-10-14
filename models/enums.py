from enum import Enum


class CommercialityStatus(Enum):
  NOT_COMMERCIAL = "not_commercial"


class Crosspost(Enum):
  FB = "FB"
  IG = "IG"

class IntegrityReviewDecision(Enum):
  PENDING = "pending"


class ProductType(Enum):
  STORY = "story"


class AppID(Enum):
  COM_BLOKS_WWW_STICKER_IG_MENTION_SCREEN = "com.bloks.www.sticker.ig.mention.screen"


class BloksStickerType(Enum):
  MENTION = "mention"


class ID(Enum):
  BLOKS_STICKER_ID = "bloks_sticker_id"

class VideoCodec(Enum):
  AVC1_64001_F = "avc1.64001f"
  AVC1_64001_E = "avc1.64001e"
