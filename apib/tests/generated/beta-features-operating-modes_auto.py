from collections.abc import Generator
from datetime import datetime
from json import loads
from typing import Optional, Union, Any

from dateutil.parser import isoparse
from pydantic import Field, TypeAdapter

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str, enum_str
from wxc_sdk.base import SafeEnum as Enum


__all__ = ['BetaFeaturesScheduleBasedRoutingWithOperatingModesApi', 'LocationObject', 'MonthObject',
           'OperatingModeCallForwarding', 'OperatingModeDayScheduleObject',
           'OperatingModeDifferentHoursDailyScheduleObject', 'OperatingModeGetObject',
           'OperatingModeHolidayGetObject', 'OperatingModeHolidayObject', 'OperatingModeListGetObject',
           'OperatingModeRecurrenceObject', 'OperatingModeSameHoursDailyScheduleObject',
           'OperatingModeScheduleTypeObject', 'OrgLocLevelObject', 'RecurYearlyByDateObject',
           'RecurYearlyByDayObject', 'RecurYearlyByDayObjectDay', 'RecurYearlyByDayObjectWeek']


class OperatingModeScheduleTypeObject(str, Enum):
    #: Specifies the `operating mode` is active during the same hours daily (i.e., same schedule for Monday to Friday,
    #: and Saturday to Sunday).
    same_hours_daily = 'SAME_HOURS_DAILY'
    #: Specifies the `operating mode` is active during different hours for different days of the week.
    different_hours_daily = 'DIFFERENT_HOURS_DAILY'
    #: Specifies the `operating mode` is active during holidays with their own days, and recurrence.
    holiday = 'HOLIDAY'
    #: Specifies the `operating mode` doesn't have any schedules defined.
    none_ = 'NONE'


class OrgLocLevelObject(str, Enum):
    #: Specifies this `operating mode` is configured across the organization.
    organization = 'ORGANIZATION'
    #: Specifies this `operating mode` is configured across a location.
    location = 'LOCATION'


class LocationObject(ApiModel):
    #: Unique identifier of the location.
    #: example: Y2lzY29zcGFyazovL3VzL0xPQ0FUSU9OL2E4Mjg5NzIyLTFiODAtNDFiNy05Njc4LTBlNzdhZThjMTA5OA
    id: Optional[str] = None
    #: Name of the location.
    #: example: Cisco-HQ
    name: Optional[str] = None


class OperatingModeCallForwarding(ApiModel):
    #: Call forwarding is enabled, or disabled. `False` if the flag is not set.
    #: example: True
    enabled: Optional[bool] = None
    #: The destination for forwarding.
    #: example: +19705550006
    destination: Optional[str] = None
    #: The destination voicemail enabled. `False` if the flag is not set.
    destination_voicemail_enabled: Optional[bool] = None


class OperatingModeListGetObject(ApiModel):
    #: A unique identifier for the `operating mode`.
    #: example: Y2lzY29zcGFyazovL3VzL09QRVJBVElOR19NT0RFL2JiOTc1OTcxLTBjZWYtNDdhNi05Yzc5LTliZWFjY2IwYjg4Mg
    id: Optional[str] = None
    #: Unique name for the `operating mode`.
    #: example: Day Operating Mode
    name: Optional[str] = None
    #: Defines the scheduling of the `operating mode`.
    #: example: SAME_HOURS_DAILY
    type: Optional[OperatingModeScheduleTypeObject] = None
    #: Level at which the `operating mode` would be defined.
    #: example: LOCATION
    level: Optional[OrgLocLevelObject] = None
    #: Location object having a unique identifier for the location, and its name. Mandatory if level is `LOCATION`.
    location: Optional[LocationObject] = None
    #: Call forwarding settings for an `operating mode`.
    call_forwarding: Optional[OperatingModeCallForwarding] = None


class OperatingModeDayScheduleObject(ApiModel):
    #: Specifies if the `operating mode` schedule for the specified weekday(s) is enabled, or not. `False` if the flag
    #: is not set.
    #: example: True
    enabled: Optional[bool] = None
    #: Specifies if the `operating mode` is enabled for the entire day. `False` if the flag is not set.
    all_day_enabled: Optional[bool] = None
    #: Start time for the `operating mode`.
    #: example: 09:00
    start_time: Optional[datetime] = None
    #: End time for the `operating mode`.
    #: example: 17:00
    end_time: Optional[datetime] = None


