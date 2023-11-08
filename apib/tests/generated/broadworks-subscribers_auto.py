from collections.abc import Generator
from datetime import datetime
from typing import Optional, Union

from dateutil.parser import isoparse
from pydantic import Field

from wxc_sdk.api_child import ApiChild
from wxc_sdk.base import ApiModel, dt_iso_str
from wxc_sdk.base import SafeEnum as Enum


__auto__ = ['Error', 'PrecheckABroadworksSubscriberProvisioningCustomerInfo', 'Subscriber', 'SubscriberListResponse',
            'SubscriberPackage', 'SubscriberProvisioningPrecheckResponse',
            'SubscriberProvisioningPrecheckResponseInfo', 'SubscriberStatus']


class Error(ApiModel):
    #: An error code that identifies the reason for the error.
    #: example: 10022.0
    error_code: Optional[int] = None
    #: A description of the error.
    #: example: The BroadWorks UserID is already associated with an existing user.
    description: Optional[str] = None


class SubscriberPackage(str, Enum):
    #: Softphone package.
    softphone = 'softphone'
    #: Basic package.
    basic = 'basic'
    #: Standard package.
    standard = 'standard'
    #: Premium package.
    premium = 'premium'


class SubscriberStatus(str, Enum):
    #: Subscriber Provisioning is paused, pending input of email address.
    pending_email_input = 'pending_email_input'
    #: Subscriber Provisioning is paused. The subscriber has entered an email address but has yet to complete
    #: validation.
    pending_email_validation = 'pending_email_validation'
    #: Subscriber Provisioning is paused. An automated email is sent to the subscriber, waiting for the subscriber's
    #: consent.
    pending_user_migration = 'pending_user_migration'
    #: Subscriber provisioning is in progress.
    provisioning = 'provisioning'
    #: The subscriber is fully provisioned on Webex.
    provisioned = 'provisioned'
    #: An update is in progress for a provisioned subscriber.
    updating = 'updating'
    #: An error occurred provisioning the subscriber on Webex.
    error = 'error'


class Subscriber(ApiModel):
    #: A unique Cisco identifier for the subscriber.
    #: example: 'Y2lzY29zcGFyazovL3VzL1NVQlNDUklCRVIvNjk3MGU2YmItNzQzOS00ZmZiLWFkMzQtZDNmZjAxNjdkZGFk'
    id: Optional[str] = None
    #: The Person Id of the subscriber on Webex. To be used when referencing this subscriber on other Webex APIs. Only
    #: presented when status is `provisioned`.
    #: example: Y2lzY29zcGFyazovL3VzL1BFT1BMRS9mNWIzNjE4Ny1jOGRkLTQ3MjctOGIyZi1mOWM0NDdmMjkwNDY
    person_id: Optional[str] = None
    #: The user ID of the subscriber on BroadWorks.
    #: example: 95547321@sp.com
    user_id: Optional[str] = None
    #: The Service Provider supplied unique identifier for the subscriber's enterprise.
    #: example: Reseller1+acme
    sp_enterprise_id: Optional[str] = None
    #: The first name of the subscriber.
    #: example: John
    first_name: Optional[str] = None
    #: The last name of the subscriber.
    #: example: Andersen
    last_name: Optional[str] = None
    #: The email address of the subscriber.
    #: example: john.anderson@acme.com
    email: Optional[str] = None
    #: The primary phone number configured against the subscriber on BroadWorks.
    #: example: +1-240-555-1212
    primary_phone_number: Optional[str] = None
    #: The mobile phone number configured against the subscriber on BroadWorks.
    #: example: +1-818-279-1234
    mobile_phone_number: Optional[str] = None
    #: The extension number configured against the subscriber on BroadWorks.
    #: example: 1212
    extension: Optional[datetime] = None
    #: The Webex for BroadWorks Package assigned to the subscriber.
    #: example: standard
    package: Optional[SubscriberPackage] = None
    #: The provisioning status of the user.
    #: example: provisioned
    status: Optional[SubscriberStatus] = None
    #: List of errors that occurred during that last attempt to provision/update this subscriber.
    #: 
    #: *Note:*
    #: 
    #: + This list captures errors that occurred during *asynchronous or background* provisioning of the subscriber,
    #: *after* the API has been accepted and 200 OK response returned.
    #: 
    #: + Any errors that occur during initial API request validation will be captured directly in error response with
    #: appropriate HTTP status code.
    errors: Optional[list[Error]] = None
    #: The date and time the subscriber was provisioned.
    #: example: 2019-10-18T14:26:16.000Z
    created: Optional[datetime] = None
    #: The date and time the provisioning status of the subscriber last changed.
    #: example: 2020-03-18T16:05:34.000Z
    last_status_change: Optional[datetime] = None
    #: This Provisioning ID associated with this subscriber.
    #: example: ZjViMzYxODctYzhkZC00NzI3LThiMmYtZjljNDQ3ZjI5MDQ2OjQyODVmNTk0LTViNTEtNDdiZS05Mzk2LTZjMzZlMmFkODNhNQ
    provisioning_id: Optional[str] = None
    #: Indicates if the subscriber was self activated, rather than provisioned via these APIs.
    self_activated: Optional[bool] = None


