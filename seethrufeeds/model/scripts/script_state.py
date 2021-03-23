"""
Stores script state
A script can choose to use states rather than an evaluation method,
the script state gets set during the script runtime
Each state has a default status and message, these can be overwritten elsewhere if a custom status or message is needed
"""
from dataclasses import dataclass
from enum import Enum
from seethrufeeds.feeds.feed_result import FeedStatusEnum


@dataclass(frozen=True)
class State:
    status: FeedStatusEnum
    message: str


class StatesEnum(Enum):
    """
    Defines the possible states that a script can have
    """
    ok = State(FeedStatusEnum.green, "")
    warning = State(FeedStatusEnum.amber, "Warning message")
    error = State(FeedStatusEnum.red, "Error message")