class OperatingModeSameHoursDailyScheduleObject(ApiModel):
    #: `Operating mode` schedule for Monday to Friday.
    monday_to_friday: Optional[OperatingModeDayScheduleObject] = None
    #: `Operating mode` schedule for Saturday to Sunday.
    saturday_to_sunday: Optional[OperatingModeDayScheduleObject] = None


class OperatingModeDifferentHoursDailyScheduleObject(ApiModel):
    #: `Operating mode` schedule for Sunday.
    sunday: Optional[OperatingModeDayScheduleObject] = None
    #: `Operating mode` schedule for Monday.
    monday: Optional[OperatingModeDayScheduleObject] = None
    #: `Operating mode` schedule for Tuesday.
    tuesday: Optional[OperatingModeDayScheduleObject] = None
    #: `Operating mode` schedule for Wednesday.
    wednesday: Optional[OperatingModeDayScheduleObject] = None
    #: `Operating mode` schedule for Thursday.
    thursday: Optional[OperatingModeDayScheduleObject] = None
    #: `Operating mode` schedule for Friday.
    friday: Optional[OperatingModeDayScheduleObject] = None
    #: `Operating mode` schedule for Saturday.
    saturday: Optional[OperatingModeDayScheduleObject] = None


class MonthObject(str, Enum):
    _january___schedule_the_event_in_january_ = '`JANUARY`: Schedule the event in January.'
    _february___schedule_the_event_in_february_ = '`FEBRUARY`: Schedule the event in February.'
    _march___schedule_the_event_in_march_ = '`MARCH`: Schedule the event in March.'
    _april___schedule_the_event_in_april_ = '`APRIL`: Schedule the event in April.'
    _may___schedule_the_event_in_may_ = '`MAY`: Schedule the event in May.'
    _june___schedule_the_event_in_june_ = '`JUNE`: Schedule the event in June.'
    _july___schedule_the_event_in_july_ = '`JULY`: Schedule the event in July.'
    _august___schedule_the_event_in_august_ = '`AUGUST`: Schedule the event in August.'
    _september___schedule_the_event_in_september_ = '`SEPTEMBER`: Schedule the event in September.'
    _october___schedule_the_event_in_october_ = '`OCTOBER`: Schedule the event in October.'
    _november___schedule_the_event_in_november_ = '`NOVEMBER`: Schedule the event in November.'
    _december___schedule_the_event_in_december_ = '`DECEMBER`: Schedule the event in December.'


class RecurYearlyByDateObject(ApiModel):
    #: Schedule the event on a specific day of the month.
    #: example: 1
    day_of_month: Optional[int] = None
    #: Schedule the event on a specific month of the year.
    #: example: JANUARY
    month: Optional[MonthObject] = None


class RecurYearlyByDayObjectDay(str, Enum):
    sunday = 'SUNDAY'
    _sunday___schedule_the_event_on_sunday_ = '`SUNDAY`: Schedule the event on Sunday.'
    _monday___schedule_the_event_on_monday_ = '`MONDAY`: Schedule the event on Monday.'
    _tuesday___schedule_the_event_on_tuesday_ = '`TUESDAY`: Schedule the event on Tuesday.'
    _wednesday___schedule_the_event_on_wednesday_ = '`WEDNESDAY`: Schedule the event on Wednesday.'
    _thursday___schedule_the_event_on_thursday_ = '`THURSDAY`: Schedule the event on Thursday.'
    _friday___schedule_the_event_on_friday_ = '`FRIDAY`: Schedule the event on Friday.'
    _saturday___schedule_the_event_on_saturday_ = '`SATURDAY`: Schedule the event on Saturday.'


