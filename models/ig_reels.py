from typing import Any, Dict, List, Optional, Union

from pydantic.fields import Field

from models.base import IBase
from models.enums import (ID, AppID, BloksStickerType, CommercialityStatus,
                          Crosspost, ProductType, VideoCodec)


class CommentInformTreatment(IBase):
  should_have_inform_treatment: bool
  text: str
  url: Optional[str] = None
  action_type: Optional[str] = None


class Candidate(IBase):
  width: int
  height: int
  url: str


class ImageVersions2(IBase):
  candidates: List[Candidate]


class SharingFrictionInfo(IBase):
  should_have_sharing_friction: bool
  bloks_app_url: Optional[str] = None
  sharing_friction_payload: Optional[str] = None


class IgMention(IBase):
  account_id: str
  username: str
  full_name: str
  profile_pic_url: str


class StickerData(IBase):
  ig_mention: IgMention


class BloksSticker(IBase):
  id: ID
  app_id: AppID
  sticker_data: StickerData
  bloks_sticker_type: BloksStickerType


class StoryBloksSticker(IBase):
  bloks_sticker: BloksSticker
  x: float
  y: float
  z: int
  width: float
  height: float
  rotation: float


class StoryLink(IBase):
  link_type: str
  url: str
  link_title: str
  display_url: str


class Story(IBase):
  x: float
  y: float
  z: int
  width: float
  height: float
  rotation: float
  is_pinned: int
  is_hidden: int
  is_sticker: int
  is_fb_sticker: int
  start_time_ms: float
  end_time_ms: float
  media_id: Optional[str] = None
  product_type: Optional[str] = None
  media_code: Optional[str] = None
  media_compound_str: Optional[str] = None
  story_link: Optional[StoryLink] = None


class ItemUser(IBase):
  pk: int
  is_private: bool


class VideoVersion(IBase):
  type: int
  width: int
  height: int
  url: str
  id: str


class Item(IBase):
  taken_at: int
  pk: str
  id: str
  caption_position: float
  is_reel_media: bool
  is_terminal_video_segment: bool
  device_timestamp: int
  client_cache_key: str
  filter_type: int
  caption_is_edited: bool
  like_and_view_counts_disabled: bool
  strong_id: str = Field(alias='strong_id__')
  is_reshare_of_text_post_app_media_in_ig: bool
  is_post_live_clips_media: bool
  deleted_reason: int
  integrity_review_decision: str
  has_shared_to_fb: int
  expiring_at: int
  is_unified_video: bool
  should_request_ads: bool
  is_visual_reply_commenter_notice_enabled: bool
  commerciality_status: CommercialityStatus
  explore_hide_comments: bool
  shop_routing_user_id: Optional[str] = None
  can_see_insights_as_brand: bool
  is_organic_product_tagging_eligible: bool
  likers: List[Any]
  media_type: int
  code: str
  caption: Optional[str] = None
  clips_tab_pinned_user_ids: List[Any]
  comment_inform_treatment: CommentInformTreatment
  sharing_friction_info: SharingFrictionInfo
  has_translation: bool
  original_media_has_visual_reply_media: bool
  can_viewer_save: bool
  is_in_profile_grid: bool
  profile_grid_control_enabled: bool
  is_comments_gif_composer_enabled: bool
  product_suggestions: List[Any]
  image_versions2: ImageVersions2
  original_width: int
  original_height: int
  product_type: ProductType
  is_paid_partnership: bool
  music_metadata: Optional[str] = None
  organic_tracking_token: str
  ig_media_sharing_disabled: bool
  crosspost: Optional[List[Crosspost]] = None
  is_open_to_public_submission: bool
  has_delayed_metadata: bool
  is_auto_created: bool
  is_cutout_sticker_allowed: bool
  is_dash_eligible: Optional[int] = None
  video_dash_manifest: Optional[str] = None
  video_codec: Optional[Union[VideoCodec, str]] = None
  number_of_qualities: Optional[int] = None
  video_versions: Optional[List[VideoVersion]] = None
  has_audio: Optional[bool] = None
  video_duration: Optional[float] = None
  user: ItemUser
  can_reshare: bool
  can_reply: bool
  can_send_prompt: bool
  is_first_take: bool
  is_rollcall_v2: bool
  is_superlative: bool
  is_fb_post_from_fb_story: bool
  can_play_spotify_audio: bool
  archive_story_deletion_ts: int
  created_from_add_yours_browsing: bool
  story_link_stickers: Optional[List[Story]] = None
  story_bloks_stickers: Optional[List[StoryBloksSticker]] = None
  has_liked: bool
  supports_reel_reactions: bool
  can_send_custom_emojis: bool
  show_one_tap_fb_share_tooltip: bool
  accessibility_caption: Optional[str] = None
  attribution_content_url: Optional[str] = None
  story_feed_media: Optional[List[Story]] = None
  imported_taken_at: Optional[int] = None


class FriendshipStatus(IBase):
  following: bool
  is_private: bool
  incoming_request: bool
  outgoing_request: bool
  is_bestie: bool
  is_restricted: bool
  is_feed_favorite: bool


class The51054288_User(IBase):
  pk: int
  pk_id: int
  full_name: str
  is_private: bool
  strong_id: int = Field(alias='strong_id__')
  username: str
  interop_messaging_user_fbid: int
  is_verified: bool
  friendship_status: FriendshipStatus
  profile_pic_id: str
  profile_pic_url: str


class Reel(IBase):
  id: int
  strong_id: int = Field(alias='strong_id__')
  latest_reel_media: int
  expiring_at: int
  seen: int
  can_reply: bool
  can_gif_quick_reply: bool
  can_reshare: bool
  can_react_with_avatar: bool
  reel_type: str
  ad_expiry_timestamp_in_millis: Optional[str] = None
  is_cta_sticker_available: Optional[str] = None
  app_sticker_info: Optional[str] = None
  should_treat_link_sticker_as_cta: Optional[str] = None
  user: The51054288_User
  items: List[Item]
  prefetch_count: int
  media_count: int
  media_ids: List[str]
  is_cacheable: bool
  disabled_reply_types: List[str]
  eligible_for_hype: Optional[bool] = None


class InsReels(IBase):
  reels: Dict[str, Reel]
  reels_media: List[Reel]
  status: str
