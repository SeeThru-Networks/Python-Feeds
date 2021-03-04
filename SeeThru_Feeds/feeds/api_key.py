import os
import re
from dataclasses import dataclass
from uuid import UUID

from .exceptions import SecretKeyDoesNotExist, InvalidSecretKey, AccessTokenDoesNotExist, InvalidAccessToken


@dataclass(frozen=True)
class ApiKey:
    """
    Stores the api credentials used for the SeeThru api.
    It is recommended to store these in environment variables as they can be easily loaded with ApiKey.from_env
    """
    access_token: UUID
    secret_key: str

    def __post_init__(self):
        """
        Validates the types of the credentials given
        """
        if type(self.access_token) != UUID:
            raise InvalidAccessToken("access_token must be of type UUID")
        if type(self.secret_key) != str:
            raise InvalidSecretKey("secret_key must be of type str")

        # Validates the secret key
        if not re.search("^[0-9a-fA-F]{64}?$", self.secret_key):
            raise InvalidSecretKey("secret_key must be a string of 64 hex characters")

    def get_access_token(self):
        return self.access_token

    def get_secret_key(self):
        return self.secret_key

    @staticmethod
    def from_env(access_token_name: str = "ACCESS_TOKEN", secret_key_name: str = "SECRET_KEY") -> "ApiKey":
        """
        Reads the api key from the environment

        Args:
            access_token_name (str): The name of the access token in the environment
            secret_key_name (str): The name of the secret key in the environment

        Returns:
            ApiKey: A new apikey
        """
        access = os.environ.get(access_token_name, None)
        secret = os.environ.get(secret_key_name, None)
        if access is None:
            raise AccessTokenDoesNotExist()
        if secret is None:
            raise SecretKeyDoesNotExist()

        try:
            access = UUID(access)
        except ValueError:
            raise InvalidAccessToken("access_token must be a valid GUID")

        return ApiKey(access_token=access, secret_key=secret)
