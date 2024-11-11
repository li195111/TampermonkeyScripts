from enum import Enum
from typing import Any, Dict, List, Optional, Union

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
  fan_club_id: Optional[str] = None
  fan_club_name: Optional[str] = None
  is_fan_club_referral_eligible: Optional[bool] = None
  fan_consideration_page_revamp_eligiblity: Optional[Union[str,
                                                           FanConsiderationPageRevampEligiblity]] = None
  is_fan_club_gifting_eligible: Optional[bool] = None
  subscriber_count: Optional[int] = None
  connected_member_count: Optional[int] = None
  autosave_to_exclusive_highlight: Optional[bool] = None
  has_enough_subscribers_for_ssc: Optional[bool] = None


class HDProfilePicURLInfo(IBase):
  url: str
  width: int
  height: int
  scans_profile: Optional[str] = None


class CaptionUser(IBase):
  fbid_v2: str
  feed_post_reshare_disabled: Optional[bool] = None
  full_name: str
  id: int
  is_private: bool
  is_unpublished: Optional[bool] = None
  pk: int
  pk_id: int
  show_account_transparency_details: Optional[bool] = None
  strong_id: str = Field(alias='strong_id__')
  third_party_downloads_enabled: Optional[int] = None
  account_badges: Optional[List[Any]] = None
  fan_club_info: Optional[FanClubInfo] = None
  has_anonymous_profile_picture: Optional[bool] = None
  hd_profile_pic_url_info: Optional[HDProfilePicURLInfo] = None
  hd_profile_pic_versions: Optional[List[HDProfilePicURLInfo]] = None
  is_favorite: Optional[bool] = None
  is_verified: bool
  profile_pic_id: Optional[str] = None
  profile_pic_url: str
  transparency_product_enabled: Optional[bool] = None
  username: str
  latest_reel_media: Optional[int] = None


class Caption(IBase):
  pk: str
  user_id: int
  user: CaptionUser
  type: int
  text: str
  did_report_as_spam: bool
  created_at: int
  created_at_utc: int
  content_type: str
  status: str
  bit_flags: int
  share_enabled: bool
  is_ranked_comment: bool
  is_covered: bool
  private_reply_status: Optional[int] = None
  media_id: str
  has_translation: Optional[bool] = None


class UserElement(IBase):
  pk: str
  pk_id: str
  full_name: str
  is_private: bool
  strong_id: str = Field(alias='strong_id__')
  username: str
  is_verified: bool
  profile_pic_id: Optional[str] = None
  profile_pic_url: str
  fbid_v2: Optional[str] = None
  profile_grid_display_type: Optional[str] = None


class In(IBase):
  user: UserElement
  position: List[float]
  start_time_in_video_in_sec: Optional[str] = None
  duration_in_video_in_sec: Optional[str] = None


class Tags(IBase):
  tags_in: Optional[List[In]] = None


class CarouselMediaImageVersions2(IBase):
  candidates: List[HDProfilePicURLInfo]


class SharingFrictionInfo(IBase):
  should_have_sharing_friction: bool
  bloks_app_url: Optional[str] = None
  sharing_friction_payload: Optional[str] = None


class VideoVersion(IBase):
  type: int
  width: int
  height: int
  url: str
  id: str


class CarouselMedia(IBase):
  id: str
  explore_pivot_grid: bool
  product_type: Optional[str] = None
  media_type: int
  accessibility_caption: Optional[str] = None
  image_versions2: CarouselMediaImageVersions2
  original_width: int
  original_height: int
  carousel_parent_id: str
  pk: str
  commerciality_status: str
  taken_at: int
  preview: Optional[str] = None
  usertags: Optional[Tags] = None
  featured_products: Optional[List[Any]] = None
  fb_user_tags: Tags
  shop_routing_user_id: Optional[str] = None
  sharing_friction_info: SharingFrictionInfo
  product_suggestions: List[Any]
  video_versions: Optional[List[VideoVersion]] = None
  has_audio: Optional[bool] = None
  video_duration: Optional[float] = None
  is_dash_eligible: Optional[int] = None
  video_dash_manifest: Optional[str] = None
  video_codec: Optional[str] = None
  number_of_qualities: Optional[int] = None


