from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['IdentityManagedOrg', 'ManagedOrgsResponse', 'PartnerAdminUser', 'PartneradminsfororgResponse']


class IdentityManagedOrg(ApiModel):
    #: The org ID of the managed org.
    #: example: Y2LZY29ZCGFYAZOVL3VZL1BFT1BMRS9MNWIZNJE4NY1JOGRKLTQ3MJCTOGIYZI1MOWM0NDDMMJKWNDY
    org_id: Optional[str] = None
    #: role ID of the user to this org.
    #: example: YXRSYXMTCG9YDGFSLNBHCNRUZXIUC2FSZXNMDWXSYWRTAW4=
    role: Optional[str] = None


class PartnerAdminUser(ApiModel):
    #: The user ID of the partner admin.
    #: example: Y2LZY29ZCGFYAZOVL3VZL1BFT1BMRS9JOTYWOTZIYI1KYTRHLTQ3NZETYTC2ZI1KNDEZODQWZWVM1TQ
    id: Optional[str] = None
    #: The display name of the partner admin.
    #: example: display name
    display_name: Optional[str] = None
    #: The first name of the partner admin.
    #: example: John
    first_name: Optional[str] = None
    #: The last name of the partner admin.
    #: example: Doe
    last_name: Optional[str] = None
    #: List of emails for the partner admin.
    #: example: ['johndoe@example.com']
    emails: Optional[list[str]] = None
    #: The role of this partner admin in the given customer org.
    #: example: id_full_admin
    role_in_customer_org: Optional[str] = None


class ManagedOrgsResponse(ApiModel):
    #: An array of managed orgs objects.
    items: Optional[list[IdentityManagedOrg]] = None


class PartneradminsfororgResponse(ApiModel):
    #: An array of partner admin user details.
    items: Optional[list[PartnerAdminUser]] = None


class PartnerAdministratorsApi(ApiChild, base='partner/organizations'):
    """
    Partner Administrators
    
    Partner organizations that manage their customers through Webex Partner Hub can leverage this API to assign or
    unassign partner administrator roles to their users, as well as assign or unassign customer organizations to
    specific partner administrators.
    Managing other partner administrators in an organization requires the partner full administrator role. The users
    being acted upon also exist in the partners own organization. To create a user, see `People API
    <https://developer.webex.com/docs/api/v1/people>`_. The authorizing
    admin must grant the spark-admin:organizations-read scope for read operations and spark-admin:organizations-write
    scope for write operations.
    """
    ...