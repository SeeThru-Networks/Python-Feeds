from seethrufeeds.core.exceptions import config as ConfigExceptions

class Feed:
    Script: str
    Api_Key: str
    Guid: str

    def __init__(self, _script, api_key, guid):
        self.Script = _script
        self.Api_Key = api_key
        self.Guid = guid

    @staticmethod
    def new(_script: str, api_key: str, guid: str) -> "Feed":
        """
            Creates a new feed, with given attributes

            Args:
                _script (str): The name of the script that the feed refers to
                api_key (str): The name of the api key to use for the feed
                guid (str): The guid of the feed

            Returns:
                Feed: The new feed
            """
        return Feed(_script, api_key, guid)

    @staticmethod
    def load(data: dict, name: str) -> "Feed":
        """
        Parses the given data into a feed

        Args:
            data: The data to parse
            name: The feed name

        Returns:
            Feed: The new model
        """
        if "Script" not in data:
            raise ConfigExceptions.FeedException("There is no script defined", name)
        if "Api_Key" not in data:
            raise ConfigExceptions.FeedException("There is no api_key defined", name)
        if "Guid" not in data:
            raise ConfigExceptions.FeedException("There is no guid defined", name)
        return Feed(
            data["Script"],
            data["Api_Key"],
            data["Guid"]
        )

    def dump(self) -> dict:
        """
        Dumps the feed into a dictionary

        Returns:
            dict: The dumped data
        """
        return {
            "Script": self.Script,
            "Api_Key": self.Api_Key,
            "Guid": self.Guid
        }
