from enum import Enum
from typing import Any, List, Optional
from uuid import UUID

from pydantic.fields import Field

from models.base import IBase


class StoryLikesConfig(IBase):
  is_enabled: bool
  ufi_type: int

class DisabledReplyType(Enum):
  STORY_REMIX_REPLY = "story_remix_reply"
  STORY_SELFIE_REPLY = "story_selfie_reply"


class RankerScores(IBase):
  ptap: float
  fp: float
  vm: float

class ReelType(Enum):
  USER_REEL = "user_reel"


class BirthdayTodayVisibilityForViewer(Enum):
  NOT_VISIBLE = "NOT_VISIBLE"


class FriendshipStatus(IBase):
  muting: bool
  is_muting_reel: bool
  following: bool
  is_bestie: bool
  outgoing_request: bool

class User(IBase):
  pk: str
  pk_id: str
  full_name: str
  is_private: bool
  strong_id: str = Field(alias='strong_id__')
  username: str
  is_verified: bool
  profile_pic_id: str
  profile_pic_url: str
  birthday_today_visibility_for_viewer: BirthdayTodayVisibilityForViewer
  friendship_status: FriendshipStatus

class Tray(IBase):
  id: str
  strong_id: str = Field(alias='strong_id__')
  latest_reel_media: int
  expiring_at: int
  seen: int
  can_reply: bool
  can_gif_quick_reply: bool
  can_reshare: bool
  can_react_with_avatar: bool
  reel_type: ReelType
  ad_expiry_timestamp_in_millis: None
  is_cta_sticker_available: None
  app_sticker_info: None
  should_treat_link_sticker_as_cta: None
  user: User
  ranked_position: int
  seen_ranked_position: int
  muted: bool
  prefetch_count: int
  ranker_scores: Optional[RankerScores]
  story_duration_secs: Optional[int]
  story_wedge_size: Optional[int]
  has_besties_media: bool
  latest_besties_reel_media: float
  media_count: int
  media_ids: List[str]
  has_video: bool
  has_fan_club_media: bool
  show_fan_club_stories_teaser: bool
  disabled_reply_types: List[DisabledReplyType]
  eligible_for_hype: bool

class ReelsTray(IBase):
  tray: List[Tray]
  story_ranking_token: UUID
  story_likes_config: StoryLikesConfig
  quick_snaps: None
  broadcasts: List[Any]
  sticker_version: int
  face_filter_nux_version: int
  stories_viewer_gestures_nux_eligible: bool
  has_new_nux_story: bool
  refresh_window_ms: int
  response_timestamp: int
  status: str
