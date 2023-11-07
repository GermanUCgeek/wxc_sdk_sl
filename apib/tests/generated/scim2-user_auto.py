from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['EmailObject', 'EmailObjectType', 'GetUserResponse',
            'GetUserResponseUrnietfparamsscimschemasextensionenterprise20User', 'ManagedGroupObject',
            'ManagedOrgsObject', 'ManagedSitesObject', 'ManagerResponseObject', 'NameObject', 'PatchUser',
            'PatchUserOperations', 'PatchUserOperationsOp', 'PhotoObject', 'PhotoObjectType', 'PostUser',
            'PostUserUrnietfparamsscimschemasextensionenterprise20User',
            'PostUserUrnietfparamsscimschemasextensionenterprise20UserManager',
            'PostUserUrnscimschemasextensionciscowebexidentity20User', 'PutUser', 'PutUserAddresses',
            'PutUserPhoneNumbers', 'PutUserPhoneNumbersType', 'RoleObject', 'RoleObjectType', 'SearchUserResponse',
            'SipAddressObject', 'SipAddressObjectType', 'UserTypeObject']


class PatchUserOperationsOp(str, Enum):
    add = 'add'
    replace = 'replace'
    remove = 'remove'


class PatchUserOperations(ApiModel):
    #: The operation to perform.
    #: example: add
    op: Optional[PatchUserOperationsOp] = None
    #: A string containing an attribute path describing the target of the operation.
    #: example: displayName
    path: Optional[str] = None
    #: New value.
    #: example: new displayName value
    value: Optional[str] = None


