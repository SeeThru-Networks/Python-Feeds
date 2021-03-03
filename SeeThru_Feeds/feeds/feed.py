import json
from json import JSONDecodeError
from uuid import UUID

import requests
from requests import RequestException

from SeeThru_Feeds.feeds.api_key import ApiKey
from SeeThru_Feeds.feeds.exceptions import InvalidFeedGuid, InvalidApiKey, ApiError, MalformedApiResponse, \
    ApiUnexpectedError, ApiInvalidGuid, ApiKeyInvalidPermissions, ApiKeyTimeout, ApiInvalidFeedResult, \
    ApiKeyUnauthorized
from SeeThru_Feeds.feeds.feed_result import FeedResult


def match_error_api_message_to_exception(message: str):
    """
    Matches the message given by the api to a specific exception
    Args:
        message (str): The message to match
    """
    if message == "An unexpected error occurred.":
        raise ApiUnexpectedError()
    elif message == "Please specify a valid Feed GUID.":
        raise ApiInvalidGuid()
    elif message == "Please use an authorised API key.":
        raise ApiKeyUnauthorized()
    elif message == "You do not have permission to update the selected feed.":
        raise ApiKeyInvalidPermissions()
    elif message == "This feed has already been updated within the last 30 seconds.":
        raise ApiKeyTimeout()
    elif message == "Invalid result color specified.":
        raise ApiInvalidFeedResult("Invalid feed result status")
    elif message == "Invalid timestamp specified.":
        raise ApiInvalidFeedResult("Invalid feed result timestamp")
    elif message == "Invalid version number specified.":
        raise ApiInvalidFeedResult("Invalid feed version")


class Feed:
    # Containers of the true values
    _feed_guid: UUID
    _api_key: ApiKey
    _result: FeedResult
    _version: str = "1"

    def __init__(self, feed_guid: UUID, api_key: ApiKey, result: FeedResult, version: str):
        self.feed_guid = feed_guid
        self.api_key = api_key
        self.result = result
        self.version = version

    @property
    def feed_guid(self) -> UUID:
        return self._feed_guid

    @feed_guid.setter
    def feed_guid(self, feed_guid: UUID):
        if type(feed_guid) != UUID:
            raise InvalidFeedGuid("feed_guid must be of type UUID")
        self._feed_guid = feed_guid

    def get_feed_guid(self):
        return self.feed_guid

    @property
    def api_key(self) -> ApiKey:
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: ApiKey):
        if type(api_key) != ApiKey:
            raise InvalidApiKey("api_key must be of type ApiKey")
        self._api_key = api_key

    def get_api_key(self):
        return self.api_key

    @property
    def result(self) -> FeedResult:
        return self._result

    @result.setter
    def result(self, result: FeedResult):
        if type(result) != FeedResult:
            raise TypeError("result must be a valid FeedResult")
        self._result = result

    def get_result(self):
        return self.result

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, version: str):
        if type(version) != str:
            raise TypeError("version must be a valid string")
        self._version = version

    def get_version(self):
        return self.version

    def push(self):
        headers = {
            "X-Access-Token": str(self.api_key.access_token),
            "X-secret": self.api_key.secret_key
        }
        data = {
            "guid": str(self.feed_guid),
            "color": self.result.get_status_value(),
            "message": self.result.message,
            "timestamp": self.result.get_timestamp_str(),
            "version": self.version
        }

        try:
            response = requests.post(
                f"https://api.seethrunetworks.com/feed/{str(self.feed_guid)}/update",
                data=data,
                headers=headers)
        except RequestException as e:
            raise e

        try:
            response_json = json.loads(response.content)
            if "success" not in response_json:
                raise MalformedApiResponse()
            # Only matches the error for an unsuccessful post
            if not response_json["success"]:
                if "message" not in response_json:
                    raise MalformedApiResponse()

                try:
                    match_error_api_message_to_exception(response_json["message"])
                except ApiError as e:
                    raise e

        except JSONDecodeError:
            raise MalformedApiResponse()
