from enum import Enum
from typing import Any, List, Optional, Union

from pydantic.fields import Field

from models.base import IBase


class BioLink(IBase):
  title: str
  lynx_url: str
  url: str
  link_type: str

class BiographyWithEntities(IBase):
  raw_text: str
  entities: List[Any]
class ClipsMusicAttributionInfo(IBase):
  artist_name: str
  song_name: str
  uses_original_audio: bool
  should_mute_audio: bool
  should_mute_audio_reason: str
  audio_id: str

class DashInfo(IBase):
  is_dash_eligible: bool
  video_dash_manifest: Optional[str] = None
  number_of_qualities: int

class Dimensions(IBase):
  height: int
  width: int

class EdgeFollowClass(IBase):
  count: int

class FluffyNode(IBase):
  text: str

class EdgeMediaToCaptionEdge(IBase):
  node: FluffyNode

class EdgeMediaToCaption(IBase):
  edges: List[EdgeMediaToCaptionEdge]

class NodeUser(IBase):
  full_name: str
  followed_by_viewer: bool
  id: str
  is_verified: bool
  profile_pic_url: str
  username: str

class TentacledNode(IBase):
  user: NodeUser
  x: float
  y: float

class EdgeMediaToTaggedUserEdge(IBase):
  node: TentacledNode

class EdgeMediaToTaggedUser(IBase):
  edges: List[EdgeMediaToTaggedUserEdge]

class Owner(IBase):
  id: int
  username: str

class SharingFrictionInfo(IBase):
  should_have_sharing_friction: bool
  bloks_app_url: Optional[str] = None

class StickyNode(IBase):
  typename: str = Field(alias='__typename')
  id: str
  shortcode: str
  dimensions: Dimensions
  display_url: str
  edge_media_to_tagged_user: EdgeMediaToTaggedUser
  fact_check_overall_rating: Optional[str] = None
  fact_check_information: Optional[str] = None
  gating_info: Optional[str] = None
  sharing_friction_info: SharingFrictionInfo
  media_overlay_info: Optional[str] = None
  media_preview: Optional[str] = None
  owner: Owner
  is_video: bool
  has_upcoming_event: bool
  accessibility_caption: Optional[str] = None
  dash_info: Optional[DashInfo] = None
  has_audio: Optional[bool] = None
  tracking_token: Optional[str] = None
  video_url: Optional[str] = None
  video_view_count: Optional[int] = None

class EdgeSidecarToChildrenEdge(IBase):
  node: StickyNode

class EdgeSidecarToChildren(IBase):
  edges: List[EdgeSidecarToChildrenEdge]

class Location(IBase):
  id: str
  has_public_page: bool
  name: str
  slug: str

class ThumbnailResource(IBase):
  src: str
  config_width: int
  config_height: int

class FelixProfileGridCrop(IBase):
  crop_left: float
  crop_right: float
  crop_top: float
  crop_bottom: float

class PurpleNode(IBase):
  typename: str = Field(alias='__typename')
  id: str
  shortcode: str
  dimensions: Dimensions
  display_url: str
  edge_media_to_tagged_user: EdgeMediaToTaggedUser
  fact_check_overall_rating: Optional[str] = None
  fact_check_information: Optional[str] = None
  gating_info: Optional[str] = None
  sharing_friction_info: SharingFrictionInfo
  media_overlay_info: Optional[str] = None
  media_preview: Optional[str] = None
  owner: Owner
  is_video: bool
  has_upcoming_event: bool
  accessibility_caption: Optional[str] = None
  dash_info: Optional[DashInfo] = None
  has_audio: Optional[bool] = None
  tracking_token: Optional[str] = None
  video_url: Optional[str] = None
  video_view_count: Optional[int] = None
  edge_media_to_caption: EdgeMediaToCaption
  edge_media_to_comment: EdgeFollowClass
  comments_disabled: bool
  taken_at_timestamp: int
  edge_liked_by: EdgeFollowClass
  edge_media_preview_like: EdgeFollowClass
  location: Optional[Location] = None
  nft_asset_info: Optional[str] = None
  thumbnail_src: str
  thumbnail_resources: List[ThumbnailResource]
  felix_profile_grid_crop: Optional[Union[str, FelixProfileGridCrop]] = None
  coauthor_producers: List[Any]
  pinned_for_users: List[Any]
  viewer_can_reshare: bool
  encoding_status: Optional[str] = None
  is_published: Optional[bool] = None
  product_type: Optional[str] = None
  title: Optional[str] = None
  video_duration: Optional[float] = None
  edge_sidecar_to_children: Optional[EdgeSidecarToChildren] = None
  clips_music_attribution_info: Optional[ClipsMusicAttributionInfo] = None

