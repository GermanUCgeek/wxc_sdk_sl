from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GroupResponse', 'GroupsCollectionResponse', 'Member', 'PatchGroup', 'PatchMemberWithOperation',
            'PostGroup', 'PostMember']


class Member(ApiModel):
    #: Person ID of the group member.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xOTUzOTdhMi03MTU5LTRjNTgtYTBiOC00NmQ2ZWZlZTdkMTM
    id: Optional[str] = None
    #: Member type.
    #: example: user
    type: Optional[str] = None
    #: example: Jane Smith
    display_name: Optional[str] = None


class PostMember(ApiModel):
    #: Person ID.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xOTUzOTdhMi03MTU5LTRjNTgtYTBiOC00NmQ2ZWZlZTdkMTM
    id: Optional[str] = None


class PatchMemberWithOperation(ApiModel):
    #: Person ID.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS8xOTUzOTdhMi03MTU5LTRjNTgtYTBiOC00NmQ2ZWZlZTdkMTM
    id: Optional[str] = None
    #: Operation type. The default operation is `add` if no operation is specified.
    #: example: add
    operation: Optional[str] = None


class PostGroup(ApiModel):
    #: The name of the group.
    #: example: Sales Group
    display_name: Optional[str] = None
    #: The ID of the organization to which this group belongs. If not specified, the organization ID from the OAuth
    #: token is used.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNDhhZGI4MS0yOGY5LTRhYjUtYjJkNi1lOWI0OTRlNzJhMDY
    org_id: Optional[str] = None
    #: Description of the group.
    #: example: Salas Group in San Jose
    description: Optional[str] = None
    #: An array of members. Maximum of 500 members can be provided. To add more members, use the `Update a Group
    #: <https://developer.webex.com/docs/api/v1/groups/update-a-group>`_ API to
    #: add additional members.
    members: Optional[list[PostMember]] = None


class PatchGroup(ApiModel):
    #: The name of the group.
    #: example: New Sales Group
    display_name: Optional[str] = None
    #: Description of the group.
    #: example: Sales Group in LA
    description: Optional[str] = None
    #: An array of members operations.
    members: Optional[list[PatchMemberWithOperation]] = None


class GroupResponse(ApiModel):
    #: A unique identifier for the group.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSU1fR1JPVVAvMjUxMDRiZTAtZjg3NC00MzQzLTk2MDctZGYwMmRmMzdiNWMxOjM0OGFkYjgxLTI4ZjktNGFiNS1iMmQ2LWU5YjQ5NGU3MmEwNg
    id: Optional[str] = None
    #: The name of the group.
    #: example: Sales Group
    display_name: Optional[str] = None
    #: The ID of the organization to which this group belongs.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi8zNDhhZGI4MS0yOGY5LTRhYjUtYjJkNi1lOWI0OTRlNzJhMDY
    org_id: Optional[str] = None
    #: The timestamp indicating creation date/time of group
    #: example: 2022-02-17T02:13:29.706Z
    created: Optional[datetime] = None
    #: The timestamp indicating lastModification time of group
    #: example: 2022-02-17T02:13:29.706Z
    last_modified: Optional[datetime] = None
    #: example: 1.0
    member_size: Optional[int] = None
    #: An array of members
    members: Optional[list[Member]] = None


class GroupsCollectionResponse(ApiModel):
    #: Total number of groups returned in the response.
    #: example: 3.0
    total_results: Optional[int] = None
    #: example: 1.0
    start_index: Optional[int] = None
    #: example: 10.0
    items_per_page: Optional[int] = None
    #: An array of group objects.
    groups: Optional[list[GroupResponse]] = None


class GroupsApi(ApiChild, base='groups'):
    """
    Groups
    
    Groups contain a collection of members in Webex. A member represents a Webex user. A group is used to assign
    templates and settings to the set of members contained in a group.  To create and manage a group, including adding
    and removing members from a group, an auth token containing the `identity:groups_rw` is required.  Searching and
    viewing members of a group requires an auth token with a scope of `identity:groups_read`.
    
    To learn more about managing people to use as members in the /groups API please refer to the `People API
    <https://developer.webex.com/docs/api/v1/people>`_.
    """
    ...