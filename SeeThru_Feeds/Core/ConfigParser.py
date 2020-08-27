import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

import toml


class ConfigPart:
    @staticmethod
    def load(data: dict) -> "ConfigPart":
        """
        Converts a dictionary representation of a config part to the object model

        Args:
            data (dict): The dictionary representation

        Returns:
            ConfigPart: The object model
        """
        return ConfigPart()

    def dump(self) -> dict:
        """
        Converts the config part to a dictionary representation

        Returns:
            dict: The dictionary representation of the config part
        """
        return {}


class ConfigHeader(ConfigPart):
    Scheme_Name: str
    Scheme_Description: str
    Scheme_Author: str
    Scheme_Owner: str
    Creation_Date: str

    def __init__(self, name: str, description: str, author: str, owner: str, creation_date: str):
        self.Scheme_Name = name
        self.Scheme_Description = description
        self.Scheme_Author = author
        self.Scheme_Owner = owner
        self.Creation_Date = creation_date

    @staticmethod
    def new(name: str) -> "ConfigHeader":
        """
        Creates a new config header, with default attributes

        Args:
            name (str): The name of the feedscheme

        Returns:
            ConfigHeader: The new header
        """
        description = "Enter a description for your feed scheme"
        author = "Enter the author of your feed scheme"
        owner = "Enter the owner for your feed scheme"
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return ConfigHeader(name, description, author, owner, creation_date)

    @staticmethod
    def load(data: dict) -> "ConfigHeader":
        if "Scheme_Name" not in data:
            raise Exception()  # TODO: Handle error properly
        if "Scheme_Description" not in data:
            raise Exception()  # TODO: Handle error properly
        if "Scheme_Author" not in data:
            raise Exception()  # TODO: Handle error properly
        if "Scheme_Owner" not in data:
            raise Exception()  # TODO: Handle error properly
        if "Creation_Date" not in data:
            raise Exception()  # TODO: Handle error properly
        return ConfigHeader(
            data["Scheme_Name"],
            data["Scheme_Description"],
            data["Scheme_Author"],
            data["Scheme_Owner"],
            data["Creation_Date"]
        )

    def dump(self) -> dict:
        return {
            "Scheme_Name": self.Scheme_Name,
            "Scheme_Description": self.Scheme_Description,
            "Scheme_Author": self.Scheme_Author,
            "Scheme_Owner": self.Scheme_Owner,
            "Creation_Date": self.Creation_Date
        }


class ScriptMeta(ConfigPart):
    Script_Name: str
    Script_Output_Path: str
    Script_Object_Path: str

    def __init__(self, name: str, output_path: str, object_path: str):
        self.Script_Name = name
        self.Script_Output_Path = output_path
        self.Script_Object_Path = object_path

    @staticmethod
    def new(name: str) -> "ScriptMeta":
        """
        Creates a new script meta, with attributes derived from the name

        Args:
            name (str): The name of the script

        Returns:
            ScriptMeta: The new script meta
        """
        output_path = f"Outputs/{name}"
        object_path = f"Scripts.{name}@{name}"
        return ScriptMeta(name, output_path, object_path)

    @staticmethod
    def load(data: dict) -> "ScriptMeta":
        if "Script_Name" not in data:
            raise Exception()  # TODO: Handle error properly
        if "Script_Output_Path" not in data:
            raise Exception()  # TODO: Handle error properly
        if "Script_Object_Path" not in data:
            raise Exception()  # TODO: Handle error properly
        return ScriptMeta(
            data["Script_Name"],
            data["Script_Output_Path"],
            data["Script_Object_Path"]
        )

    def dump(self) -> dict:
        return {
            "Script_Name": self.Script_Name,
            "Script_Output_Path": self.Script_Output_Path,
            "Script_Object_Path": self.Script_Object_Path
        }


