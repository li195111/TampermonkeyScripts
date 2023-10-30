from enum import Enum
from typing import Optional, List, Any, Dict, Union

from pydantic.fields import Field
from models.base import IBase

class ContentType(Enum):
  COMMENT = "comment"


class Status(Enum):
  ACTIVE = "Active"

class FanConsiderationPageRevampEligiblity(IBase):
  should_show_social_context: bool
  should_show_content_preview: bool


class FanClubInfo(IBase):
  fan_club_id: Optional[str]
  fan_club_name: Optional[str]
  is_fan_club_referral_eligible: Optional[str]
  fan_consideration_page_revamp_eligiblity: Optional[Union[str,FanConsiderationPageRevampEligiblity]]
  is_fan_club_gifting_eligible: Optional[str]
  subscriber_count: Optional[str]
  connected_member_count: Optional[str]
  autosave_to_exclusive_highlight: Optional[str]
  has_enough_subscribers_for_ssc: Optional[str]

class HDProfilePicURLInfo(IBase):
  url: str
  width: int
  height: int
  scans_profile: Optional[str]

class CaptionUser(IBase):
  fbid_v2: str
  feed_post_reshare_disabled: bool
  full_name: str
  id: int
  is_private: bool
  is_unpublished: bool
  pk: int
  pk_id: int
  show_account_transparency_details: bool
  strong_id: str = Field(alias='strong_id__')
  third_party_downloads_enabled: int
  account_badges: List[Any]
  fan_club_info: FanClubInfo
  has_anonymous_profile_picture: bool
  hd_profile_pic_url_info: HDProfilePicURLInfo
  hd_profile_pic_versions: List[HDProfilePicURLInfo]
  is_favorite: bool
  is_verified: bool
  profile_pic_id: Optional[str]
  profile_pic_url: str
  transparency_product_enabled: bool
  username: str
  latest_reel_media: int

class Caption(IBase):
  pk: str
  user_id: int
  user: CaptionUser
  type: int
  text: str
  did_report_as_spam: bool
  created_at: int
  created_at_utc: int
  content_type: ContentType
  status: Status
  bit_flags: int
  share_enabled: bool
  is_ranked_comment: bool
  is_covered: bool
  private_reply_status: int
  media_id: str
  has_translation: Optional[bool]

class UserElement(IBase):
  pk: str
  pk_id: str
  full_name: str
  is_private: bool
  strong_id: str = Field(alias='strong_id__')
  username: str
  is_verified: bool
  profile_pic_id: Optional[str]
  profile_pic_url: str
  fbid_v2: Optional[str]
  profile_grid_display_type: Optional[str]

class In(IBase):
  user: UserElement
  position: List[float]
  start_time_in_video_in_sec: Optional[str]
  duration_in_video_in_sec: Optional[str]

class Tags(IBase):
  tags_in: Optional[List[In]]

class CarouselMediaImageVersions2(IBase):
  candidates: List[HDProfilePicURLInfo]

class SharingFrictionInfo(IBase):
  should_have_sharing_friction: bool
  bloks_app_url: Optional[str]
  sharing_friction_payload: Optional[str]

class VideoVersion(IBase):
  type: int
  width: int
  height: int
  url: str
  id: str

class CarouselMedia(IBase):
  id: str
  explore_pivot_grid: bool
  product_type: Optional[str]
  media_type: int
  accessibility_caption: Optional[str]
  image_versions2: CarouselMediaImageVersions2
  original_width: int
  original_height: int
  carousel_parent_id: str
  pk: str
  commerciality_status: str
  taken_at: int
  preview: Optional[str]
  usertags: Optional[Tags]
  featured_products: List[Any]
  fb_user_tags: Tags
  shop_routing_user_id: Optional[str]
  sharing_friction_info: SharingFrictionInfo
  product_suggestions: List[Any]
  video_versions: Optional[List[VideoVersion]]
  has_audio: Optional[bool]
  video_duration: Optional[float]
  is_dash_eligible: Optional[int]
  video_dash_manifest: Optional[str]
  video_codec: Optional[str]
  number_of_qualities: Optional[int]

class AchievementsInfo(IBase):
  show_achievements: bool
  num_earned_achievements: Optional[str]

