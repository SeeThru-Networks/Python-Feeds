#!/usr/bin/env python3
from pathlib import Path

from SeeThru_Feeds.Model.Feeds import Feed
from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptBase
from SeeThru_Feeds.Model.Scripts.ScriptResult import ScriptResult
import SeeThru_Feeds.Core.ConfigParser as ConfigParser

import argparse
import importlib
import os
import sys
import re
from datetime import datetime

import toml
from dotenv import load_dotenv

from SeeThru_Feeds.Model.Scripts.ScriptState import StateEngine


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
    path = os.path.join(SeeThruFeed.Base_Dir, path)
    f = open(path, "w")
    f.close()


def create_dir(path: os.path):
    """
    Creates a directory
    Args:
        path: The path of the new directory
    """
    path = os.path.join(SeeThruFeed.Base_Dir, path)
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
    Base_Dir = os.getcwd()
    Programs = {}

    @classmethod
    def setup_programs(cls):
        cls.Programs = {
            "help": {
                "procedure": SeeThruFeed.display_help,
                "arguments": [],
                "help": "Displays this help screen"
            },
            "createfeedscheme": {
                "procedure": SeeThruFeed.create_feedscheme,
                "arguments": [
                    ProgramArgument("name", action="store", type=str, help="The name of the scheme"),
                    ProgramArgument("path", action="store", type=str,
                                    help="The directory to store the feedscheme, defaults to ./name"),
                    ProgramArgument("--no-config", action="store_const", const=True, required=False,
                                    help="Create a scheme without a config file"),
                ],
                "help": "Create a feed scheme with the given name, this will create the feedscheme in a new directory"
            },
            "createscript": {
                "procedure": SeeThruFeed.create_script,
                "arguments": [
                    ProgramArgument("name", action="store", type=str, help="The name of the script"),
                    ProgramArgument("--no-config", action="store_const", const=True, required=False,
                                    help="Create the script without a config file")
                ],
                "help": "Creates a new script in the Scripts/ directory as well as a config file entry"
            },
            "addscript": {
                "procedure": SeeThruFeed.add_script,
                "arguments": [
                    ProgramArgument("name", action="store", type=str, help="The name of the script")
                ],
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
                "help": "Add a state to a script"
            },
            "createfeed": {
                "procedure": SeeThruFeed.create_feed,
                "arguments": [
                    ProgramArgument("name", action="store", type=str, help="The internal name of the feed"),
                    ProgramArgument("--script", "-s", action="store", type=str, required=True,
                                    help="The name of the script to use for the feed"),
                    ProgramArgument("--api-key", "-k", default="apikey", action="store", type=str, required=True,
                                    help="The reference of the apikey to use for the feed"),
                    ProgramArgument("--guid", "-g", action="store", type=str, required=True,
                                    help="The guid of the feed")
                ],
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
                "help": "Adds a new api key to the config file, this can be used by feeds to upload results to SeeThru"
            },
            "runfeedscheme": {
                "procedure": SeeThruFeed.run_feedscheme,
                "arguments": [],
                "help": "Runs the feed scheme defined in the config file and uploaded any feeds"
            },
            "run": {
                "alias": "runfeedscheme",
                "help": "An alias of runfeedscheme"
            }
        }

    def __init__(self, argv, base_dir=os.getcwd()):
        """
        Provides the core functionality

        Arguments:
            argv {[string]} -- The cli args
            base_dir {string} -- The base directory to work from
        """
        SeeThruFeed.Base_Dir = base_dir
        SeeThruFeed.setup_programs()
        self.argv = argv

        if len(argv) == 1:  # If no arguments were given, print a help Message
            print("Please provide a valid program: ")
            for program in SeeThruFeed.Programs.keys():
                print(f"\t{program}")
            return

        # Loads any present env file
        load_dotenv(dotenv_path=os.path.join(SeeThruFeed.Base_Dir, ".env"))

        # Runs the appropriate program
        if argv[1] in SeeThruFeed.Programs.keys():
            # Gets the program
            programName = argv[1]
            program = SeeThruFeed.Programs[programName]
            argv = argv[2:]

            if "alias" in program:
                programName = program["alias"]
                program = SeeThruFeed.Programs[programName]

            # Creates the argparse program
            parser = argparse.ArgumentParser(prog=programName)
            # For every argument defined in the program
            for argument in program["arguments"]:
                parser.add_argument(*argument.args, **argument.extra)
            # Parses the arguments
            args = parser.parse_args(argv)

            # Runs the program
            program["procedure"](self, **vars(args))
            return
        else:
            print("Please provide a valid program: ")
            for program in SeeThruFeed.Programs.keys():
                print(f"\t{program}")

    def display_help(self):
        """
        Prints the help screen
        """
        for program in SeeThruFeed.Programs.keys():
            print(f"\t{program} - {SeeThruFeed.Programs[program]['help']}")

    def create_feedscheme(self, name, path=None, no_config=False):
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
            path = Path(SeeThruFeed.Base_Dir).joinpath(path)

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

        # Creates the new script
        templatePath = Path(__file__).parent.joinpath("templates/Manage_Template.template")
        scriptFile = open(templatePath, 'r')
        scriptTemplate = scriptFile.read()
        # Opens the new script file
        newScript = open(path.joinpath("manage.py"), "w")
        newScript.write(scriptTemplate)
        # Closes the files
        newScript.close()
        scriptFile.close()

        if no_config:
            return

        # Creates a config
        config = ConfigParser.Config.new(name)
        ConfigParser.ConfigParser.toml(path.joinpath('config.toml')).set_config(config).save()

    def create_script(self, name, no_config=False):
        """
        Creates a new script and adds the script to the config file

        Args:
            name (str): The name of the script
            no_config (bool): Whether the script should be added to the config file
        """
        # Creates the new script
        scriptFile = open(os.path.join(os.path.dirname(__file__), 'templates/Script_Template.template'), 'r')
        scriptTemplate = scriptFile.read()
        # Sets the default information
        scriptTemplate = scriptTemplate.replace(r"{{ Script_Name }}", name)
        # Opens the new script file
        newScript = open(os.path.join(SeeThruFeed.Base_Dir, f"Scripts/{name}.py"), "w")
        newScript.write(scriptTemplate)
        # Closes the files
        newScript.close()
        scriptFile.close()

        if no_config:
            return

        # Loads the config file
        with ConfigParser.ConfigParser.toml(Path(SeeThruFeed.Base_Dir).joinpath("config.toml")) as config:
            # Creates a new script
            config.add_script(name)


    def add_script(self, name):
        with ConfigParser.ConfigParser.toml(Path(SeeThruFeed.Base_Dir).joinpath("config.toml")) as config:
            config.add_script(name)


    def add_scriptstate(self, script, name, status, message):
        # Loads the config file
        with ConfigParser.ConfigParser.toml(Path(SeeThruFeed.Base_Dir).joinpath("config.toml")) as config:
            if script not in config.Scripts:
                # TODO: Show error message
                return
            config.Scripts[script].add_state(name, status, message)

    def run_feedscheme(self):
        """
        Runs the feed scheme
        """
        # Opens the config file and parses it
        config = ConfigParser.ConfigParser.toml(Path(SeeThruFeed.Base_Dir).joinpath("config.toml")).load()

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
                value = get_config_attribute(fillable)  # TODO: Perform conversion on different value types

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
                        print(
                            "Please provide a valid status of either 'red', 'amber' or 'green'. This state will not be used")

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
            feed = Feed.Feed()
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
        with ConfigParser.ConfigParser.toml(Path(SeeThruFeed.Base_Dir).joinpath("config.toml")) as config:
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
        with ConfigParser.ConfigParser.toml(Path(SeeThruFeed.Base_Dir).joinpath("config.toml")) as config:
            # Adds the reference to the env file in the config
            config.add_api_key(
                reference,
                f"$({reference.upper()}_ACCESS_TOKEN)",
                f"$({reference.upper()}_SECRET)"
            )

        # Adds the access token and secret to the env file
        if no_env is None:
            envFile = open(os.path.join(SeeThruFeed.Base_Dir, ".env"), "a")
            envFile.write(f"{reference.upper()}_ACCESS_TOKEN={access_token}\n")
            envFile.write(f"{reference.upper()}_SECRET={secret}\n")



def exec():
    """
    Provides an entry point for the command line utility
    """
    SeeThruFeed(sys.argv)