class EdgeFelixVideoTimelineEdge(IBase):
  node: PurpleNode

class PageInfo(IBase):
  has_next_page: bool
  end_cursor: Optional[str] = None

class EdgeFelixVideoTimelineClass(IBase):
  count: int
  page_info: PageInfo
  edges: List[EdgeFelixVideoTimelineEdge]

class IndigoNode(IBase):
  username: str

class EdgeMutualFollowedByEdge(IBase):
  node: IndigoNode

class EdgeMutualFollowedBy(IBase):
  count: int
  edges: List[EdgeMutualFollowedByEdge]

class FBProfileBioLink(IBase):
  url: str
  name: str

class DataUser(IBase):
  ai_agent_type: Optional[str] = None
  biography: str
  bio_links: List[BioLink]
  fb_profile_biolink: Optional[Union[str, FBProfileBioLink]] = None
  biography_with_entities: BiographyWithEntities
  blocked_by_viewer: bool
  restricted_by_viewer: Optional[bool] = None
  country_block: bool
  eimu_id: str
  external_url: Optional[str] = None
  external_url_linkshimmed: Optional[str] = None
  edge_followed_by: EdgeFollowClass
  fbid: str
  followed_by_viewer: bool
  edge_follow: EdgeFollowClass
  follows_viewer: bool
  full_name: str
  group_metadata: Optional[str] = None
  has_ar_effects: bool
  has_clips: bool
  has_guides: bool
  has_channel: bool
  has_blocked_viewer: bool
  highlight_reel_count: int
  has_requested_viewer: bool
  hide_like_and_view_counts: bool
  id: int
  is_business_account: bool
  is_professional_account: bool
  is_supervision_enabled: bool
  is_guardian_of_viewer: bool
  is_supervised_by_viewer: bool
  is_supervised_user: bool
  is_embeds_disabled: bool
  is_joined_recently: bool
  guardian_id: Optional[str] = None
  business_address_json: Optional[str] = None
  business_contact_method: str
  business_email: Optional[str] = None
  business_phone_number: Optional[str] = None
  business_category_name: Optional[str] = None
  overall_category_name: Optional[str] = None
  category_enum: Optional[str] = None
  category_name: Optional[str] = None
  is_private: bool
  is_verified: bool
  is_verified_by_mv4b: bool
  is_regulated_c18: bool
  edge_mutual_followed_by: EdgeMutualFollowedBy
  pinned_channels_list_count: int
  profile_pic_url: str
  profile_pic_url_hd: str
  requested_by_viewer: bool
  should_show_category: bool
  should_show_public_contacts: bool
  show_account_transparency_details: bool
  transparency_label: Optional[str] = None
  transparency_product: Optional[str] = None
  username: str
  connected_fb_page: Optional[str] = None
  pronouns: List[Any]
  edge_felix_video_timeline: Optional[EdgeFelixVideoTimelineClass] = None
  edge_owner_to_timeline_media: Optional[EdgeFelixVideoTimelineClass] = None
  edge_saved_media: Optional[EdgeFelixVideoTimelineClass] = None
  edge_media_collections: Optional[EdgeFelixVideoTimelineClass] = None

class Data(IBase):
  user: DataUser

class UserProfile(IBase):
  data: Data
  status: str