class SubscriberListResponse(ApiModel):
    #: An array of Subscriber objects.
    items: Optional[list[Subscriber]] = None


class SubscriberProvisioningPrecheckResponseInfo(ApiModel):
    #: Provisioning Precheck `infoCode`.
    #: example: 100.0
    info_code: Optional[int] = None
    #: A textual description of the `infoCode`.
    #: example: Provisioning Precheck validation successful.
    description: Optional[str] = None


class SubscriberProvisioningPrecheckResponse(ApiModel):
    #: A textual representation of the Precheck response message containing the `infoCode` object in the case of a
    #: success response and the `errorCode` object in the case of failure.
    #: example: success
    message: Optional[str] = None
    #: A list of `ProvisioningPreCheckResponseInfo` objects.
    info: Optional[SubscriberProvisioningPrecheckResponseInfo] = None


class PrecheckABroadworksSubscriberProvisioningCustomerInfo(ApiModel):
    #: Email address of the customer org user to be provisioned.
    #: example: "john.anderson@example.com"
    primary_email: Optional[str] = None


class BroadWorksSubscribersApi(ApiChild, base='broadworks/subscribers'):
    """
    BroadWorks Subscribers
    
    These are a set of APIs that are specifically targeted at BroadWorks Service Providers who sign up to the Webex for
    BroadWorks solution. They enable Service Providers to provision Webex Services for their subscribers. Please note
    these APIs require a functional BroadWorks system configured for Webex for BroadWorks. Read more about using this
    API
    at https://www.cisco.com/go/WebexBroadworksAPI.
    
    Viewing Webex for BroadWorks subscriber information requires an administrator auth token with
    `spark-admin:broadworks_subscribers_read` scope. Provisioning, updating, and removing subscribers requires an
    administrator auth token with the `spark-admin:broadworks_subscribers_write` scope.
    
    <div>
    <Callout type="info">Additional Infocodes are given for all success cases. To learn more about the Infocodes used
    in Broadworks Subscriber Provisioning Precheck APIs, see the `Provisioning Precheck API Info Codes
    <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#whats-possible-with-webex-for-broadworks-provisioning-precheck-apis>`_
    guides.</Callout>
    </div>
    """

    def list_broad_works_subscribers(self, user_id: str = None, person_id: str = None, email: str = None,
                                     provisioning_id: str = None, sp_enterprise_id: str = None,
                                     last_status_change: str = None, status: SubscriberStatus = None,
                                     after: str = None, self_activated: bool = None,
                                     max_: int = None) -> list[Subscriber]:
        """
        List BroadWorks Subscribers

        This API lets a Service Provider search for their associated subscribers. There are a number of filter options
        that can be combined in a single request.

        :param user_id: The user ID of the subscriber on BroadWorks.
        :type user_id: str
        :param person_id: The Person ID of the Webex subscriber.
        :type person_id: str
        :param email: The email address of the subscriber.
        :type email: str
        :param provisioning_id: The Provisioning ID associated with this subscriber.
        :type provisioning_id: str
        :param sp_enterprise_id: The Service Provider supplied unique identifier for the subscriber's enterprise.
        :type sp_enterprise_id: str
        :param last_status_change: Only include subscribers with a provisioning status change after this date and time.
            Epoch time (in milliseconds) preferred, but ISO 8601 date format also accepted.
        :type last_status_change: str
        :param status: The provisioning status of the subscriber. This Parameter supports multiple comma separated
            values. For example : status=error,provisioned,provisioning.
        :type status: SubscriberStatus
        :param after: Only include subscribers created after this date and time. Epoch time (in milliseconds)
            preferred, but ISO 8601 date format also accepted.
        :type after: str
        :param self_activated: Indicates if the subscriber was self activated, rather than provisioned via these APIs.
        :type self_activated: bool
        :param max_: Limit the maximum number of subscribers returned in the search response, up to 100 per page. Refer
            to the `Pagination
            <https://developer.webex.com/docs/basics#pagination>`_ section of `Webex REST API Basics
        :type max_: int
        :rtype: list[Subscriber]
        """
        params = {}
        if user_id is not None:
            params['userId'] = user_id
        if person_id is not None:
            params['personId'] = person_id
        if email is not None:
            params['email'] = email
        if provisioning_id is not None:
            params['provisioningId'] = provisioning_id
        if sp_enterprise_id is not None:
            params['spEnterpriseId'] = sp_enterprise_id
        if last_status_change is not None:
            params['lastStatusChange'] = last_status_change
        if status is not None:
            params['status'] = status
        if after is not None:
            params['after'] = after
        if self_activated is not None:
            params['selfActivated'] = str(self_activated).lower()
        if max_ is not None:
            params['max'] = max_
        url = self.ep()
        ...


    def provision_a_broad_works_subscriber(self, provisioning_id: str, user_id: str, sp_enterprise_id: str,
                                           first_name: str, last_name: str, package: SubscriberPackage,
                                           primary_phone_number: str = None, mobile_phone_number: str = None,
                                           extension: Union[str, datetime] = None, email: str = None,
                                           language: str = None, timezone: str = None) -> Subscriber:
        """
        Provision a BroadWorks Subscriber

        Provision a new BroadWorks subscriber for Webex services.
        
        This API lets a Service Provider map a BroadWorks subscriber to a new or existing Webex user and assign the
        required licenses and entitlements for Webex and Meetings.

        :param provisioning_id: This Provisioning ID defines how this subscriber is to be provisioned for Webex
            Services.
        
        Each Customer Template will have their own unique Provisioning ID. This ID will be displayed under the chosen
        Customer Template
        on Webex Partner Hub.
        :type provisioning_id: str
        :param user_id: The user ID of the subscriber on BroadWorks.
        :type user_id: str
        :param sp_enterprise_id: The Service Provider supplied unique identifier for the subscriber's enterprise.
        :type sp_enterprise_id: str
        :param first_name: The first name of the subscriber.
        :type first_name: str
        :param last_name: The last name of the subscriber.
        :type last_name: str
        :param package: The Webex for BroadWorks package to be assigned to the subscriber.
        :type package: SubscriberPackage
        :param primary_phone_number: The primary phone number configured against the subscriber on BroadWorks.
        :type primary_phone_number: str
        :param mobile_phone_number: The mobile phone number configured against the subscriber on BroadWorks. Any empty
            value on update will remove the already configured mobile phone number.
        :type mobile_phone_number: str
        :param extension: The extension number configured against the subscriber on BroadWorks.
        :type extension: Union[str, datetime]
        :param email: The email address of the subscriber (mandatory for the trusted email provisioning flow).
        :type email: str
        :param language: The {ISO-639-1}_{ISO-3166} or {ISO-639-1} locale or language code used as preferred language
            for organization and Webex Meeting Sites. Refer to the `help page
            <https://www.cisco.com/content/en/us/td/docs/voice_ip_comm/cloudCollaboration/wx4bwks/Solution_Guide/wbxbw_b_solution-guide/wbxbw_b_SolutionGuide-PDF_chapter_01.html#Cisco_Reference.dita_f10351e1-f775-418d-a700-ec8487e0a33b>`_ for more information.
        :type language: str
        :param timezone: The time zone associated with the subscriber. Refer to the `Webex Meetings Site Timezone
            <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone>`_
            section of the `Webex for BroadWorks
            <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide>`_ guide for more information.
        :type timezone: str
        :rtype: :class:`Subscriber`
        """
        url = self.ep()
        ...


    def get_a_broad_works_subscriber(self, subscriber_id: str) -> Subscriber:
        """
        Get a BroadWorks Subscriber

        This API lets a Service Provider retrieve details of a provisioned BroadWorks subscriber on Webex.

        :param subscriber_id: A unique identifier for the subscriber in question.
        :type subscriber_id: str
        :rtype: :class:`Subscriber`
        """
        url = self.ep(f'{subscriber_id}')
        ...


    def update_a_broad_works_subscriber(self, subscriber_id: str, user_id: str = None, first_name: str = None,
                                        last_name: str = None, primary_phone_number: str = None,
                                        mobile_phone_number: str = None, extension: Union[str, datetime] = None,
                                        timezone: str = None, package: str = None) -> Subscriber:
        """
        Update a BroadWorks Subscriber

        This API lets a Service Provider update certain details of a provisioned BroadWorks subscriber
        on Webex.
        
        <div>
        <Callout type='info'>The updated items will not be immediately reflected in the response body, but can be
        subsequently obtained via the `Get a BroadWorks Subscriber
        <https://developer.webex.com/docs/api/v1/broadworks-subscribers/get-a-broadworks-subscriber>`_ API once the status has transitioned from the
        updating state to the provisioned state.</Callout>
        </div>
        
        o

        :param subscriber_id: A unique identifier for the subscriber in question.
        :type subscriber_id: str
        :param user_id: The user ID of the subscriber on BroadWorks.
        :type user_id: str
        :param first_name: The first name of the subscriber.
        :type first_name: str
        :param last_name: The last name of the subscriber.
        :type last_name: str
        :param primary_phone_number: The primary phone number configured against the subscriber on BroadWorks.
        :type primary_phone_number: str
        :param mobile_phone_number: The mobile phone number configured against the subscriber on BroadWorks. Any empty
            value on update will remove the already configured mobile phone number.
        :type mobile_phone_number: str
        :param extension: The extension number configured against the subscriber on BroadWorks.
        :type extension: Union[str, datetime]
        :param timezone: The time zone associated with the subscriber. Refer to the `Webex Meetings Site Timezone
            <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone>`_
            section of the `Webex for BroadWorks
            <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide>`_ guide for more information.
        :type timezone: str
        :param package: The Webex for BroadWorks Package to be assigned to the subscriber.
        :type package: str
        :rtype: :class:`Subscriber`
        """
        url = self.ep(f'{subscriber_id}')
        ...


    def remove_a_broad_works_subscriber(self, subscriber_id: str):
        """
        Remove a BroadWorks Subscriber

        This API will allow a Service Provider to remove the mapping between a BroadWorks Subscriber and Webex user.

        :param subscriber_id: A unique identifier for the subscriber in question.
        :type subscriber_id: str
        :rtype: None
        """
        url = self.ep(f'{subscriber_id}')
        ...


    def precheck_a_broadworks_subscriber_provisioning(self, email: str, provisioning_id: str = None,
                                                      user_id: str = None, sp_enterprise_id: str = None,
                                                      first_name: str = None, last_name: str = None,
                                                      package: SubscriberPackage = None,
                                                      primary_phone_number: str = None,
                                                      mobile_phone_number: str = None, extension: Union[str,
                                                      datetime] = None, language: str = None, timezone: str = None,
                                                      customer_info: PrecheckABroadworksSubscriberProvisioningCustomerInfo = None) -> SubscriberProvisioningPrecheckResponse:
        """
        Precheck a Broadworks Subscriber Provisioning

        Verify the likely success of provisioning a broadworks subscriber.
        
        <div>
        <Callout type='info'>
        The Prerequisite for using this API is to have at least one Broadworks Cluster configured against partner using
        Partner Hub. The Provisioning Precheck APIs supports two variants of Broadworks Provisioning Precheck
        Requests. Please refer to `Using the Provisioning Precheck API
        <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#using-the-precheck-provisioning-api>`_ section in `Webex for BroadWorks
        information.
        </Callout>
        </div>

        :param email: The email address of the subscriber.
        :type email: str
        :param provisioning_id: Provisioning ID that defines how this subscriber is to be provisioned for Cisco Webex
            Services. Each Customer Template has its unique Provisioning ID. This ID will be displayed under the
            chosen Customer Template on Cisco Webex Control Hub.
        :type provisioning_id: str
        :param user_id: The user ID of the Broadworks subscriber.
        :type user_id: str
        :param sp_enterprise_id: The Service Provider supplied unique identifier for the subscriber's enterprise.
        :type sp_enterprise_id: str
        :param first_name: The first name of the subscriber.
        :type first_name: str
        :param last_name: The last name of the subscriber.
        :type last_name: str
        :param package: The Webex for BroadWorks package to be assigned to the subscriber.
        :type package: SubscriberPackage
        :param primary_phone_number: The primary phone number configured for the subscriber on BroadWorks.
        :type primary_phone_number: str
        :param mobile_phone_number: The mobile phone number configured against the subscriber on BroadWorks.
        :type mobile_phone_number: str
        :param extension: The extension number configured against the subscriber on BroadWorks.
        :type extension: Union[str, datetime]
        :param language: The ISO 639-1 language code associated with the subscriber. Reserved for future use. Any value
            currently specified will be ignored during subscriber provisioning.
        :type language: str
        :param timezone: The time zone associated with the subscriber. Refer to the `Webex Meetings Site Timezone
            <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide#webex-meetings-site-timezone>`_
            section of the `Webex for BroadWorks
            <https://developer.webex.com/docs/api/guides/webex-for-broadworks-developers-guide>`_ guide for more information.
        :type timezone: str

        :type customer_info: PrecheckABroadworksSubscriberProvisioningCustomerInfo
        :rtype: :class:`SubscriberProvisioningPrecheckResponse`
        """
        url = self.ep('validate')
        ...

    ...