class AchievementsInfo(IBase):
  show_achievements: Optional[bool] = None
  num_earned_achievements: Optional[str] = None


class AudioReattributionInfo(IBase):
  should_allow_restore: bool


class AdditionalAudioInfo(IBase):
  additional_audio_username: Optional[str] = None
  audio_reattribution_info: AudioReattributionInfo


class AudioRankingInfo(IBase):
  best_audio_cluster_id: Optional[str] = None


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
  overflow: Optional[str] = None
  ufi: Optional[str] = None


class ContentAppreciationInfo(IBase):
  enabled: bool
  entry_point_container: Optional[Union[str, EntryPointContainer]] = None


class ConsumptionInfo(IBase):
  is_bookmarked: bool
  should_mute_audio_reason: str
  is_trending_in_clips: bool
  should_mute_audio_reason_type: Optional[str] = None
  display_media_id: Optional[str] = None


class OriginalSoundInfo(IBase):
  audio_asset_id: str
  music_canonical_id: Optional[str] = None
  progressive_download_url: str
  duration_in_ms: int
  dash_manifest: str
  ig_artist: Optional[Union[str, UserElement]] = None
  should_mute_audio: bool
  hide_remixing: bool
  original_media_id: str
  time_created: int
  original_audio_title: str
  consumption_info: ConsumptionInfo
  can_remix_be_shared_to_fb: bool
  can_remix_be_shared_to_fb_expansion: bool
  formatted_clips_media_count: Optional[str] = None
  allow_creator_to_rename: bool
  audio_parts: List[Any]
  is_explicit: bool
  original_audio_subtype: str
  is_audio_automatically_attributed: bool
  is_reuse_disabled: bool
  is_xpost_from_fb: bool
  xpost_fb_creator_info: Optional[str] = None
  is_original_audio_download_eligible: bool
  trend_rank: Optional[str] = None
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
  sanitized_title: Optional[str] = None
  subtitle: str
  display_artist: str
  artist_id: Optional[str] = None
  cover_artwork_uri: str
  cover_artwork_thumbnail_uri: str
  progressive_download_url: str
  reactive_audio_download_url: Optional[str] = None
  fast_start_progressive_download_url: Optional[str] = None
  web_30_s_preview_download_url: Optional[str] = None
  highlight_start_times_in_ms: List[int]
  is_explicit: bool
  dash_manifest: Optional[str] = None
  has_lyrics: bool
  audio_asset_id: str
  duration_in_ms: int
  dark_message: Optional[str] = None
  allows_saving: bool
  ig_username: Optional[str] = None
  is_eligible_for_audio_effects: bool


class AudioMutingInfo(IBase):
  mute_audio: bool
  mute_reason_str: str
  allow_audio_editing: bool
  show_muted_audio_toast: bool


class MusicConsumptionInfo(IBase):
  ig_artist: Optional[Union[str, UserElement]] = None
  placeholder_profile_pic_url: str
  should_mute_audio: bool
  should_mute_audio_reason: str
  should_mute_audio_reason_type: Optional[str] = None
  is_bookmarked: bool
  overlap_duration_in_ms: int
  audio_asset_start_time_in_ms: int
  allow_media_creation_with_music: bool
  is_trending_in_clips: bool
  trend_rank: Optional[str] = None
  formatted_clips_media_count: Optional[str] = None
  display_labels: Optional[Union[List[str], str]] = None
  should_allow_music_editing: bool
  derived_content_id: Optional[str] = None
  audio_filter_infos: List[Any]
  audio_muting_info: AudioMutingInfo


