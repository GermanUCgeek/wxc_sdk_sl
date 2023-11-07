from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['CreateAPersonPhoneNumbers', 'CreateAPersonPhoneNumbersType', 'Person', 'PersonAddresses',
            'PersonCollectionResponse', 'PersonInvitePending', 'PersonPhoneNumbers', 'PersonPhoneNumbersType',
            'PersonStatus', 'PersonType']


class PersonPhoneNumbersType(str, Enum):
    #: Work phone number of the person.
    work = 'work'
    #: Work extension of the person. For the Webex Calling person, the value will have a routing prefix along with the
    #: extension.
    work_extension = 'work_extension'
    #: Mobile number of the person.
    mobile = 'mobile'
    #: FAX number of the person.
    fax = 'fax'


class PersonPhoneNumbers(ApiModel):
    #: The type of phone number.
    #: example: work
    type: Optional[PersonPhoneNumbersType] = None
    #: The phone number.
    #: example: +1 408 526 7209
    value: Optional[str] = None


class PersonAddresses(ApiModel):
    #: The type of address
    #: example: work
    type: Optional[str] = None
    #: The user's country
    #: example: US
    country: Optional[str] = None
    #: the user's locality, often city
    #: example: Milpitas
    locality: Optional[str] = None
    #: the user's region, often state
    #: example: California
    region: Optional[str] = None
    #: the user's street
    #: example: 1099 Bird Ave.
    street_address: Optional[str] = None
    #: the user's postal or zip code
    #: example: 99212
    postal_code: Optional[str] = None


class PersonStatus(str, Enum):
    #: Active within the last 10 minutes
    active = 'active'
    #: The user is in a call
    call = 'call'
    #: The user has manually set their status to "Do Not Disturb"
    do_not_disturb = 'DoNotDisturb'
    #: Last activity occurred more than 10 minutes ago
    inactive = 'inactive'
    #: The user is in a meeting
    meeting = 'meeting'
    #: The user or a Hybrid Calendar service has indicated that they are "Out of Office"
    out_of_office = 'OutOfOffice'
    #: The user has never logged in; a status cannot be determined
    pending = 'pending'
    #: The user is sharing content
    presenting = 'presenting'
    #: The user’s status could not be determined
    unknown = 'unknown'


class PersonInvitePending(str, Enum):
    #: The person has been invited to Webex but has not created an account
    true = 'true'
    #: An invite is not pending for this person
    false = 'false'


class PersonType(str, Enum):
    #: Account belongs to a person
    person = 'person'
    #: Account is a bot user
    bot = 'bot'
    #: Account is a `guest user
    #: <https://developer.webex.com/docs/guest-issuer>`_
    appuser = 'appuser'


