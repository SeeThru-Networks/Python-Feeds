#!/usr/bin/env python3
import argparse
import importlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path, PurePath
from typing import List, Optional

import toml
from dotenv import load_dotenv

import seethrufeeds.core.config_parser as ConfigParser
from seethrufeeds.model.Feeds import feed
from seethrufeeds.model.Scripts.script_base import ScriptBase
from seethrufeeds.model.Scripts.script_result import ScriptResult
from seethrufeeds.model.Scripts.script_state import StateEngine


class ProgramArgument:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.extra = kwargs


def touch_file(path: str):
    """
    Touches a new file
    Args:
        path: The path to touch the file
    """
    path = os.path.join(path)
    f = open(path, "w")
    f.close()


def create_dir(path: os.path):
    """
    Creates a directory
    Args:
        path: The path of the new directory
    """
    path = os.path.join(path)
    os.mkdir(path)


def get_config_attribute(attribute: str) -> str:
    """
    Replaces all occurrences of $(variable_name) in an attribute with the associated environment variable
    Args:
        attribute: The attribute value

    Returns:
        The attribute
    """
    if type(attribute) != str:
        return attribute
    parts = re.findall(r"\$\([\w\d\-\+]+\)", attribute)
    for arg in parts:
        environment_variable = os.environ.get(arg[2:-1], "")
        attribute = attribute.replace(arg, environment_variable)
    return attribute