class ScriptState(ConfigPart):
    Name: str
    Status: str
    Message: str

    def __init__(self, name: str, status: str, message: str):
        self.Name = name
        self.Status = status
        self.Message = message

    @staticmethod
    def new(name: str, status: str, message: str) -> "ScriptState":
        """
                Creates a new script state, with given attributes

                Args:
                    name (str): The name of the state
                    status (str): The status to give the script state
                    message (str): The message to give the script state

                Returns:
                    ScriptState: The new script state

                """
        return ScriptState(name, status, message)

    @staticmethod
    def load(data: dict) -> "ScriptState":
        if "Name" not in data:
            raise Exception()  # TODO: Handle error properly
        if "Status" not in data:
            raise Exception()  # TODO: Handle error properly
        if "Message" not in data:
            raise Exception()  # TODO: Handle error properly
        return ScriptState(
            data["Name"],
            data["Status"],
            data["Message"]
        )

    def dump(self) -> dict:
        return {
            "Name": self.Name,
            "Status": self.Status,
            "Message": self.Message
        }


class ConfigScript(ConfigPart):
    Meta: "ScriptMeta"
    Fillables: Dict[str, Any]
    States: Dict[str, "ScriptState"]

    def __init__(self,
                 meta: "ScriptMeta",
                 fillables: Dict[str, Any],
                 states: Dict[str, "ScriptState"]):
        self.Meta = meta
        self.Fillables = fillables
        self.States = states

    @staticmethod
    def new(name: str) -> "ConfigScript":
        """
            Creates a new script, with default attributes

            Args:
                name (str): The name of the script

            Returns:
                ConfigScript: The new script
            """
        meta = ScriptMeta.new(name)
        return ConfigScript(meta, {}, {})

    def add_fillable(self, name: str, value: Any) -> Any:
        """
            Adds a new fillable to the script

            Args:
                name (str): The name of the fillable
                value (Any): The value to give the fillable

            Returns:
                Any: The value
            """
        self.Fillables[name] = value
        return value

    def add_state(self, name: str, status: str, message: str) -> ScriptState:
        """
            Adds a new state to the script

            Args:
                name (str): The name of the state
                status (str): The status to give the script state
                message (str): The message to give the script state

            Returns:
                ScriptState: The new state
            """
        state = ScriptState.new(name, status, message)
        self.States[name] = state
        return state

    @staticmethod
    def load(data: dict) -> "ConfigScript":
        # Loads the meta
        if "Meta" in data:
            meta = ScriptMeta.load(data["Meta"])
        else:
            raise Exception()  # TODO: Handle error properly
        # Loads the fillable properties set
        fillables = {}
        if "Fillables" in data:
            fillables = data["Fillables"]
        # Loads the script states
        states = {}
        if "States" in data:
            states = data["States"]
            if type(states) != dict:
                raise Exception()
            # Loads the state into internal object model
            states = {
                key: ScriptState.load(states[key]) for key in states.keys()
            }
        return ConfigScript(
            meta,
            fillables,
            states
        )

    def dump(self) -> dict:
        data = {
            "Meta": self.Meta.dump()
        }
        if len(self.Fillables) != 0:
            data["Fillables"] = self.Fillables
        if len(self.States) != 0:
            # Turns internal representation of state into dictionary
            data["States"] = {
                key: self.States[key].dump() for key in self.States.keys()
            }
        return data


class ApiKey(ConfigPart):
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
    def load(data: dict) -> "ApiKey":
        if "Access_Token" not in data:
            raise Exception()  # TODO: Handle error properly
        if "Secret" not in data:
            raise Exception()  # TODO: Handle error properly
        return ApiKey(
            data["Access_Token"],
            data["Secret"]
        )

    def dump(self) -> dict:
        return {
            "Access_Token": self.Access_Token,
            "Secret": self.Secret
        }


class Feed(ConfigPart):
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
    def load(data: dict) -> "Feed":
        if "Script" not in data:
            raise Exception()  # TODO: Handle error properly
        if "Api_Key" not in data:
            raise Exception()  # TODO: Handle error properly
        if "Guid" not in data:
            raise Exception()  # TODO: Handle error properly
        return Feed(
            data["Script"],
            data["Api_Key"],
            data["Guid"]
        )

    def dump(self) -> dict:
        return {
            "Script": self.Script,
            "Api_Key": self.Api_Key,
            "Guid": self.Guid
        }


