from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['ECMFolder', 'ECMFolderCollectionResponse', 'ECMFolderRoomType']


class ECMFolderRoomType(str, Enum):
    #: 1:1 room
    direct = 'direct'
    #: group room
    group = 'group'


class ECMFolder(ApiModel):
    #: A unique identifier for the folder.
    #: example: Y2lzY29zcGFyazovL3VybjpURUFNOnVzLWVhc3QtMl9hL1RBQlMvZDg1ZTYwNj
    id: Optional[str] = None
    #: A unique identifier for the room to which the folder should be linked to.
    #: example: Y2lzY29zcGFyazovL3VzL1JPT00vYmJjZWIxYWQtNDNmMS0zYjU4LTkxNDctZjE0YmIwYzRkMTU0
    room_id: Optional[str] = None
    #: The room type.
    #: example: group
    room_type: Optional[ECMFolderRoomType] = None
    #: Sharepoint or OneDrive drive id. It can be queried via MS Graph APIs.
    #: example: 123
    drive_id: Optional[datetime] = None
    #: Sharepoint or OneDrive item id. It can be queried via MS Graph APIs.
    #: example: 456
    item_id: Optional[datetime] = None
    #: Indicates if this is the default content storage for the room.
    #: example: false
    default_folder: Optional[str] = None
    #: This should match the folder name in the ECM backend.
    #: example: OneDrive folder for shared documents
    display_name: Optional[str] = None
    #: Folder's content URL.
    #: example: https://cisco-my.sharepoint.com/personal/naalluri/123
    content_url: Optional[str] = None
    #: The person ID of the person who created this folder link.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    creator_id: Optional[str] = None
    #: The date and time when the folder link was created.
    #: example: 2015-10-18T14:26:16.203Z
    created: Optional[datetime] = None


class ECMFolderCollectionResponse(ApiModel):
    items: Optional[list[ECMFolder]] = None


class ECMFolderLinkingApi(ApiChild, base='room/linkedFolders'):
    """
    ECM folder linking
    
    Enterprise Content Management folder-linking in Webex is how users configure existing OneDrive and SharePoint
    online folders as the (default or reference) storage backend for spaces. This configuration can be done in our
    native clients and via API.
    A space participant will be able to configure an ECM folder for a space. Only one ECM folder per space and only
    OneDrive and SharePoint online are currently supported.
    """
    ...