from datetime import datetime, timezone
from enum import Enum


class FeedStatusEnum(Enum):
    green = "green"
    amber = "amber"
    red = "red"
    default = "default"

    # Links to colours
    ok = green
    warning = amber
    error = red


class FeedResult:
    """
    Stores a feed result that can be transferred to SeeThru via the api,
    the timestamp provided can be any timezone but will be converted to utc upon pushing
    """
    # Containers of the true values
    _status: FeedStatusEnum
    _message: str
    _timestamp: datetime

    def __init__(self, status: FeedStatusEnum, message: str, timestamp: datetime = None):
        """
        Args:
            status (FeedStatusEnum): The status of the result
            message (str): The message of the result
            timestamp (datetime): The timestamp of the result, defaults to utc now
        """
        self.status = status
        self.message = message
        if timestamp is None:
            self.timestamp = datetime.now()
        else:
            self.timestamp = timestamp

    @property
    def status(self) -> FeedStatusEnum:
        return self._status

    @status.setter
    def status(self, status: FeedStatusEnum):
        if status not in FeedStatusEnum:
            raise TypeError("status must be of type FeedStatusEnum")
        self._status = status

    def get_status(self) -> FeedStatusEnum:
        return self.status

    def get_status_value(self) -> str:
        """
        Gets the value attached to the status enum

        Returns:
            The colour value
        """
        return self.status.value

    @property
    def message(self) -> str:
        return self._message

    @message.setter
    def message(self, message: str):
        if type(message) != str:
            raise TypeError("message must be of type string")
        self._message = message

    def get_message(self) -> str:
        return self.message

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp: datetime):
        """
        Converts the given timezone to utc and sets it

        Args:
            timestamp (datetime): The timezone to be converted to utc
        """
        if type(timestamp) != datetime:
            raise TypeError("timestamp must be of type datetime")
        self._timestamp = timestamp.astimezone(tz=timezone.utc)

    def get_timestamp(self) -> datetime:
        return self.timestamp

    def get_timestamp_str(self) -> str:
        """
        Returns a %Y-%m-%d %H:%M:%S formatted timestamp

        Returns:
            str: The formatted timestamp
        """
        return self._timestamp.astimezone(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