class MusicInfo(IBase):
  music_asset_info: MusicAssetInfo
  music_consumption_info: MusicConsumptionInfo
  music_canonical_id: Optional[str] = None


class MashupInfo(IBase):
  mashups_allowed: Optional[bool] = None
  can_toggle_mashups_allowed: Optional[bool] = None
  has_been_mashed_up: Optional[bool] = None
  is_light_weight_check: Optional[bool] = None
  formatted_mashups_count: Optional[str] = None
  original_media: Optional[Union[str, dict]] = None
  privacy_filtered_mashups_media_count: Optional[str] = None
  non_privacy_filtered_mashups_media_count: Optional[int] = None
  mashup_type: Optional[str] = None
  is_creator_requesting_mashup: Optional[bool] = None
  has_nonmimicable_additional_audio: Optional[bool] = None
  is_pivot_page_available: Optional[bool] = None


class ClipsMetadata(IBase):
  music_info: Optional[Union[str, MusicInfo]] = None
  original_sound_info: Optional[Union[str, OriginalSoundInfo]] = None
  audio_type: Optional[str] = None
  music_canonical_id: str
  featured_label: Optional[str] = None
  mashup_info: Optional[Union[MashupInfo, str]] = None
  reusable_text_info: Optional[Union[str, List[ReusableTextInfo]]] = None
  reusable_text_attribute_string: Optional[str] = None
  nux_info: Optional[str] = None
  viewer_interaction_settings: Optional[str] = None
  branded_content_tag_info: BrandedContentTagInfo
  shopping_info: Optional[str] = None
  additional_audio_info: AdditionalAudioInfo
  is_shared_to_fb: bool
  breaking_content_info: Optional[str] = None
  challenge_info: Optional[str] = None
  reels_on_the_rise_info: Optional[str] = None
  breaking_creator_info: Optional[str] = None
  asset_recommendation_info: Optional[str] = None
  contextual_highlight_info: Optional[str] = None
  clips_creation_entry_point: Optional[str] = None
  audio_ranking_info: Optional[AudioRankingInfo] = None
  template_info: Optional[str] = None
  is_fan_club_promo_video: bool
  disable_use_in_clips_client_cache: bool
  content_appreciation_info: ContentAppreciationInfo
  achievements_info: AchievementsInfo
  show_achievements: Optional[bool] = None
  show_tips: Optional[str] = None
  merchandising_pill_info: Optional[str] = None
  is_public_chat_welcome_video: bool
  professional_clips_upsell_type: int
  external_media_info: Optional[str] = None


class CommentInformTreatment(IBase):
  should_have_inform_treatment: bool
  text: str
  url: Optional[str] = None
  action_type: Optional[str] = None


class Comment(IBase):
  pk: str
  user_id: str
  user: UserElement
  type: int
  text: str
  did_report_as_spam: bool
  created_at: int
  created_at_utc: int
  content_type: str
  status: str
  bit_flags: int
  share_enabled: bool
  is_ranked_comment: bool
  is_covered: bool
  private_reply_status: Optional[int] = None
  media_id: str
  has_translation: Optional[bool] = None
  has_liked_comment: bool
  comment_like_count: int
  parent_comment_id: Optional[str] = None


class AdditionalCandidates(IBase):
  igtv_first_frame: HDProfilePicURLInfo
  first_frame: HDProfilePicURLInfo
  smart_frame: Optional[str] = None


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
  additional_candidates: Optional[AdditionalCandidates] = None
  smart_thumbnail_enabled: Optional[bool] = None
  scrubber_spritesheet_info_candidates: Optional[ScrubberSpritesheetInfoCandidates] = None


class Location(IBase):
  pk: str
  short_name: str
  facebook_places_id: str
  external_source: str
  name: str
  address: str
  city: str
  has_viewer_saved: bool
  lng: Optional[float] = None
  lat: Optional[float] = None
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
  square_crop: Optional[SquareCrop] = None


class MediaNotes(IBase):
  items: List[Any]


