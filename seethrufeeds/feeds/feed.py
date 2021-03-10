import json
from dataclasses import dataclass
from json import JSONDecodeError
from uuid import UUID

import requests
from requests import RequestException

from seethrufeeds.feeds.api_key import ApiKey
from seethrufeeds.feeds.exceptions import InvalidFeedGuid, InvalidApiKey, ApiError, MalformedApiResponse, \
    ApiUnexpectedError, ApiInvalidGuid, ApiKeyInvalidPermissions, ApiKeyTimeout, ApiInvalidFeedResult, \
    ApiKeyUnauthorized
from seethrufeeds.feeds.feed_result import FeedResult


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


@dataclass(frozen=True)
class Feed:
    """
    Represents a feed on SeeThru, every feed requires a feed guid (provided by SeeThru), an api key and a version,
    the version provided will be the version that feed results are pushed with
    """
    feed_guid: UUID
    api_key: ApiKey
    version: str = "1"

    def __post_init__(self):
        """
        Validates the types of the feed fields
        """
        if type(self.feed_guid) != UUID:
            raise InvalidFeedGuid("feed_guid must be of type UUID")
        if type(self.api_key) != ApiKey:
            raise InvalidApiKey("api_key must be of type ApiKey")
        if type(self.version) != str:
            raise TypeError("version must be of type str")

    def get_feed_guid(self):
        return self.feed_guid

    def get_api_key(self):
        return self.api_key

    def push(self, result: FeedResult):
        """
        Pushes the result to SeeThru under the current feed, the version of the feed is pushed with the result

        Args:
            result (FeedResult): The result to push to SeeThru
        """
        headers = {
            "X-Access-Token": str(self.api_key.access_token),
            "X-secret": self.api_key.secret_key
        }
        data = {
            "guid": str(self.feed_guid),
            "color": result.get_status_value(),
            "message": result.message,
            "timestamp": result.get_timestamp_str(),
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
