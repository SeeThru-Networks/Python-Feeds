import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from .exceptions import config as ConfigExceptions
from .config import Config

import toml


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
            data = {}
            if self.method == "json":
                # Generates the config
                data = json.loads(file.read())
            elif self.method == "toml":
                # Generates the config
                data = toml.loads(file.read())

        try:
            self.config = Config.load(data)
            return self.config
        except ConfigExceptions.ScriptException as e:
            print(f"{e.script_name}: {e}")
            sys.exit(1)
        except ConfigExceptions.FeedException as e:
            print(f"{e.name}: {e}")
            sys.exit(1)
        except ConfigExceptions.ApiKeyException as e:
            print(f"{e.name}: {e}")
            sys.exit(1)
        except ConfigExceptions.ConfigException as e:
            print(e)
            sys.exit(1)

    def save(self):
        """
        Saves the config file, with the appropriate type
        """
        if not self.config_path.parent.exists():
            return
        with self.config_path.open('w') as file:
            content = ""
            if self.method == "json":
                content = json.dumps(self.config.dump(), indent=4)
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