class MusicMetadata(IBase):
  music_canonical_id: int
  audio_type: Optional[str] = None
  music_info: Optional[Union[str, MusicInfo]] = None
  original_sound_info: Optional[Union[str, OriginalSoundInfo]] = None
  pinned_media_ids: Optional[Union[str, List[str]]] = None


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
  usertags: Optional[Tags] = None
  photo_of_you: Optional[bool] = None
  shop_routing_user_id: Optional[str] = None
  can_see_insights_as_brand: bool
  is_organic_product_tagging_eligible: bool
  has_liked: bool
  like_count: int
  facepile_top_likers: Optional[List[UserElement]] = None
  top_likers: Optional[List[str]] = None
  media_type: int
  code: str
  can_viewer_reshare: bool
  caption: Optional[Caption] = None
  clips_tab_pinned_user_ids: List[Any]
  comment_inform_treatment: CommentInformTreatment
  sharing_friction_info: SharingFrictionInfo
  original_media_has_visual_reply_media: Optional[bool] = None
  fb_user_tags: Tags
  invited_coauthor_producers: List[Any]
  all_previous_submitters: Optional[List[Any]] = None
  can_viewer_save: bool
  is_in_profile_grid: bool
  profile_grid_control_enabled: bool
  featured_products: Optional[List[Any]] = None
  is_comments_gif_composer_enabled: bool
  product_suggestions: List[Any]
  user: CaptionUser
  image_versions2: ItemImageVersions2
  original_width: int
  original_height: int
  media_notes: Optional[MediaNotes] = None
  product_type: Optional[str] = None
  is_paid_partnership: bool
  music_metadata: Optional[MusicMetadata] = None
  organic_tracking_token: str
  ig_media_sharing_disabled: bool
  is_open_to_public_submission: bool
  carousel_media_count: Optional[int] = None
  carousel_media: Optional[List[CarouselMedia]] = None
  carousel_media_ids: Optional[List[str]] = None
  carousel_media_pending_post_count: Optional[int] = None
  comment_likes_enabled: Optional[bool] = None
  comment_threading_enabled: bool
  max_num_visible_preview_comments: int
  has_more_comments: Optional[bool] = None
  next_max_id: Optional[str] = None
  preview_comments: Optional[List[Comment]] = None
  comments: Optional[List[Comment]] = None
  comment_count: int
  can_view_more_preview_comments: Optional[bool] = None
  hide_view_all_comment_entrypoint: Optional[bool] = None
  inline_composer_display_condition: Optional[str] = None
  has_delayed_metadata: Optional[bool] = None
  is_auto_created: Optional[bool] = None
  is_quiet_post: bool
  is_cutout_sticker_allowed: bool
  location: Optional[Location] = None
  lng: Optional[float] = None
  lat: Optional[float] = None
  fb_like_count: Optional[int] = None
  video_subtitles_confidence: Optional[float] = None
  video_subtitles_uri: Optional[str] = None
  play_count: Optional[int] = None
  fb_play_count: Optional[int] = None
  media_appreciation_settings: Optional[MediaAppreciationSettings] = None
  media_cropping_info: Optional[MediaCroppingInfo] = None
  is_artist_pick: Optional[bool] = None
  is_third_party_downloads_eligible: Optional[bool] = None
  clips_metadata: Optional[ClipsMetadata] = None
  is_dash_eligible: Optional[int] = None
  video_dash_manifest: Optional[str] = None
  video_codec: Optional[str] = None
  number_of_qualities: Optional[int] = None
  video_versions: Optional[List[VideoVersion]] = None
  has_audio: Optional[bool] = None
  video_duration: Optional[float] = None


class FeedUser(IBase):
  items: List[Item]
  num_results: int
  more_available: Optional[bool] = None
  next_max_id: Optional[str] = None
  user: Optional[UserElement] = None
  auto_load_more_enabled: Optional[bool] = None
  status: str
