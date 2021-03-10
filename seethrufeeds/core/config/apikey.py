from seethrufeeds.core.exceptions import config as ConfigExceptions

class ApiKey:
    Access_Token: str
    Secret: str

    def __init__(self, access_token, secret):
        self.Access_Token = access_token
        self.Secret = secret

    @staticmethod
    def new(access_token: str, secret: str) -> "ApiKey":
        """
            Creates a new api key, with given attributes

            Args:
                access_token (str): The access token
                secret (str): The secret key

            Returns:
                ApiKey: The new api key
            """
        return ApiKey(access_token, secret)

    @staticmethod
    def load(data: dict, name: str) -> "ApiKey":
        """
        Parses the given data into an api key

        Args:
            data: The data to parse
            name: The name of the api key

        Returns:
            ApiKey: The new api key
        """
        if "Access_Token" not in data:
            raise ConfigExceptions.ApiKeyException(f"There is no access_token", name)
        if "Secret" not in data:
            raise ConfigExceptions.ApiKeyException(f"There is no secret", name)
        return ApiKey(
            data["Access_Token"],
            data["Secret"]
        )

    def dump(self) -> dict:
        """
        Dumps the api key into a dictionary

        Returns:
            dict: The dumped data
        """
        return {
            "Access_Token": self.Access_Token,
            "Secret": self.Secret
        }