class RecurYearlyByDayObjectWeek(str, Enum):
    second = 'SECOND'
    _first___schedule_the_event_on_the_first_week_of_the_month_ = '`FIRST`: Schedule the event on the first week of the month.'
    _second___schedule_the_event_on_the_second_week_of_the_month_ = '`SECOND`: Schedule the event on the second week of the month.'
    _third___schedule_the_event_on_the_third_week_of_the_month_ = '`THIRD`: Schedule the event on the third week of the month.'
    _fourth___schedule_the_event_on_the_fourth_week_of_the_month_ = '`FOURTH`: Schedule the event on the fourth week of the month.'
    _last___schedule_the_event_on_the_last_week_of_the_month_ = '`LAST`: Schedule the event on the last week of the month.'


class RecurYearlyByDayObject(ApiModel):
    #: Schedule the event on a specific day.
    #: example: SUNDAY
    day: Optional[RecurYearlyByDayObjectDay] = None
    #: Schedule the event on a specific week.
    #: example: SECOND
    week: Optional[RecurYearlyByDayObjectWeek] = None
    #: Schedule the event on a specific month.
    #: example: JANUARY
    month: Optional[MonthObject] = None


class OperatingModeRecurrenceObject(ApiModel):
    #: Recurrence definition yearly by date.
    recur_yearly_by_date: Optional[RecurYearlyByDateObject] = None
    #: Recurrence definition yearly by day.
    recur_yearly_by_day: Optional[RecurYearlyByDayObject] = None


class OperatingModeHolidayGetObject(ApiModel):
    #: A unique identifier for the holiday.
    #: example: Y2lzY29zcGFyazovL3VzL1NDSEVEVUxFX0VWRU5UL2E4Mjg5NzIyLTFiODAtNDFiNy05Njc4LTBlNzdhZThjMTIwOQ
    id: Optional[str] = None
    #: Name of the holiday.
    #: example: Christmas
    name: Optional[str] = None
    #: Specifies if the `operating mode holiday` schedule event is enabled for the entire day. `False` if the flag is
    #: not set.
    #: example: True
    all_day_enabled: Optional[bool] = None
    #: Start date of the `operating mode holiday`.
    #: example: 2024-12-25
    start_date: Optional[datetime] = None
    #: End date of the `operating mode holiday`.
    #: example: 2024-12-26
    end_date: Optional[datetime] = None
    #: Start time for the `operating mode holiday`. Mandatory if `allDayEnabled` is false.
    #: example: 09:00
    start_time: Optional[datetime] = None
    #: End time for the `operating mode holiday`. Mandatory if `allDayEnabled` is false.
    #: example: 17:00
    end_time: Optional[datetime] = None
    #: Recurrence configuration for the `operating mode holiday`.
    recurrence: Optional[OperatingModeRecurrenceObject] = None


class OperatingModeGetObject(ApiModel):
    #: A unique identifier for the `operating mode`.
    #: example: Y2lzY29zcGFyazovL3VzL09QRVJBVElOR19NT0RFL2JiOTc1OTcxLTBjZWYtNDdhNi05Yzc5LTliZWFjY2IwYjg4Mg
    id: Optional[str] = None
    #: Unique name for the `operating mode`.
    #: example: Day Operating Mode
    name: Optional[str] = None
    #: Defines the scheduling of the `operating mode`.
    #: example: SAME_HOURS_DAILY
    type: Optional[OperatingModeScheduleTypeObject] = None
    #: Level at which the `operating mode` would be defined.
    #: example: LOCATION
    level: Optional[OrgLocLevelObject] = None
    #: Location object having a unique identifier for the location, and its name. Mandatory if level is `LOCATION`.
    location: Optional[LocationObject] = None
    #: `Operating mode` schedule for same hours daily. Present if type is `SAME_HOURS_DAILY`.
    same_hours_daily: Optional[OperatingModeSameHoursDailyScheduleObject] = None
    #: `Operating mode` schedule for different hours daily. Present if type is `DIFFERENT_HOURS_DAILY`.
    different_hours_daily: Optional[OperatingModeDifferentHoursDailyScheduleObject] = None
    #: `Operating mode` schedule for holidays. Present if type is `HOLIDAY`.
    holidays: Optional[list[OperatingModeHolidayGetObject]] = None
    #: Call forwarding settings for an `operating mode`.
    call_forwarding: Optional[OperatingModeCallForwarding] = None