class Config(ConfigPart):
    Header: "ConfigHeader"
    Scripts: Dict[str, "ConfigScript"]
    Feeds: Dict[str, "Feed"]
    Api_Keys: Dict[str, "ApiKey"]

    def __init__(self,
                 header: "ConfigHeader",
                 scripts: Dict[str, "ConfigScript"],
                 feeds: Dict[str, "Feed"],
                 api_keys: Dict[str, "ApiKey"]):
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
        header = ConfigHeader.new(name)
        return Config(header, {}, {}, {})

    def add_script(self, name: str) -> ConfigScript:
        """
        Adds a script to the config

        Args:
            name (str): The name of the script

        Returns:
            ConfigScript: The new script
        """
        configscript = ConfigScript.new(name)
        self.Scripts[name] = configscript
        return configscript

    def add_feed(self, name: str, _script: str, api_key: str, guid: str) -> Feed:
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
        feed = Feed.new(_script, api_key, guid)
        self.Feeds[name] = feed
        return feed

    def add_api_key(self, name: str, access_token: str, secret: str) -> ApiKey:
        """
        Adds an api key to the config

        Args:
            name (str): The name of the api key
            access_token (str): The access token of the api key
            secret (str): The secret key of the api key

        Returns:
            ApiKey: The new api key
        """
        api_key = ApiKey.new(access_token, secret)
        self.Api_Keys[name] = api_key
        return api_key

    @staticmethod
    def load(data: dict) -> "Config":
        if "Header" in data:
            header = ConfigHeader.load(data["Header"])
        else:
            raise Exception()  # TODO: Handle error properly
        scripts = {}
        if "Scripts" in data:
            if type(data["Scripts"]) != dict:
                raise Exception()
            scripts = {
                key: ConfigScript.load(data["Scripts"][key]) for key in data["Scripts"].keys()
            }
        feeds = {}
        if "Feeds" in data:
            if type(data["Feeds"]) != dict:
                raise Exception()
            feeds = {
                key: Feed.load(data["Feeds"][key]) for key in data["Feeds"].keys()
            }
        api_keys = {}
        if "Api_Keys" in data:
            if type(data["Api_Keys"]) != dict:
                raise Exception()
            api_keys = {
                key: ApiKey.load(data["Api_Keys"][key]) for key in data["Api_Keys"].keys()
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


class ConfigParser:
    def __init__(self, config_path: Path, method: str = "json"):
        self.config_path: Path = config_path
        self.method: str = method
        self.config: Config = Config.new("")

    @staticmethod
    def json(config_path: Path):
        """
        Creates and sets the parser's type to json

        Args:
            config_path (Path):The config file path

        Returns:
            ConfigParser: The parser
        """
        return ConfigParser(config_path, "json")

    @staticmethod
    def toml(config_path: Path):
        """
        Creates and sets the parser's type to toml

        Args:
            config_path (Path):The config file path

        Returns:
            ConfigParser: The parser
        """
        return ConfigParser(config_path, "toml")

    def set_config(self, config: Config):
        """
        Sets the config to the parser

        Args:
            config (Config): The config

        Returns:
            ConfigParser: The parser
        """
        self.config = config
        return self

    def load(self):
        """
        Opens the config file and parses it into the object model

        Returns:
            Config: The config
        """
        # Opens the config file and parses it
        if not self.config_path.exists():
            return self.config
        with self.config_path.open('r') as file:
            if self.method == "json":
                # Generates the config
                data = json.loads(file.read())
                self.config = Config.load(data)
                return self.config
            elif self.method == "toml":
                # Generates the config
                data = toml.loads(file.read())
                self.config = Config.load(data)
                return self.config
            # TODO: Throw error
            return self.config

    def save(self):
        """
        Saves the config file, with the appropriate type
        """
        if not self.config_path.parent.exists():
            return
        with self.config_path.open('w') as file:
            content = ""
            if self.method == "json":
                content = json.dumps(self.config.dump())
            elif self.method == "toml":
                content = toml.dumps(self.config.dump())
            file.write(content)

    def __enter__(self):
        return self.load()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()


if __name__ == "__main__":
    # config = Config.new("Generic")
    # script = config.add_script("Google")
    # script.add_fillable("HOST", "192.168.0.1")
    #
    # output = config.dump()
    # print(output)

    with ConfigParser.toml(Path("./config.toml")) as config:
        breakpoint()
