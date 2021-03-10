from typing import Dict

from . import header as ConfigHeader, script as ConfigScript, feed as ConfigFeed, apikey as ConfigApiKey

from seethrufeeds.core.exceptions import config as ConfigExceptions

class Config:
    Header: "ConfigHeader.Header"
    Scripts: Dict[str, "ConfigScript.Script"]
    Feeds: Dict[str, "ConfigFeed"]
    Api_Keys: Dict[str, "ConfigApiKey.ApiKey"]

    def __init__(self,
                 header: "ConfigHeader.Header",
                 scripts: Dict[str, "ConfigScript.Script"],
                 feeds: Dict[str, "ConfigFeed.Feed"],
                 api_keys: Dict[str, "ConfigApiKey.ApiKey"]):
        self.Header = header
        self.Scripts = scripts
        self.Feeds = feeds
        self.Api_Keys = api_keys

    @staticmethod
    def new(name: str) -> "Config":
        """
        Creates a new config, with newly generated attributes

        Args:
            name (str): The name of the feedscheme

        Returns:
            Config: The new config
        """
        header = ConfigHeader.Header.new(name)
        return Config(header, {}, {}, {})

    def add_script(self, name: str) -> ConfigScript:
        """
        Adds a script to the config

        Args:
            name (str): The name of the script

        Returns:
            Script: The new script
        """
        configscript = ConfigScript.Script.new(name)
        self.Scripts[name] = configscript
        return configscript

    def add_feed(self, name: str, _script: str, api_key: str, guid: str) -> "ConfigFeed.Feed":
        """
        Adds a feed to the config

        Args:
            name (str): The name of the feed
            _script (str): The name of the script that the feed uses
            api_key (str): The name of the api key that the feed uses
            guid (str): The guid of the feed

        Returns:
            Feed: The new feed
        """
        feed = ConfigFeed.Feed.new(_script, api_key, guid)
        self.Feeds[name] = feed
        return feed

    def add_api_key(self, name: str, access_token: str, secret: str) -> ConfigApiKey.ApiKey:
        """
        Adds an api key to the config

        Args:
            name (str): The name of the api key
            access_token (str): The access token of the api key
            secret (str): The secret key of the api key

        Returns:
            ApiKey: The new api key
        """
        api_key = ConfigApiKey.ApiKey.new(access_token, secret)
        self.Api_Keys[name] = api_key
        return api_key

    @staticmethod
    def load(data: dict) -> "Config":
        if "Header" in data:
            header = ConfigHeader.Header.load(data["Header"])
        else:
            raise ConfigExceptions.ConfigException("No header provided")
        scripts = {}
        if "Scripts" in data:
            if type(data["Scripts"]) != dict:
                raise ConfigExceptions.ConfigException("Config has invalid scripts")
            scripts = {
                key: ConfigScript.Script.load(data["Scripts"][key], key) for key in data["Scripts"].keys()
            }
        feeds = {}
        if "Feeds" in data:
            if type(data["Feeds"]) != dict:
                raise ConfigExceptions.ConfigException("Config has invalid feeds")
            feeds = {
                key: ConfigFeed.Feed.load(data["Feeds"][key], key) for key in data["Feeds"].keys()
            }
        api_keys = {}
        if "Api_Keys" in data:
            if type(data["Api_Keys"]) != dict:
                raise ConfigExceptions.ConfigException("Config has invalid api_keys")
            api_keys = {
                key: ConfigApiKey.ApiKey.load(data["Api_Keys"][key], key) for key in data["Api_Keys"].keys()
            }
        return Config(
            header,
            scripts,
            feeds,
            api_keys
        )

    def dump(self) -> dict:
        data = {
            "Header": self.Header.dump()
        }
        if len(self.Scripts) != 0:
            data["Scripts"] = {
                key: self.Scripts[key].dump() for key in self.Scripts.keys()
            }
        if len(self.Feeds) != 0:
            data["Feeds"] = {
                key: self.Feeds[key].dump() for key in self.Feeds.keys()
            }
        if len(self.Api_Keys) != 0:
            data["Api_Keys"] = {
                key: self.Api_Keys[key].dump() for key in self.Api_Keys.keys()
            }
        return data