class SeeThruFeed:
    Programs = {}

    base_dir: Path
    argv: List[str]
    config_file: Path
    config_method: str

    @classmethod
    def setup_programs(cls):
        cls.Programs = {
            "help": {
                "procedure": SeeThruFeed.display_help,
                "arguments": [],
                "uses_config": False,
                "help": "Displays this help screen"
            },
            "createfeedscheme": {
                "procedure": SeeThruFeed.create_feedscheme,
                "arguments": [
                    ProgramArgument("name", action="store",
                                    type=str, help="The name of the scheme"),
                    ProgramArgument("--path", "-p", action="store", type=str, required=False,
                                    help="The directory to store the feedscheme, defaults to ./name"),
                    ProgramArgument("--no-config", action="store_const", const=True, required=False,
                                    help="Create a scheme without a config file"),
                    ProgramArgument("--config_path", action="store", type=str, required=False,
                                    help="The name of the script to use for the feed"),
                    ProgramArgument("--config_method", action="store", choices=["json", "toml"], type=str, 
                                    required=False, help="The name of the script to use for the feed")
                ],
                "uses_config": False,
                "help": "Create a feed scheme with the given name, this will create the feedscheme in a new directory"
            },
            "createscript": {
                "procedure": SeeThruFeed.create_script,
                "arguments": [
                    ProgramArgument("name", action="store",
                                    type=str, help="The name of the script"),
                    ProgramArgument("--no-config", action="store_const", const=True, required=False,
                                    help="Create the script without a config file")
                ],
                "uses_config": True,
                "help": "Creates a new script in the Scripts/ directory as well as a config file entry"
            },
            "addscript": {
                "procedure": SeeThruFeed.add_script,
                "arguments": [
                    ProgramArgument("name", action="store",
                                    type=str, help="The name of the script"),
                    ProgramArgument("--script", "-s", action="store", required=False,
                                    help="The object import path of the script file to use")
                ],
                "uses_config": True,
                "help": "Add a pre-existing script into the config file"
            },
            "addscriptstate": {
                "procedure": SeeThruFeed.add_scriptstate,
                "arguments": [
                    ProgramArgument("script", action="store", type=str,
                                    help="The name of the script to add the state to"),
                    ProgramArgument("--name", action="store", type=str, required=True,
                                    help="The name of the state"),
                    ProgramArgument("--status", action="store", type=str, required=True,
                                    help="The status to give the state"),
                    ProgramArgument("--message", action="store", type=str, required=True, default="",
                                    help="The message to give the state")
                ],
                "uses_config": True,
                "help": "Add a state to a script"
            },
            "createfeed": {
                "procedure": SeeThruFeed.create_feed,
                "arguments": [
                    ProgramArgument("name", action="store", type=str,
                                    help="The internal name of the feed"),
                    ProgramArgument("--script", "-s", action="store", type=str, required=True,
                                    help="The name of the script to use for the feed"),
                    ProgramArgument("--api-key", "-k", default="apikey", action="store", type=str, required=True,
                                    help="The reference of the apikey to use for the feed"),
                    ProgramArgument("--guid", "-g", action="store", type=str, required=True,
                                    help="The guid of the feed")
                ],
                "uses_config": True,
                "help": "Enters a feed into the config file, using the given script as a source"
            },
            "addapikey": {
                "procedure": SeeThruFeed.add_apikey,
                "arguments": [
                    ProgramArgument("reference", default="apikey", action="store", type=str,
                                    help="The reference to give the apikey"),
                    ProgramArgument("--no-env", action="store_const", const=True, required=False,
                                    help="Create the apikey without storing the token and secret in an env file"),
                    ProgramArgument("--access-token", "-t", action="store", type=str, required=False,
                                    help="The access token of the apikey"),
                    ProgramArgument("--secret", "-s", action="store", type=str, required=False,
                                    help="The secret of the apikey")
                ],
                "uses_config": True,
                "help": "Adds a new api key to the config file, this can be used by feeds to upload results to SeeThru"
            },
            "convert": {
                "procedure": SeeThruFeed.convert_config,
                "arguments": [
                    ProgramArgument("--to", default="json", action="store", type=str,
                                    help="Convert the config file to a new format"),
                    ProgramArgument("--output", "-o", action="store", type=str, required=False,
                                    help="The output file of the new config")
                ],
                "uses_config": True,
                "help": "Converts the config file from one type to another"
            },
            "runfeedscheme": {
                "procedure": SeeThruFeed.run_feedscheme,
                "arguments": [],
                "uses_config": True,
                "help": "Runs the feed scheme defined in the config file and uploaded any feeds"
            },
            "run": {
                "alias": "runfeedscheme",
                "help": "An alias of runfeedscheme"
            }
        }

    def __init__(self, argv=None, base_dir=os.getcwd()):
        """
        Provides the core functionality

        Args:
            argv (List[str]): Command line arguments, if provided, run is automatically ran
            base_dir (Union[str, Path]): The base directory to work from
        """
        SeeThruFeed.setup_programs()
        self.base_dir = Path(base_dir)
        self.argv = []
        self.config_file = Path()
        self.config_method = ""

        # Loads any present env file
        load_dotenv(dotenv_path=os.path.join(base_dir, ".env"))

        if argv is not None:
            self.run(argv)

    def run(self, argv):
        if len(argv) == 1:  # If no arguments were given, print a help Message
            print("Please provide a valid program: ")
            for program in SeeThruFeed.Programs.keys():
                print(f"\t{program}")
            return

        # Removes the first part of the args
        argv = argv[1:]
        self.argv = argv

        # Runs the appropriate program
        if argv[0] in SeeThruFeed.Programs.keys():
            # Gets the program
            programName = argv[0]
            program = SeeThruFeed.Programs[programName]
            argv = argv[1:]

            if "alias" in program:
                programName = program["alias"]
                program = SeeThruFeed.Programs[programName]

            # Creates the argparse program
            parser = argparse.ArgumentParser(prog=programName)
            # Uses every argument defined in the program
            for argument in program["arguments"]:
                parser.add_argument(*argument.args, **argument.extra)
            # If the program uses the config, generic config arguments are added
            if program["uses_config"]:
                # Config path
                parser.add_argument("--config_path", action="store", type=str, required=False,
                                    help="The name of the script to use for the feed")
                # Config method
                parser.add_argument("--config_method", action="store", choices=["json", "toml"], 
                                    type=str, required=False, help="The name of the script to use for the feed")

            # Parses the argument
            args = vars(parser.parse_args(argv))

            # Automatically validates the config file
            if program["uses_config"]:
                path = args["config_path"]
                if type(path) == str:
                    path = Path(path)
                method = args["config_method"]
                self.validate_config_path(path, method)

                del args["config_path"]
                del args["config_method"]

            # Runs the program
            program["procedure"](self, **args)
            return
        else:
            print("Please provide a valid program: ")
            for program in SeeThruFeed.Programs.keys():
                print(f"\t{program}")

    def get_config_path(self):
        """
        Finds a config file and method in the base directory

        Returns:
            bool: Whether a config was found
        """
        for fileName in self.base_dir.iterdir():
            match = re.search(r"(?:\/|\\|^)(?:conf|config).(json|toml)$", fileName.name)
            if match is None:
                continue
            configMethod = match.group(1)
            self.config_file = fileName
            self.config_method = configMethod
            return True
        return False

    def validate_config_path(self, path, method):
        """
        Confirms that the given path and method are valid, if neither are provided, 
        an attempt is made to automatically discover the path and method,
        if only the path is provided, an attemp it made to automatically discover the method.
        The results are stored in self.config_path and self.config_method respectively

        Args:
            path (Path): The config path
            method (str): The config method
        """
        # Attempts to automatically discover a config file
        if path is None:
            if self.get_config_path():
                return
            raise Exception("No config file could be found")

        # Attempts to discover the method
        if method is None:
            # Identifies the config method
            match = re.search(r".(json|toml)$", path.name)
            if match is None:
                raise Exception("The method couldn't be identified from the config path")            
            method = match.group(1)
            
        # Validates the path and method
        if not isinstance(path, PurePath):
            raise TypeError("Path is invalid type")
        if method not in ["json", "toml"]:
            raise TypeError("Please provide a valid method")

        self.config_file = path
        self.config_method = method


    def display_help(self):
        """
        Prints the help screen
        """
        for program in SeeThruFeed.Programs.keys():
            print(f"\t{program} - {SeeThruFeed.Programs[program]['help']}")

    def create_feedscheme(self, name, path=None, no_config=False, config_path=None, config_method=None):
        """
        Creates a new feed scheme of the given name in the
        current working directory

        Arguments:
            name (str): The name of the feed scheme
            no_config (bool): Whether a config file should be generated for the feedscheme
        """
        # Gets the absolute the path
        if path is None:
            path = name
        path = Path(path)
        if not path.is_absolute():
            path = self.base_dir.joinpath(path)

        # Creates the directory structure
        path.mkdir(parents=True, exist_ok=True)

        path.joinpath("__init__.py").touch()
        path.joinpath("Scripts").mkdir()
        path.joinpath("Scripts/__init__.py").touch()
        path.joinpath("Scripts/Vendor").mkdir()
        path.joinpath("Scripts/Vendor/__init__.py").touch()
        path.joinpath("Components").mkdir()
        path.joinpath("Components/__init__.py").touch()
        path.joinpath("Components/Vendor").mkdir()
        path.joinpath("Components/Vendor/__init__.py").touch()
        path.joinpath("Outputs").mkdir()

        # Creates the new manager
        templatePath = Path(__file__).parent.joinpath("templates/Manage_Template.template")
        with open(templatePath, "r") as managerTemplate:
            template = managerTemplate.read()
            
        with open(path.joinpath("manage.py"), "w") as manager:
            manager.write(template)

        if no_config:
            return

        # Validates the config path
        if config_path is None:
            if config_method is None:
                config_method = "json"
            config_path = path.joinpath("config." + config_method)

        self.validate_config_path(config_path, config_method)
        # Creates a config
        config = ConfigParser.Config.new(name)
        ConfigParser.ConfigParser(self.config_file, self.config_method).set_config(config).save()

    def create_script(self, name, no_config=False):
        """
        Creates a new script and adds the script to the config file

        Args:
            name (str): The name of the script
            no_config (bool): Whether the script should be added to the config file
        """
        # Creates the new script
        with open(Path(__file__).parent.joinpath("templates/Script_Template.template"), 'r') as scriptTemplate:
            template = scriptTemplate.read()
        # Sets the default information
        template = template.replace(r"{{ Script_Name }}", name)
        with open(self.base_dir.joinpath(f"Scripts/{name}.py"), "w") as script:
            script.write(template)

        if no_config:
            return

        # Loads the config file
        with ConfigParser.ConfigParser(self.config_file, self.config_method) as config:
            # Creates a new script
            config.add_script(name)

    def add_script(self, name, script=None):
        with ConfigParser.ConfigParser(self.config_file, self.config_method) as config:
            configScript = config.add_script(name)
            if script is not None:
                configScript.Meta.Script_Object_Path = script

    def add_scriptstate(self, script, name, status, message):
        # Loads the config file
        with ConfigParser.ConfigParser(self.config_file, self.config_method) as config:
            if script not in config.Scripts:
                # TODO: Show error message
                return
            config.Scripts[script].add_state(name, status, message)

    def run_feedscheme(self):
        """
        Runs the feed scheme
        """
        # Opens the config file and parses it
        config = ConfigParser.ConfigParser(self.config_file, self.config_method).load()

        if len(config.Scripts) == 0:
            # TODO: Show error message
            return

        scriptResults = {}

        for key, script in config.Scripts.items():
            scriptName = get_config_attribute(script.Meta.Script_Name)

            # Splits the object's module and the object's name from the Script_Object_Path
            objectComponents = get_config_attribute(script.Meta.Script_Object_Path).split('@')
            if len(objectComponents) != 2:
                # TODO: Show error message
                return
            objectModule, objectName = tuple(objectComponents)

            # Dynamically imports the script
            scriptModule = importlib.import_module(objectModule)
            if objectName not in dir(scriptModule):
                # TODO: Show error message
                return
            scriptClass = getattr(scriptModule, objectName)
            # Instantiates the script
            scriptInstance: ScriptBase = scriptClass()

            # Sets any fillables defined
            for key, fillable in script.Fillables.items():
                # Gets all defined environment variables
                  
                # TODO: Perform conversion on different value types
                value = get_config_attribute(fillable)

                # Assigns the fillable to the script
                scriptInstance.set_property(key, fillable)

            # Gets any state defined
            for key, value in script.States.items():
                if isinstance(scriptInstance, StateEngine):
                    # Configures the state to the script
                    scriptInstance: StateEngine
                    try:
                        scriptInstance.configure_state(key, value.Status, value.Message)
                    except ValueError as _:
                        print("Please provide a valid status of either 'red', 'amber' or 'green'. This state will not be used")

            scriptInstance.set_internal_alias(scriptName)
            # Runs the script
            scriptInstance.set_output_path(script.Meta.Script_Output_Path)
            scriptInstance.run_script()
            scriptInstance.evaluate_script()
            scriptInstance.log_output()
            scriptInstance.export_to_output()

            scriptResults[scriptName] = scriptInstance.get_result()

        # Goes through every feed
        if len(config.Feeds) == 0:
            return
        if len(config.Api_Keys):
            return
        for key, feed in config.Feeds.items():
            if feed.Script not in scriptResults:
                continue
            # Gets the api key
            if feed.Api_Key not in config.Api_Keys:
                continue
            accessToken = get_config_attribute(config.Api_Keys[feed.Api_Key].Access_Token)
            secret = get_config_attribute(config.Api_Keys[feed.Api_Key].Secret)

            result = scriptResults[feed.Script]

            # Pushes the script result
            feed = feed.Feed()
            feed.set_guid(feed.Guid)
            feed.set_api_key(accessToken, secret)
            feed.set_script_result(result)
            result = feed.push()
            if result != "":
                print(f"Feed push failed with message: {result}")

    def create_feed(self, name, script, api_key, guid):
        """
        Creates a new feed entry in the config file
        Args:
            name: The internal name of the feed (Internal use only)
            script: The name of the script that this feed uses
            api_key: The reference to the api key to use
            guid: The guid of the feed
        """
        # Loads the config file
        with ConfigParser.ConfigParser(self.config_file, self.config_method) as config:
            # Adds the feed to the config
            config.add_feed(name, script, api_key, guid)

    def add_apikey(self, reference, no_env, access_token, secret):
        """
        Adds an api key to the config file
        Args:
            reference (str): The reference to give the api key
            no_env (bool): If true, the access_toke and secret aren't required and aren't added to the env file
            access_token (str): The access token of the api key
            secret (str): The secret of the api key
        """
        # Only gets the access token and secret if an env file is wanted to store them in
        if no_env is None:
            if access_token is None:
                access_token = input("Please enter the access token: ")
            if secret is None:
                secret = input("Please enter the secret: ")

        # Loads the config file
        with ConfigParser.ConfigParser(self.config_file, self.config_method) as config:
            # Adds the reference to the env file in the config
            config.add_api_key(
                reference,
                f"$({reference.upper()}_ACCESS_TOKEN)",
                f"$({reference.upper()}_SECRET)"
            )

        # Adds the access token and secret to the env file
        if no_env is None:
            envFile = open(os.path.join(self.base_dir, ".env"), "a")
            envFile.write(f"{reference.upper()}_ACCESS_TOKEN={access_token}\n")
            envFile.write(f"{reference.upper()}_SECRET={secret}\n")

    def convert_config(self, to, output=None):
        if to not in ["json", "toml"]:
            print("Please provide a valid method")
            return

        parser = ConfigParser.ConfigParser(
            self.config_file, self.config_method)
        parser.load()
        parser.method = to
        parser.config_path = Path(output)
        parser.save()


def exec():
    """
    Provides an entry point for the command line utility
    """
    SeeThruFeed(sys.argv)