class PatchUser(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:api:messages:2.0:PatchOp']
    schemas: Optional[list[str]] = None
    #: A list of patch operations.
    operations: Optional[list[PatchUserOperations]] = Field(alias='Operations', default=None)


class PostUserUrnietfparamsscimschemasextensionenterprise20UserManager(ApiModel):
    #: Webex Identity assigned user identifier of the user's manager. The manager must be in the same org as the user.
    #: example: b5717a4a-0169-43b2-ac3c-db20ba4e72cd
    value: Optional[str] = None


class PostUserUrnietfparamsscimschemasextensionenterprise20User(ApiModel):
    #: Identifies the name of a cost center.
    #: example: costCenter 123
    cost_center: Optional[str] = None
    #: Identifies the name of an organization.
    #: example: Cisco webexidentity
    organization: Optional[str] = None
    #: Identifies the name of a division.
    #: example: division 456
    division: Optional[str] = None
    #: Identifies the name of a department.
    #: example: department 789
    department: Optional[str] = None
    #: Numeric or alphanumeric identifier assigned to a person, typically based on order of hire or association with an
    #: organization.
    #: example: 518-8888-888
    employee_number: Optional[str] = None
    #: The user's manager.
    manager: Optional[PostUserUrnietfparamsscimschemasextensionenterprise20UserManager] = None


class SipAddressObjectType(str, Enum):
    enterprise = 'enterprise'


class SipAddressObject(ApiModel):
    #: The sip address value.
    #: example: sipAddress value1
    value: Optional[str] = None
    #: The type of the sipAddress.
    #: example: enterprise
    type: Optional[SipAddressObjectType] = None
    #: A human-readable description, primarily used for display purposes.
    #: example: sipAddress1 description
    display: Optional[str] = None
    #: Designate the primary sipAddress.
    #: example: True
    primary: Optional[bool] = None


class ManagedOrgsObject(ApiModel):
    #: Webex Identity assigned organization identifier.
    #: example: 75fe2995-24f5-4831-8d2c-1c2f8255912e
    org_id: Optional[str] = None
    #: Role in the target organization for the user.
    #: example: id_full_admin
    role: Optional[str] = None


class ManagedGroupObject(ApiModel):
    #: Webex Identity assigned organization identifier.
    #: example: 153ced48-d2d1-4369-86fd-9b9fade218ff
    org_id: Optional[str] = None
    #: A unique identifier for the group.
    #: example: 1929effd-b750-43d6-be0d-7dcdaac38e92
    group_id: Optional[str] = None
    #: Role in the target organization for the user.
    #: example: location_full_admin
    role: Optional[str] = None


class ManagedSitesObject(ApiModel):
    #: Managed site name.
    #: example: admintrainSiteName1.webex.com
    site_name: Optional[str] = None
    #: Role in the managed site for the user.
    #: example: full_admin
    role: Optional[str] = None


class PostUserUrnscimschemasextensionciscowebexidentity20User(ApiModel):
    #: Account status of the user.
    #: example: ['element='string' content='active' attributes={'typeAttributes': ApibArray(element='array', content=[ApibString(element='string', content='fixed', attributes=None, meta=None)], attributes=None, meta=None)} meta=None']
    account_status: Optional[list[str]] = None
    #: sipAddress values for the user.
    sip_addresses: Optional[list[SipAddressObject]] = None
    #: Organizations that the user can manage.
    managed_orgs: Optional[list[ManagedOrgsObject]] = None
    #: Groups that the user can manage.
    managed_groups: Optional[list[ManagedGroupObject]] = None
    #: Sites that the user can manage.
    managed_sites: Optional[list[ManagedSitesObject]] = None


class UserTypeObject(str, Enum):
    user = 'user'
    room = 'room'
    external_calling = 'external_calling'
    calling_service = 'calling_service'


class NameObject(ApiModel):
    #: The given name of the user, or first name in most Western languages (e.g., "Sarah" given the full name "Ms.
    #: Sarah J Henderson, III").
    #: example: Sarah
    given_name: Optional[str] = None
    #: The family name of the user, or last name in most Western languages (e.g., "Henderson" given the full name "Ms.
    #: Sarah J Henderson, III").
    #: example: Henderson
    family_name: Optional[str] = None
    #: The middle name(s) of the user (e.g., "Jane" given the full name "Ms. Sarah J Henderson, III").
    #: example: Jane
    middle_name: Optional[str] = None
    #: The honorific prefix(es) of the user, or title in most Western languages (e.g., "Ms." given the full name "Ms.
    #: Sarah J Henderson, III").
    #: example: Mr.
    honorific_prefix: Optional[str] = None
    #: The honorific suffix(es) of the user, or suffix in most Western languages (e.g., "III" given the full name "Ms.
    #: Sarah J Henderson, III").
    #: example: III
    honorific_suffix: Optional[str] = None


class PutUserPhoneNumbersType(str, Enum):
    work = 'work'
    home = 'home'
    mobile = 'mobile'
    work_extension = 'work_extension'
    fax = 'fax'
    pager = 'pager'
    other = 'other'


class PutUserPhoneNumbers(ApiModel):
    #: phone number.
    #: example: 400 123 1234
    value: Optional[str] = None
    #: We support the following types of phone numbers: 'mobile', 'work', 'fax', 'work_extension', 'alternate1',
    #: 'alternate2'.  Alternate 1 and Alternate 2 are types inherited from Webex meeting sites.
    #: example: work
    type: Optional[PutUserPhoneNumbersType] = None
    #: A human-readable name, primarily used for display purposes.
    #: example: work phone number
    display: Optional[str] = None
    #: A Boolean value indicating the phone number premary status.
    #: example: True
    primary: Optional[bool] = None


class PhotoObjectType(str, Enum):
    photo = 'photo'
    thumbnail = 'thumbnail'
    resizable = 'resizable'


class PhotoObject(ApiModel):
    #: photo link.
    #: example: https://photos.example.com/profilephoto/72930000000Ccne/F
    value: Optional[str] = None
    #: The type of the photo
    #: example: photo
    type: Optional[PhotoObjectType] = None
    #: A human-readable description, primarily used for display purposes.
    #: example: photo description
    display: Optional[str] = None
    #: A Boolean value indicating the photo usage status.
    #: example: True
    primary: Optional[bool] = None


class PutUserAddresses(ApiModel):
    #: address type
    #: example: work
    type: Optional[str] = None
    #: The full street address component, which may include house number, street name, P.O. box, and multi-line
    #: extended street address information. This attribute MAY contain newlines.
    #: example: 100 Universal City Plaza
    street_address: Optional[str] = None
    #: The city or locality component.
    #: example: Hollywood
    locality: Optional[str] = None
    #: The state or region component.
    #: example: CA
    region: Optional[str] = None
    #: The zip code or postal code component.
    #: example: 91608
    postal_code: Optional[str] = None
    #: The country name component.
    #: example: US
    country: Optional[str] = None


class EmailObjectType(str, Enum):
    work = 'work'
    home = 'home'
    room = 'room'
    other = 'other'


class EmailObject(ApiModel):
    #: The email address.
    #: example: user1@example.home.com
    value: Optional[str] = None
    #: The type of the email.
    #: example: home
    type: Optional[EmailObjectType] = None
    #: A human-readable description, primarily used for display purposes.
    #: example: home email description
    display: Optional[str] = None
    #: A Boolean value indicating the email status. If the type is work and primary is true, the value must equal
    #: "userName".
    primary: Optional[bool] = None


class PostUser(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:schemas:core:2.0:User', 'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', 'urn:scim:schemas:extension:cisco:webexidentity:2.0:User']
    schemas: Optional[list[str]] = None
    #: A unique identifier for the user and is used to authenticate the user in Webex.  This attribute must be set to
    #: the user's primary email address.  No other user in Webex may have the same userName value and thus this value
    #: is required to be unique within Webex.
    #: example: user1@example.com
    user_name: Optional[str] = None
    #: The type of the user.
    #: example: user
    user_type: Optional[UserTypeObject] = None
    #: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant", "Engineer" etc.
    #: example: Sales manager
    title: Optional[str] = None
    #: A boolean value of "true" or "false" indicating whether the user is active in Webex.
    #: example: True
    active: Optional[bool] = None
    #: Indicates the user's preferred language.  Acceptable values for this field are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: with the 2 letter language code followed by an _ and then the 2 letter country code.  Examples are:
    #: en_US : for english spoken in the United Statesfr_FR: for french spoken in France.
    #: example: en_US
    preferred_language: Optional[str] = None
    #: The user's locale which is used to represent the user's currency, time format, and numerical representations.
    #: Acceptable values for this field are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: followed by an _ and then the 2 letter country code.  Examples are:
    #: en_US : for English spoken in the United States or fr_FR: for French spoken in France.
    #: example: en_US
    locale: Optional[str] = None
    #: The user's time zone specified in the `IANA timezone
    #: <https://nodatime.org/timezones>`_ timezone format, for example, "America/Los_Angeles".
    #: example: America/Los_Angeles
    timezone: Optional[str] = None
    #: A fully qualified URL pointing to a page representing the user's online profile.
    #: example: https://jojowiki.com/Jonathan_Joestar
    profile_url: Optional[str] = None
    #: External identity.
    #: example: externalIdValue
    external_id: Optional[str] = None
    #: The value to display or show the user's name in Webex.
    #: example: Mr. Jonathan Jane Joestar, III
    display_name: Optional[str] = None
    #: A casual name of the user.  The value Bob when the user's formal name is Robert.
    #: example: JoJo
    nick_name: Optional[str] = None
    #: The components of the user's real name.
    name: Optional[NameObject] = None
    #: A list of user's phone numbers with an indicator of primary to specify the user's main number.
    phone_numbers: Optional[list[PutUserPhoneNumbers]] = None
    #: A list of photos for the user that represent a thing the user has.
    photos: Optional[list[PhotoObject]] = None
    #: User's physical mailing address.
    addresses: Optional[list[PutUserAddresses]] = None
    #: A list of the user's email addresses with an indicator of the user's primary email address.  The primary email
    #: address must be the same value as the user's userName.
    emails: Optional[list[EmailObject]] = None
    #: SCIM2 enterprise extension
    urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: Optional[PostUserUrnietfparamsscimschemasextensionenterprise20User] = Field(alias='urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', default=None)
    #: The Cisco extension of SCIM 2.
    urn_scim_schemas_extension_cisco_webexidentity_2_0_user: Optional[PostUserUrnscimschemasextensionciscowebexidentity20User] = Field(alias='urn:scim:schemas:extension:cisco:webexidentity:2.0:User', default=None)


class PutUser(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:schemas:core:2.0:User', 'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', 'urn:scim:schemas:extension:cisco:webexidentity:2.0:User']
    schemas: Optional[list[str]] = None
    #: A unique identifier for the user and is used to authenticate the user in Webex.  This attribute must be set to
    #: the user's primary email address.  No other user in Webex may have the same userName value and thus this value
    #: is required to b unique within Webex.
    #: example: user1Changed@example.com
    user_name: Optional[str] = None
    #: The type of the user.
    #: example: user
    user_type: Optional[UserTypeObject] = None
    #: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant", "Engineer" etc.
    #: example: Sales manager
    title: Optional[str] = None
    #: A boolean value of "true" or "false" indicating whether the user is active in Webex.
    #: example: True
    active: Optional[bool] = None
    #: Indicates the user's preferred language.  Acceptable values for this field are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: with the 2 letter language code followed by an _ and then the 2 letter country code.  Examples are:
    #: en_US : for english spoken in the United States, fr_FR: for french spoken in France.
    #: example: en_US
    preferred_language: Optional[str] = None
    #: The user's locale which is used to represent the user's currency, time format, and numerical representations.
    #: Acceptable values for this field are based on the  `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: followed by an _ and then the 2 letter country code.  Examples are:
    #: en_US : for English spoken in the United States, or fr_FR: for French spoken in France.
    #: example: en_US
    locale: Optional[str] = None
    #: The user's time zone specified in the `IANA timezone
    #: <https://nodatime.org/timezones>`_ timezone format. e.g: "America/Los_Angeles".
    #: example: America/Los_Angeles
    timezone: Optional[str] = None
    #: A fully qualified URL pointing to a page representing the user's online profile.
    #: example: https://jojowiki.com/Jonathan_Joestar
    profile_url: Optional[str] = None
    #: External identity.
    #: example: externalIdNewValue
    external_id: Optional[str] = None
    #: The value to display or show the user's name in Webex.
    #: example: Mr. Jonathan Jane Joestar, III
    display_name: Optional[str] = None
    #: A casual name of the user.  The value Bob when the user's formal name is Robert.
    #: example: JoJo
    nick_name: Optional[str] = None
    #: A list of user's phone numbers with an indicator of primary to specify the users main number.
    phone_numbers: Optional[list[PutUserPhoneNumbers]] = None
    #: A list of photos for the user that represent a thing the user has.
    photos: Optional[list[PhotoObject]] = None
    #: A physical mailing address of user.
    addresses: Optional[list[PutUserAddresses]] = None
    #: A list of the user's email addresses with an indicator of the user's primary email address.  The primary email
    #: address must be the same value as the user's userName.
    emails: Optional[list[EmailObject]] = None
    #: SCIM2 enterprise extention
    urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: Optional[PostUserUrnietfparamsscimschemasextensionenterprise20User] = Field(alias='urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', default=None)
    #: cisco extention of SCIM 2
    urn_scim_schemas_extension_cisco_webexidentity_2_0_user: Optional[PostUserUrnscimschemasextensionciscowebexidentity20User] = Field(alias='urn:scim:schemas:extension:cisco:webexidentity:2.0:User', default=None)


class ManagerResponseObject(ApiModel):
    #: Webex Identity assigned user identifier of the user's manager. The manager must be in the same org as the user.
    #: example: b5717a4a-0169-43b2-ac3c-db20ba4e72cd
    value: Optional[str] = None
    #: The value to display or show the manager's name in Webex.
    #: example: Identity Administrator
    display_name: Optional[str] = None
    #: The URI corresponding to a SCIM user that is the manager.
    #: example: http://integration.webexapis.com/identity/scim/0ae87ade-8c8a-4952-af08-318798958d0c/v2/Users/b5717a4a-0169-43b2-ac3c-db20ba4e72cd
    _ref: Optional[str] = Field(alias='$ref', default=None)


class GetUserResponseUrnietfparamsscimschemasextensionenterprise20User(ApiModel):
    #: Identifies the name of a cost center.
    #: example: costCenter 123
    cost_center: Optional[str] = None
    #: Identifies the name of an organization.
    #: example: Cisco webexidentity
    organization: Optional[str] = None
    #: Identifies the name of a division.
    #: example: division 456
    division: Optional[str] = None
    #: Identifies the name of a department.
    #: example: department 789
    department: Optional[str] = None
    #: Numeric or alphanumeric identifier assigned to a person, typically based on order of hire or association with an
    #: organization.
    #: example: 518-8888-888
    employee_number: Optional[str] = None
    #: The user's manager.
    manager: Optional[ManagerResponseObject] = None


class GetUserResponse(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:schemas:core:2.0:User', 'urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', 'urn:scim:schemas:extension:cisco:webexidentity:2.0:User']
    schemas: Optional[list[str]] = None
    #: Webex Identity assigned user identifier.
    #: example: 3426a8e3-d414-4bf0-a493-4f6787632a13
    id: Optional[str] = None
    #: A unique identifier for the user and is used to authenticate the user in Webex.  This attribute must be set to
    #: the user's primary email address.  No other user in Webex may have the same userName value and thus this value
    #: is required to be unique within Webex.
    #: example: user1@example.com
    user_name: Optional[str] = None
    #: A boolean value of "true" or "false" indicating whether the user is active in Webex.
    #: example: True
    active: Optional[bool] = None
    #: The components of the user's real name.
    name: Optional[NameObject] = None
    #: The value to display or show the user's name in Webex.
    #: example: Mr. Jonathan Jane Joestar, III
    display_name: Optional[str] = None
    #: A casual name of the user.  The value Bob when the user's formal name is Robert.
    #: example: JoJo
    nick_name: Optional[str] = None
    #: A list of the user's email addresses with an indicator of the user's primary email address.  The primary email
    #: address must be the same value as the user's userName.
    emails: Optional[list[EmailObject]] = None
    #: The type of the user.
    #: example: user
    user_type: Optional[UserTypeObject] = None
    #: A fully qualified URL pointing to a page representing the user's online profile.
    #: example: https://jojowiki.com/Jonathan_Joestar
    profile_url: Optional[str] = None
    #: The user's business title.  Examples of a title is "Business Manager". "Senior Accountant", "Engineer" etc.
    #: example: Sales manager
    title: Optional[str] = None
    #: Indicates the user's preferred language.  Acceptable values for this field are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: with the 2 letter language code followed by an _ and then the 2 letter country code.  Examples are:
    #: en_US : for english spoken in the United Statesfr_FR: for french spoken in France.
    #: example: en_US
    preferred_language: Optional[str] = None
    #: The user's locale which is used to represent the user's currency, time format, and numerical representations.
    #: Acceptable values for this field are based on the `ISO-696
    #: <http://www.loc.gov/standards/iso639-2/php/code_list.php>`_ and `ISO-3166
    #: followed by an _ and then the 2 letter country code.  Examples are:
    #: en_US : for English spoken in the United States or fr_FR: for French spoken in France.
    #: example: en_US
    locale: Optional[str] = None
    #: External identity.
    #: example: externalIdValue
    external_id: Optional[str] = None
    #: The user's time zone specified in the `IANA timezone
    #: <https://nodatime.org/timezones>`_ timezone format, for example, "America/Los_Angeles".
    #: example: America/Los_Angeles
    timezone: Optional[str] = None
    #: A list of user's phone numbers with an indicator of primary to specify the user's main number.
    phone_numbers: Optional[list[PutUserPhoneNumbers]] = None
    #: A list of photos for the user that represent a thing the user has.
    photos: Optional[list[PhotoObject]] = None
    #: User's physical mailing address.
    addresses: Optional[list[PutUserAddresses]] = None
    #: SCIM2 enterprise extension
    urn_ietf_params_scim_schemas_extension_enterprise_2_0_user: Optional[GetUserResponseUrnietfparamsscimschemasextensionenterprise20User] = Field(alias='urn:ietf:params:scim:schemas:extension:enterprise:2.0:User', default=None)
    #: The Cisco extension of SCIM 2.
    urn_scim_schemas_extension_cisco_webexidentity_2_0_user: Optional[PostUserUrnscimschemasextensionciscowebexidentity20User] = Field(alias='urn:scim:schemas:extension:cisco:webexidentity:2.0:User', default=None)


class RoleObjectType(str, Enum):
    #: Webex Identity roles: "id_full_admin", "id_user_admin", "id_readonly_admin", "id_device_admin".
    cirole = 'cirole'
    #: service registered role.
    servicerole = 'servicerole'


class RoleObject(ApiModel):
    #: The role value.
    #: example: id_full_admin
    value: Optional[str] = None
    #: The type of the role.
    #: example: cirole
    type: Optional[RoleObjectType] = None
    #: A human-readable description, primarily used for display purposes.
    #: example: role description
    display: Optional[str] = None


class SearchUserResponse(ApiModel):
    #: Input JSON schemas.
    #: example: ['urn:ietf:params:scim:api:messages:2.0:ListResponse']
    schemas: Optional[list[str]] = None
    #: Total number of users in search results.
    #: example: 2.0
    total_results: Optional[int] = None
    #: The total number of items in a paged result.
    #: example: 2.0
    items_per_page: Optional[int] = None
    #: Start at the one-based offset in the list of matching users.
    #: example: 1.0
    start_index: Optional[int] = None
    #: A list of users with details.
    resources: Optional[list[GetUserResponse]] = Field(alias='Resources', default=None)


class SCIM2UsersApi(ApiChild, base='identity/scim/{orgId}/v2/Users'):
    """
    SCIM 2 Users
    
    Implementation of the SCIM 2.0 user part for user management in a standards based manner. Please also see the
    `SCIM Specification
    <http://www.simplecloud.info/>`_. The schema and API design follows the standard SCIM 2.0 definition with detailed in
    `SCIM 2.0 schema
    <https://datatracker.ietf.org/doc/html/rfc7643>`_ and `SCIM 2.0 Protocol
    """
    ...