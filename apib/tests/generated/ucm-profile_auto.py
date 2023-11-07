from datetime import datetime
from typing import Optional

from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['GetManagerProfileObject', 'ReadTheListOfUcManagerProfilesResponse']


class GetManagerProfileObject(ApiModel):
    #: A unique identifier for the calling UC Manager Profile.
    #: example: Y2lzY29zcGFyazovL3VzL0NBTExJTkdfUFJPRklMRS9iMzdmMmZiYS0yZTdjLTExZWItYTM2OC1kYmU0Yjc2NzFmZTk
    id: Optional[str] = None
    #: Unique name for the calling UC Manager Profile.
    #: example: UC Profile2
    name: Optional[str] = None


class ReadTheListOfUcManagerProfilesResponse(ApiModel):
    #: Array of manager profiles.
    calling_profiles: Optional[list[GetManagerProfileObject]] = None


class UCMProfileApi(ApiChild, base='telephony/config/callingProfiles'):
    """
    UCM Profile
    
    Not supported for Webex for Government (FedRAMP)
    
    
    
    UCM Profiles supports reading and writing of UC Profile relatedsettings for a specific organization or person.
    
    Viewing these read-only organization settings requires a full or read-only administrator auth token with a scope of
    `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    Viewing people settings requires a full, user, or read-only administrator auth token with a scope of
    `spark-admin:people_read` or, for select APIs, a user auth token with `spark:people_read` scope can be used by a
    person to read their own settings.
    
    Configuring people settings requires a full or user administrator auth token with the `spark-admin:people_write`
    scope or, for select APIs, a user auth token with `spark:people_write` scope can be used by a person to update
    their own settings.
    
    A partner administrator can retrieve or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """
    ...