class OperatingModeHolidayObject(ApiModel):
    #: Name of the holiday.
    #: example: Christmas
    name: Optional[str] = None
    #: Specifies if the `operating mode holiday` schedule event is enabled for the entire day. `False` if the flag is
    #: not set.
    #: example: True
    all_day_enabled: Optional[bool] = None
    #: Start date of the `operating mode holiday`.
    #: example: 2024-12-25
    start_date: Optional[datetime] = None
    #: End date of the `operating mode holiday`.
    #: example: 2024-12-26
    end_date: Optional[datetime] = None
    #: Start time for the `operating mode holiday`. Mandatory if `allDayEnabled` is false.
    #: example: 09:00
    start_time: Optional[datetime] = None
    #: End time for the `operating mode holiday`. Mandatory if `allDayEnabled` is false.
    #: example: 17:00
    end_time: Optional[datetime] = None
    #: Recurrence configuration for the `operating mode holiday`.
    recurrence: Optional[OperatingModeRecurrenceObject] = None


class BetaFeaturesScheduleBasedRoutingWithOperatingModesApi(ApiChild, base='telephony/config'):
    """
    Beta Features: Schedule Based Routing with Operating Modes
    
    Features: `Operating modes` help manage calls more efficiently by routing them based on predefined settings.
    Authorized users can adjust these modes to reduce wait times for clients.
    `Operating modes` are used by mode-based forwarding for the `Auto Attendant`, `Call Queue`, and `Hunt Group`
    features.
    
    Viewing these read-only organization settings requires a full, read-only, or location administrator auth token with
    a scope of `spark-admin:telephony_config_read`.
    
    Modifying these organization settings requires a full, or location administrator auth token with a scope of
    `spark-admin:telephony_config_write`.
    
    A partner administrator can retrieve, or change settings in a customer's organization using the optional `orgId`
    query parameter.
    """

    def read_the_list_of_operating_modes_(self, limit_to_location_id: str, name: str = None,
                                          limit_to_org_level_enabled: bool = None, order: str = None,
                                          org_id: str = None,
                                          **params) -> Generator[OperatingModeListGetObject, None, None]:
        """
        Read the List of Operating Modes.

        Retrieve `Operating Modes` list defined at location, or organization level. Use query parameters to filter the
        result set by location or level. The list returned is sorted in ascending order by operating mode name. Long
        result sets are split into `pages
        <https://developer.webex.com/docs/basics#pagination>`_.

        `Operating modes` help manage calls more efficiently by routing them based on predefined settings.

        Retrieving this list requires a full, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param limit_to_location_id: Location query parameter to filter the `operating modes` from that location only.
        :type limit_to_location_id: str
        :param name: List `operating modes` whose name contains this string.
        :type name: str
        :param limit_to_org_level_enabled: If true, only return `operating modes` defined at the organization level.
        :type limit_to_org_level_enabled: bool
        :param order: Sort the list of `operating modes` based on `name`, either asc, or desc.
        :type order: str
        :param org_id: Retrieve `operating modes` list from this organization.
        :type org_id: str
        :return: Generator yielding :class:`OperatingModeListGetObject` instances
        """
        if name is not None:
            params['name'] = name
        params['limitToLocationId'] = limit_to_location_id
        if limit_to_org_level_enabled is not None:
            params['limitToOrgLevelEnabled'] = str(limit_to_org_level_enabled).lower()
        if order is not None:
            params['order'] = order
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep('operatingModes')
        return self.session.follow_pagination(url=url, model=OperatingModeListGetObject, item_key='operatingModes', params=params)

    def get_details_for_an_operating_mode_(self, mode_id: str, org_id: str = None) -> OperatingModeGetObject:
        """
        Get Details for an Operating Mode.

        Retrieve an `Operating Mode` by `Operating Mode ID`.

        `Operating modes` can be used to define call routing rules for different scenarios like business hours, after
        hours, holidays, etc.

        Retrieving an `operating mode` requires a full, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param mode_id: Get the `operating mode` with the matching ID.
        :type mode_id: str
        :param org_id: Get the `operating mode` from this organization.
        :type org_id: str
        :rtype: :class:`OperatingModeGetObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'operatingModes/{mode_id}')
        data = super().get(url, params=params)
        r = OperatingModeGetObject.model_validate(data)
        return r

    def create_an_operating_mode_(self, name: str, type: OperatingModeScheduleTypeObject, level: OrgLocLevelObject,
                                  call_forwarding: OperatingModeCallForwarding, location_id: str = None,
                                  same_hours_daily: OperatingModeSameHoursDailyScheduleObject = None,
                                  different_hours_daily: OperatingModeDifferentHoursDailyScheduleObject = None,
                                  holidays: list[OperatingModeHolidayObject] = None, org_id: str = None) -> str:
        """
        Create an Operating Mode.

        Create an `Operating Mode` at an organization, or a location level.

        `Operating modes` can be used to define call routing rules for different scenarios like business hours, after
        hours, holidays, etc.

        Creating an `Operating Mode` requires a full, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param name: Unique name for the `operating mode`.
        :type name: str
        :param type: Defines the scheduling of the `operating mode`.
        :type type: OperatingModeScheduleTypeObject
        :param level: Level at which the `operating mode` would be defined.
        :type level: OrgLocLevelObject
        :param call_forwarding: Call forwarding settings for an `operating mode`.
        :type call_forwarding: OperatingModeCallForwarding
        :param location_id: Unique identifier of the location. Mandatory if level is `LOCATION`.
        :type location_id: str
        :param same_hours_daily: `Operating mode` schedule for same hours daily. Mandatory if type is
            `SAME_HOURS_DAILY`.
        :type same_hours_daily: OperatingModeSameHoursDailyScheduleObject
        :param different_hours_daily: `Operating mode` schedule for different hours daily. Mandatory if type is
            `DIFFERENT_HOURS_DAILY`.
        :type different_hours_daily: OperatingModeDifferentHoursDailyScheduleObject
        :param holidays: `Operating mode` holidays. Mandatory if type is `HOLIDAY`.
        :type holidays: list[OperatingModeHolidayObject]
        :param org_id: Create the `operating mode` for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['type'] = enum_str(type)
        body['level'] = enum_str(level)
        if location_id is not None:
            body['locationId'] = location_id
        if same_hours_daily is not None:
            body['sameHoursDaily'] = same_hours_daily.model_dump(mode='json', by_alias=True, exclude_none=True)
        if different_hours_daily is not None:
            body['differentHoursDaily'] = different_hours_daily.model_dump(mode='json', by_alias=True, exclude_none=True)
        if holidays is not None:
            body['holidays'] = TypeAdapter(list[OperatingModeHolidayObject]).dump_python(holidays, mode='json', by_alias=True, exclude_none=True)
        body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep('operatingModes')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_an_operating_mode_(self, mode_id: str, name: str = None,
                                  same_hours_daily: OperatingModeSameHoursDailyScheduleObject = None,
                                  different_hours_daily: OperatingModeDifferentHoursDailyScheduleObject = None,
                                  holidays: list[OperatingModeHolidayObject] = None,
                                  call_forwarding: OperatingModeCallForwarding = None, org_id: str = None):
        """
        Modify an Operating Mode.

        Modify the designated `Operating Mode's` configuration.

        `Operating modes` can be used to define call routing rules for different scenarios like business hours, after
        hours, holidays, etc.

        Modifying an `Operating Mode` requires a full, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param mode_id: Modify the `operating mode` with the matching ID.
        :type mode_id: str
        :param name: New unique name for the `operating mode`.
        :type name: str
        :param same_hours_daily: Updated schedule for same hours daily.
        :type same_hours_daily: OperatingModeSameHoursDailyScheduleObject
        :param different_hours_daily: Updated schedule for different hours daily.
        :type different_hours_daily: OperatingModeDifferentHoursDailyScheduleObject
        :param holidays: Updated holidays. This will replace the existing holidays.
        :type holidays: list[OperatingModeHolidayObject]
        :param call_forwarding: Updated call forwarding settings for an `operating mode`.
        :type call_forwarding: OperatingModeCallForwarding
        :param org_id: Modify the `operating mode` from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if same_hours_daily is not None:
            body['sameHoursDaily'] = same_hours_daily.model_dump(mode='json', by_alias=True, exclude_none=True)
        if different_hours_daily is not None:
            body['differentHoursDaily'] = different_hours_daily.model_dump(mode='json', by_alias=True, exclude_none=True)
        if holidays is not None:
            body['holidays'] = TypeAdapter(list[OperatingModeHolidayObject]).dump_python(holidays, mode='json', by_alias=True, exclude_none=True)
        if call_forwarding is not None:
            body['callForwarding'] = call_forwarding.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'operatingModes/{mode_id}')
        super().put(url, params=params, json=body)

    def delete_an_operating_mode_(self, mode_id: str, org_id: str = None):
        """
        Delete an Operating Mode.

        Delete the designated `Operating Mode`.

        Deleting an `Operating Mode` requires a full, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param mode_id: Delete the `operating mode` with the matching ID.
        :type mode_id: str
        :param org_id: Delete the `operating mode` from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'operatingModes/{mode_id}')
        super().delete(url, params=params)

    def get_details_for_an_operating_mode_holiday_(self, mode_id: str, holiday_id: str = None,
                                                   org_id: str = None) -> OperatingModeHolidayGetObject:
        """
        Get details for an Operating Mode Holiday.

        Retrieve an `Operating Mode Holiday` by ID.

        Holidays define a recurring schedule for the `Operating Modes`.

        Retrieving an `Operating Mode Holiday` requires a full, read-only, or location administrator auth token with a
        scope of `spark-admin:telephony_config_read`.

        :param mode_id: Get the holiday from this `operating mode` matching ID.
        :type mode_id: str
        :param holiday_id: Get the `operating mode Holiday` with the matching ID.
        :type holiday_id: str
        :param org_id: Get the `operating mode` from this organization.
        :type org_id: str
        :rtype: :class:`OperatingModeHolidayGetObject`
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'operatingModes/{mode_id}/holidays/{holiday_id}')
        data = super().get(url, params=params)
        r = OperatingModeHolidayGetObject.model_validate(data)
        return r

    def create_an_operating_mode_holiday_(self, mode_id: str, name: str, all_day_enabled: bool, start_date: Union[str,
                                          datetime], end_date: Union[str, datetime], start_time: Union[str,
                                          datetime] = None, end_time: Union[str, datetime] = None,
                                          recurrence: OperatingModeRecurrenceObject = None,
                                          org_id: str = None) -> str:
        """
        Create an Operating Mode Holiday.

        Create a holiday schedule event for the designated `Operating Mode`.

        Holidays define a recurring schedule for the `Operating Modes`. An `Operating Mode` can have a max of 150
        holidays.

        Creating an `Operating Mode Holiday` requires a full, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param mode_id: Create the holiday for this `operating mode`.
        :type mode_id: str
        :param name: Name of the holiday.
        :type name: str
        :param all_day_enabled: Specifies if the `operating mode holiday` schedule event is enabled for the entire day.
            `False` if the flag is not set.
        :type all_day_enabled: bool
        :param start_date: Start date of the `operating mode holiday`.
        :type start_date: Union[str, datetime]
        :param end_date: End date of the `operating mode holiday`.
        :type end_date: Union[str, datetime]
        :param start_time: Start time for the `operating mode holiday`. Mandatory if `allDayEnabled` is false.
        :type start_time: Union[str, datetime]
        :param end_time: End time for the `operating mode holiday`. Mandatory if `allDayEnabled` is false.
        :type end_time: Union[str, datetime]
        :param recurrence: Recurrence configuration for the `operating mode holiday`.
        :type recurrence: OperatingModeRecurrenceObject
        :param org_id: Create the `operating mode holiday` for this organization.
        :type org_id: str
        :rtype: str
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        body['name'] = name
        body['allDayEnabled'] = all_day_enabled
        body['startDate'] = start_date
        body['endDate'] = end_date
        if start_time is not None:
            body['startTime'] = start_time
        if end_time is not None:
            body['endTime'] = end_time
        if recurrence is not None:
            body['recurrence'] = recurrence.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'operatingModes/{mode_id}/holidays')
        data = super().post(url, params=params, json=body)
        r = data['id']
        return r

    def modify_an_operating_mode_holiday_(self, mode_id: str, holiday_id: str = None, name: str = None,
                                          all_day_enabled: bool = None, start_date: Union[str, datetime] = None,
                                          end_date: Union[str, datetime] = None, start_time: Union[str,
                                          datetime] = None, end_time: Union[str, datetime] = None,
                                          recurrence: OperatingModeRecurrenceObject = None, org_id: str = None):
        """
        Modify an Operating Mode Holiday.

        Modify the designated `Operating Mode Holiday's` configuration.

        Modifying an `Operating Mode Holiday` requires a full, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param mode_id: Modify the holiday from this `operating mode` matching ID.
        :type mode_id: str
        :param holiday_id: Modify the `Holiday` with the matching ID.
        :type holiday_id: str
        :param name: Name of the holiday.
        :type name: str
        :param all_day_enabled: Specifies if the `operating mode holiday` schedule event is enabled for the entire day.
            If `startTime`, and `endTime` are provided, this field is ignored.
        :type all_day_enabled: bool
        :param start_date: Start date of the `operating mode holiday`.
        :type start_date: Union[str, datetime]
        :param end_date: End date of the `operating mode holiday`.
        :type end_date: Union[str, datetime]
        :param start_time: Start time for the `operating mode holiday`. Mandatory if `allDayEnabled` is not set.
        :type start_time: Union[str, datetime]
        :param end_time: End time for the `operating mode holiday`. Mandatory if `allDayEnabled` is not set.
        :type end_time: Union[str, datetime]
        :param recurrence: Recurrence configuration for the `operating mode holiday`.
        :type recurrence: OperatingModeRecurrenceObject
        :param org_id: Modify the `operating mode` from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        body = dict()
        if name is not None:
            body['name'] = name
        if all_day_enabled is not None:
            body['allDayEnabled'] = all_day_enabled
        if start_date is not None:
            body['startDate'] = start_date
        if end_date is not None:
            body['endDate'] = end_date
        if start_time is not None:
            body['startTime'] = start_time
        if end_time is not None:
            body['endTime'] = end_time
        if recurrence is not None:
            body['recurrence'] = recurrence.model_dump(mode='json', by_alias=True, exclude_none=True)
        url = self.ep(f'operatingModes/{mode_id}/holidays/{holiday_id}')
        super().put(url, params=params, json=body)

    def delete_an_operating_mode_holiday_(self, mode_id: str, holiday_id: str = None, org_id: str = None):
        """
        Delete an Operating Mode Holiday.

        Delete the designated `Operating Mode Holiday`.

        Deleting an `Operating Mode Holiday` requires a full, or location administrator auth token with a scope of
        `spark-admin:telephony_config_write`.

        :param mode_id: Delete the holiday from this `operating mode` matching ID.
        :type mode_id: str
        :param holiday_id: Delete the holiday with the matching ID.
        :type holiday_id: str
        :param org_id: Delete the `operating mode` from this organization.
        :type org_id: str
        :rtype: None
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'operatingModes/{mode_id}/holidays/{holiday_id}')
        super().delete(url, params=params)

    def retrieve_the_list_of_available_operating_modes_in_a_location_(self, location_id: str,
                                                                      org_id: str = None) -> list[LocationObject]:
        """
        Retrieve the List of Available Operating Modes in a Location.

        Retrieve list of `Operating Modes` which are available to be assigned to a location level feature (`Auto
        Attendant`, `Call Queue`, or `Hunt Group`). Since each location and an org can have a max of 100 `Operating
        Modes` defined. The max number of `operating modes` that can be returned is 200.

        `Operating modes` can be used to define call routing rules for different scenarios like business hours, after
        hours, holidays, etc. for the `Auto Attendant`, `Call Queue`, and `Hunt Group` features.

        Retrieving this list requires a full, read-only, or location administrator auth token with a scope of
        `spark-admin:telephony_config_read`.

        :param location_id: Retrieve `operating modes` list from this location.
        :type location_id: str
        :param org_id: Retrieve `operating modes` list from this organization.
        :type org_id: str
        :rtype: list[LocationObject]
        """
        params = {}
        if org_id is not None:
            params['orgId'] = org_id
        url = self.ep(f'locations/{location_id}/operatingModes/availableOperatingModes')
        data = super().get(url, params=params)
        r = TypeAdapter(list[LocationObject]).validate_python(data['operatingModes'])
        return r