class Person(ApiModel):
    #: A unique identifier for the person.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    id: Optional[str] = None
    #: The email addresses of the person.
    #: example: ['john.andersen@example.com']
    emails: Optional[list[str]] = None
    #: Phone numbers for the person.
    phone_numbers: Optional[list[PersonPhoneNumbers]] = None
    #: The Webex Calling extension for the person. Only applies to a person with a Webex Calling license
    #: example: 133
    extension: Optional[datetime] = None
    #: The ID of the location for this person retrieved from BroadCloud.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OLzYzNzE1
    location_id: Optional[str] = None
    #: The full name of the person.
    #: example: John Andersen
    display_name: Optional[str] = None
    #: The nickname of the person if configured. If no nickname is configured for the person, this field will not be
    #: present.
    #: example: John
    nick_name: Optional[str] = None
    #: The first name of the person.
    #: example: John
    first_name: Optional[str] = None
    #: The last name of the person.
    #: example: Andersen
    last_name: Optional[str] = None
    #: The URL to the person's avatar in PNG format.
    #: example: https://1efa7a94ed21783e352-c62266528714497a17239ececf39e9e2.ssl.cf1.rackcdn.com/V1~54c844c89e678e5a7b16a306bc2897b9~wx29yGtlTpilEFlYzqPKag==~1600
    avatar: Optional[str] = None
    #: The ID of the organization to which this person belongs.
    #: example: Y2lzY29zcGFyazovL3VzL09SR0FOSVpBVElPTi85NmFiYzJhYS0zZGNjLTExZTUtYTE1Mi1mZTM0ODE5Y2RjOWE
    org_id: Optional[str] = None
    #: An array of role strings representing the roles to which this admin user belongs.
    #: example: ['Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh', 'Y2lzY29zcGFyazovL3VzL1JPTEUvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi']
    roles: Optional[list[str]] = None
    #: An array of license strings allocated to this person.
    #: example: ['Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWExNTItZmUzNDgxOWNkYzlh', 'Y2lzY29zcGFyazovL3VzL0xJQ0VOU0UvOTZhYmMyYWEtM2RjYy0xMWU1LWIyNjMtMGY0NTkyYWRlZmFi']
    licenses: Optional[list[str]] = None
    #: The business department the user belongs to.
    #: example: Sales
    department: Optional[str] = None
    #: A manager identifier
    #: example: John Duarte
    manager: Optional[str] = None
    #: Person Id of the manager
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS80ZGEzYTI0OC05YjBhLTQxMDgtODU0NC1iNTQwMzEyZTU2M2E
    manager_id: Optional[str] = None
    #: the person's title
    #: example: GM
    title: Optional[str] = None
    #: Person's address
    addresses: Optional[list[PersonAddresses]] = None
    #: The date and time the person was created.
    #: example: 2015-10-18T14:26:16.000Z
    created: Optional[datetime] = None
    #: The date and time the person was last changed.
    #: example: 2015-10-18T14:26:16.000Z
    last_modified: Optional[datetime] = None
    #: The time zone of the person if configured. If no timezone is configured on the account, this field will not be
    #: present
    #: example: America/Denver
    timezone: Optional[str] = None
    #: The date and time of the person's last activity within Webex. This will only be returned for people within your
    #: organization or an organization you manage. Presence information will not be shown if the authenticated user
    #: has `disabled status sharing
    #: <https://help.webex.com/nkzs6wl/>`_.
    #: example: 2015-10-18T14:26:16.028Z
    last_activity: Optional[datetime] = None
    #: One or several site names where this user has a role (host or attendee)
    #: example: ['mysite.webex.com#attendee']
    site_urls: Optional[list[str]] = None
    #: The users sip addresses. Read-only.
    #: example: ['{"type": "personal-room","value": "testuser5@mycompany.webex.com","primary": false}']
    sip_addresses: Optional[list[str]] = None
    #: Identifier for intra-domain federation with other XMPP based messenger systems.
    #: example: user@example.com
    xmpp_federation_jid: Optional[str] = None
    #: The current presence status of the person. This will only be returned for people within your organization or an
    #: organization you manage. Presence information will not be shown if the authenticated user has
    #: `disabled status sharing
    #: <https://help.webex.com/nkzs6wl/>`_.
    #: example: active
    status: Optional[PersonStatus] = None
    #: Whether or not an invite is pending for the user to complete account activation. This property is only returned
    #: if the authenticated user is an admin user for the person's organization.
    #: example: false
    invite_pending: Optional[PersonInvitePending] = None
    #: Whether or not the user is allowed to use Webex. This property is only returned if the authenticated user is an
    #: admin user for the person's organization.
    #: example: true
    login_enabled: Optional[PersonInvitePending] = None
    #: The type of person account, such as person or bot.
    #: example: person
    type: Optional[PersonType] = None


class PersonCollectionResponse(ApiModel):
    #: An array of person objects.
    items: Optional[list[Person]] = None
    #: An array of person IDs that could not be found.
    not_found_ids: Optional[list[str]] = None


class CreateAPersonPhoneNumbersType(str, Enum):
    work = 'work'


class CreateAPersonPhoneNumbers(ApiModel):
    #: The type of phone number.
    #: example: work
    type: Optional[CreateAPersonPhoneNumbersType] = None
    #: The phone number.
    #: example: 408 526 7209
    value: Optional[str] = None


class PeopleApi(ApiChild, base='people'):
    """
    People
    
    People are registered users of Webex. Searching and viewing People requires an auth token with a `scope
    <https://developer.webex.com/docs/integrations#scopes>`_ of
    `spark:people_read`. Viewing the list of all People in your Organization requires an administrator auth token with
    `spark-admin:people_read` scope. Adding, updating, and removing People requires an administrator auth token with
    the `spark-admin:people_write` and `spark-admin:people_read` scope.
    
    A person's call settings are for `Webex Calling` and necessitate Webex Calling licenses.
    
    To learn more about managing people in a room see the `Memberships API
    <https://developer.webex.com/docs/api/v1/memberships>`_. For information about how to allocate Hybrid
    Services licenses to people, see the `Managing Hybrid Services
    <https://developer.webex.com/docs/api/guides/managing-hybrid-services-licenses>`_ guide.
    """
    ...