class AudioReattributionInfo(IBase):
  should_allow_restore: bool

class AdditionalAudioInfo(IBase):
  additional_audio_username: Optional[str]
  audio_reattribution_info: AudioReattributionInfo

class AudioRankingInfo(IBase):
  best_audio_cluster_id: Optional[str]

class BrandedContentTagInfo(IBase):
  can_add_tag: bool


class Comment(IBase):
  action_type: str

class Pill(IBase):
  action_type: str
  priority: int

class EntryPointContainer(IBase):
  pill: Pill
  comment: Comment
  overflow: Optional[str]
  ufi: Optional[str]


class ContentAppreciationInfo(IBase):
  enabled: bool
  entry_point_container: Optional[Union[str, EntryPointContainer]]

class ConsumptionInfo(IBase):
  is_bookmarked: bool
  should_mute_audio_reason: str
  is_trending_in_clips: bool
  should_mute_audio_reason_type: Optional[str]
  display_media_id: Optional[str]

class OriginalSoundInfo(IBase):
  audio_asset_id: str
  music_canonical_id: Optional[str]
  progressive_download_url: str
  duration_in_ms: int
  dash_manifest: str
  ig_artist: Optional[Union[str,UserElement]]
  should_mute_audio: bool
  hide_remixing: bool
  original_media_id: str
  time_created: int
  original_audio_title: str
  consumption_info: ConsumptionInfo
  can_remix_be_shared_to_fb: bool
  can_remix_be_shared_to_fb_expansion: bool
  formatted_clips_media_count: Optional[str]
  allow_creator_to_rename: bool
  audio_parts: List[Any]
  is_explicit: bool
  original_audio_subtype: str
  is_audio_automatically_attributed: bool
  is_reuse_disabled: bool
  is_xpost_from_fb: bool
  xpost_fb_creator_info: Optional[str]
  is_original_audio_download_eligible: bool
  trend_rank: Optional[str]
  audio_filter_infos: List[Any]
  oa_owner_is_music_artist: bool

class Color(IBase):
  count: int
  hex_rgba_color: str

class ReusableTextInfo(IBase):
  id: str
  text: str
  start_time_ms: float
  end_time_ms: float
  width: float
  height: float
  offset_x: float
  offset_y: float
  z_index: int
  rotation_degree: float
  scale: float
  alignment: str
  colors: List[Color]
  text_format_type: str
  font_size: float
  text_emphasis_mode: str
  is_animated: int

class MusicAssetInfo(IBase):
  audio_cluster_id: str
  id: str
  title: str
  sanitized_title: Optional[str]
  subtitle: str
  display_artist: str
  artist_id: Optional[str]
  cover_artwork_uri: str
  cover_artwork_thumbnail_uri: str
  progressive_download_url: str
  reactive_audio_download_url: Optional[str]
  fast_start_progressive_download_url: Optional[str]
  web_30_s_preview_download_url: Optional[str]
  highlight_start_times_in_ms: List[int]
  is_explicit: bool
  dash_manifest: Optional[str]
  has_lyrics: bool
  audio_asset_id: str
  duration_in_ms: int
  dark_message: Optional[str]
  allows_saving: bool
  ig_username: Optional[str]
  is_eligible_for_audio_effects: bool

class AudioMutingInfo(IBase):
  mute_audio: bool
  mute_reason_str: str
  allow_audio_editing: bool
  show_muted_audio_toast: bool

class MusicConsumptionInfo(IBase):
  ig_artist: Optional[Union[str,UserElement]]
  placeholder_profile_pic_url: str
  should_mute_audio: bool
  should_mute_audio_reason: str
  should_mute_audio_reason_type: Optional[str]
  is_bookmarked: bool
  overlap_duration_in_ms: int
  audio_asset_start_time_in_ms: int
  allow_media_creation_with_music: bool
  is_trending_in_clips: bool
  trend_rank: Optional[str]
  formatted_clips_media_count: Optional[str]
  display_labels: Optional[str]
  should_allow_music_editing: bool
  derived_content_id: Optional[str]
  audio_filter_infos: List[Any]
  audio_muting_info: AudioMutingInfo

class MusicInfo(IBase):
  music_asset_info: MusicAssetInfo
  music_consumption_info: MusicConsumptionInfo
  music_canonical_id: Optional[str]

class MashupInfo(IBase):
  mashups_allowed: Optional[bool]
  can_toggle_mashups_allowed: Optional[bool]
  has_been_mashed_up: Optional[bool]
  is_light_weight_check: Optional[bool]
  formatted_mashups_count: Optional[str]
  original_media: Optional[str]
  privacy_filtered_mashups_media_count: Optional[str]
  non_privacy_filtered_mashups_media_count: Optional[int]
  mashup_type: Optional[str]
  is_creator_requesting_mashup: Optional[bool]
  has_nonmimicable_additional_audio: Optional[bool]
  is_pivot_page_available: Optional[bool]

class ClipsMetadata(IBase):
  music_info: Optional[Union[str, MusicInfo]]
  original_sound_info: Optional[Union[str, OriginalSoundInfo]]
  audio_type: Optional[str]
  music_canonical_id: str
  featured_label: Optional[str]
  mashup_info: Optional[Union[MashupInfo,str]]
  reusable_text_info: Optional[Union[str, List[ReusableTextInfo]]]
  reusable_text_attribute_string: Optional[str]
  nux_info: Optional[str]
  viewer_interaction_settings: Optional[str]
  branded_content_tag_info: BrandedContentTagInfo
  shopping_info: Optional[str]
  additional_audio_info: AdditionalAudioInfo
  is_shared_to_fb: bool
  breaking_content_info: Optional[str]
  challenge_info: Optional[str]
  reels_on_the_rise_info: Optional[str]
  breaking_creator_info: Optional[str]
  asset_recommendation_info: Optional[str]
  contextual_highlight_info: Optional[str]
  clips_creation_entry_point: Optional[str]
  audio_ranking_info: AudioRankingInfo
  template_info: Optional[str]
  is_fan_club_promo_video: bool
  disable_use_in_clips_client_cache: bool
  content_appreciation_info: ContentAppreciationInfo
  achievements_info: AchievementsInfo
  show_achievements: bool
  show_tips: Optional[str]
  merchandising_pill_info: Optional[str]
  is_public_chat_welcome_video: bool
  professional_clips_upsell_type: int
  external_media_info: Optional[str]

class CommentInformTreatment(IBase):
  should_have_inform_treatment: bool
  text: str
  url: Optional[str]
  action_type: Optional[str]

class Comment(IBase):
  pk: str
  user_id: str
  user: UserElement
  type: int
  text: str
  did_report_as_spam: bool
  created_at: int
  created_at_utc: int
  content_type: ContentType
  status: Status
  bit_flags: int
  share_enabled: bool
  is_ranked_comment: bool
  is_covered: bool
  private_reply_status: int
  media_id: str
  has_translation: Optional[bool]
  has_liked_comment: bool
  comment_like_count: int
  parent_comment_id: Optional[str]

class AdditionalCandidates(IBase):
  igtv_first_frame: HDProfilePicURLInfo
  first_frame: HDProfilePicURLInfo
  smart_frame: Optional[str]

class DefaultObj(IBase):
  video_length: float
  thumbnail_width: int
  thumbnail_height: int
  thumbnail_duration: float
  sprite_urls: List[str]
  thumbnails_per_row: int
  total_thumbnail_num_per_sprite: int
  max_thumbnails_per_sprite: int
  sprite_width: int
  sprite_height: int
  rendered_width: int
  file_size_kb: int

class ScrubberSpritesheetInfoCandidates(IBase):
  default: DefaultObj

class ItemImageVersions2(IBase):
  candidates: List[HDProfilePicURLInfo]
  additional_candidates: Optional[AdditionalCandidates]
  smart_thumbnail_enabled: Optional[bool]
  scrubber_spritesheet_info_candidates: Optional[ScrubberSpritesheetInfoCandidates]

class Location(IBase):
  pk: str
  short_name: str
  facebook_places_id: str
  external_source: str
  name: str
  address: str
  city: str
  has_viewer_saved: bool
  lng: Optional[float]
  lat: Optional[float]
  is_eligible_for_guides: bool

class MediaAppreciationSettings(IBase):
  media_gifting_state: str
  gift_count_visibility: str

class SquareCrop(IBase):
  crop_left: float
  crop_right: float
  crop_top: float
  crop_bottom: float

class MediaCroppingInfo(IBase):
  square_crop: Optional[SquareCrop]

class MediaNotes(IBase):
  items: List[Any]

class MusicMetadata(IBase):
  music_canonical_id: int
  audio_type: Optional[str]
  music_info: Optional[Union[str, MusicInfo]]
  original_sound_info: Optional[Union[str,OriginalSoundInfo]]
  pinned_media_ids: Optional[Union[str,List[str]]]

class Item(IBase):
  taken_at: int
  pk: str
  id: str
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
  is_unified_video: bool
  should_request_ads: bool
  is_visual_reply_commenter_notice_enabled: bool
  commerciality_status: str
  explore_hide_comments: bool
  usertags: Optional[Tags]
  photo_of_you: Optional[bool]
  shop_routing_user_id: Optional[str]
  can_see_insights_as_brand: bool
  is_organic_product_tagging_eligible: bool
  has_liked: bool
  like_count: int
  facepile_top_likers: List[UserElement]
  top_likers: List[str]
  media_type: int
  code: str
  can_viewer_reshare: bool
  caption: Optional[Caption]
  clips_tab_pinned_user_ids: List[Any]
  comment_inform_treatment: CommentInformTreatment
  sharing_friction_info: SharingFrictionInfo
  original_media_has_visual_reply_media: bool
  fb_user_tags: Tags
  invited_coauthor_producers: List[Any]
  all_previous_submitters: Optional[List[Any]]
  can_viewer_save: bool
  is_in_profile_grid: bool
  profile_grid_control_enabled: bool
  featured_products: List[Any]
  is_comments_gif_composer_enabled: bool
  product_suggestions: List[Any]
  user: CaptionUser
  image_versions2: ItemImageVersions2
  original_width: int
  original_height: int
  media_notes: MediaNotes
  product_type: Optional[str]
  is_paid_partnership: bool
  music_metadata: Optional[MusicMetadata]
  organic_tracking_token: str
  ig_media_sharing_disabled: bool
  is_open_to_public_submission: bool
  carousel_media_count: Optional[int]
  carousel_media: Optional[List[CarouselMedia]]
  carousel_media_ids: Optional[List[str]]
  carousel_media_pending_post_count: Optional[int]
  comment_likes_enabled: Optional[bool]
  comment_threading_enabled: bool
  max_num_visible_preview_comments: int
  has_more_comments: Optional[bool]
  next_max_id: Optional[str]
  preview_comments: Optional[List[Comment]]
  comments: Optional[List[Comment]]
  comment_count: int
  can_view_more_preview_comments: Optional[bool]
  hide_view_all_comment_entrypoint: Optional[bool]
  inline_composer_display_condition: Optional[str]
  has_delayed_metadata: bool
  is_auto_created: bool
  is_quiet_post: bool
  is_cutout_sticker_allowed: bool
  location: Optional[Location]
  lng: Optional[float]
  lat: Optional[float]
  fb_like_count: Optional[int]
  video_subtitles_confidence: Optional[float]
  video_subtitles_uri: Optional[str]
  play_count: Optional[int]
  fb_play_count: Optional[int]
  media_appreciation_settings: Optional[MediaAppreciationSettings]
  media_cropping_info: Optional[MediaCroppingInfo]
  is_artist_pick: Optional[bool]
  is_third_party_downloads_eligible: Optional[bool]
  clips_metadata: Optional[ClipsMetadata]
  is_dash_eligible: Optional[int]
  video_dash_manifest: Optional[str]
  video_codec: Optional[str]
  number_of_qualities: Optional[int]
  video_versions: Optional[List[VideoVersion]]
  has_audio: Optional[bool]
  video_duration: Optional[float]

class FeedUser(IBase):
  items: List[Item]
  num_results: int
  more_available: Optional[bool]
  next_max_id: Optional[str]
  user: Optional[UserElement]
  auto_load_more_enabled: Optional[bool]
  status: str
