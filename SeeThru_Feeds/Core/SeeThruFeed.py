#!/usr/bin/env python3
from SeeThru_Feeds.Model.Feeds import Feed
from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptBase
from SeeThru_Feeds.Model.Scripts.ScriptResult import ScriptResult

import argparse
import importlib
import os
import sys
import re
from datetime import datetime

import toml
from dotenv import load_dotenv


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
                    ProgramArgument("--no-config", action="store_const", const=True, required=False,
                                    help="Create a scheme without a config file")
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
            program = SeeThruFeed.Programs[argv[1]]
            argv = argv[2:]

            if "alias" in program:
                program = SeeThruFeed.Programs[program["alias"]]
                programName = program["alias"]

            # Creates the argparse program
            parser = argparse.ArgumentParser(prog=programName)
            # For every argument defined in the program
            for argument in program["arguments"]:
                parser.add_argument(*argument.args, **argument.extra)
            # Parses the arguments
            args = parser.parse_args(argv)

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

    def create_feedscheme(self, name, no_config=False):
        """
        Creates a new feed scheme of the given name in the
        current working directory

        Arguments:
            name (str): The name of the feed scheme
            no_config (bool): Whether a config file should be generated for the feedscheme
        """
        # Creates the directory structure
        create_dir(name)
        touch_file(os.path.join(name, '__init__.py'))
        create_dir(os.path.join(name, 'Scripts'))
        touch_file(os.path.join(os.path.join(name, 'Scripts'), '__init__.py'))
        create_dir(os.path.join(name, 'Scripts/Vendor'))
        touch_file(os.path.join(os.path.join(name, 'Scripts/Vendor'), '__init__.py'))
        create_dir(os.path.join(name, 'Components'))
        touch_file(os.path.join(os.path.join(name, 'Components'), '__init__.py'))
        create_dir(os.path.join(name, 'Components/Vendor'))
        touch_file(os.path.join(os.path.join(name, 'Components/Vendor'), '__init__.py'))
        create_dir(os.path.join(name, 'Outputs'))

        # Creates the new script
        scriptFile = open(os.path.join(os.path.dirname(__file__), 'templates/Manage_Template.template'), 'r')
        scriptTemplate = scriptFile.read()
        # Opens the new script file
        newScript = open(os.path.join(name, 'manage.py'), "w")
        newScript.write(scriptTemplate)
        # Closes the files
        newScript.close()
        scriptFile.close()

        if no_config:
            return

        # Creates a config
        config = {
            "Header": {
                "Scheme_Name": name,
                "Scheme_Description": "Enter a description for your feed scheme",
                "Scheme_Author": "Enter the author of your feed scheme",
                "Scheme_Owner": "Enter the owner for your feed scheme",
                "Creation_Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "Scripts": {}
        }
        # Opens a new config file for the feed scheme
        schemeConfig = open(os.path.join(name, 'config.toml'), 'w')
        # Writes the config
        schemeConfig.write(toml.dumps(config))
        # Closes the config file
        schemeConfig.close()

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
        configFilePath = os.path.join(SeeThruFeed.Base_Dir, 'config.toml')
        if not os.path.exists(configFilePath):
            return
        schemeConfig = open(configFilePath, 'r+')
        scheme = toml.loads(schemeConfig.read())

        if "Scripts" not in scheme:
            scheme["Scripts"] = {}

        scheme["Scripts"][name] = {
            "Meta": {
                "Script_Name": f"{name}",
                "Script_Output_Path": f"Outputs/{name}",
                "Script_Object_Path": f"Scripts.{name}@{name}"
            },
        }

        schemeConfig.seek(0)
        schemeConfig.write(toml.dumps(scheme))
        schemeConfig.truncate()
        # Closes the config file
        schemeConfig.close()

    def add_script(self, name):
        # Loads the config file
        configFilePath = os.path.join(SeeThruFeed.Base_Dir, 'config.toml')
        if not os.path.exists(configFilePath):
            return
        schemeConfig = open(configFilePath, 'r+')
        scheme = toml.loads(schemeConfig.read())

        if "Scripts" not in scheme:
            scheme["Scripts"] = {}

        scheme["Scripts"][name] = {
            "Meta": {
                "Script_Name": f"{name}",
                "Script_Output_Path": f"Outputs/{name}",
                "Script_Object_Path": f"Scripts.{name}@{name}"
            },
        }

        schemeConfig.seek(0)
        schemeConfig.write(toml.dumps(scheme))
        schemeConfig.truncate()
        # Closes the config file
        schemeConfig.close()

    def run_feedscheme(self):
        """
        Runs the feed scheme
        """
        # Opens the config file and parses it
        configFilePath = os.path.join(SeeThruFeed.Base_Dir, 'config.toml')
        if not os.path.exists(configFilePath):
            return
        schemeConfig = open(configFilePath, 'r')
        scheme = toml.loads(schemeConfig.read())
        schemeConfig.close()

        if type(scheme["Scripts"]) != dict:
            return

        scriptResults = {}

        for scriptId in scheme['Scripts'].keys():
            script = scheme["Scripts"][scriptId]

            # Gets the meta
            if "Meta" not in script:
                return
            meta = script["Meta"]

            scriptName = get_config_attribute(meta["Script_Name"]) if "Script_Name" in meta else scriptId

            if "Script_Output_Path" not in meta:
                return
            outputPath = get_config_attribute(meta["Script_Output_Path"])

            # Splits the object's module and the object's name from the Script_Object_Path
            if "Script_Object_Path" not in meta:
                return
            objectComponents = get_config_attribute(meta['Script_Object_Path']).split('@')
            if len(objectComponents) != 2:
                return
            objectModule, objectName = tuple(objectComponents)

            # Dynamically imports the script
            scriptModule = importlib.import_module(objectModule)
            if objectName not in dir(scriptModule):
                return
            scriptClass = getattr(scriptModule, objectName)
            # Instantiates the script
            scriptInstance: ScriptBase = scriptClass()

            # Sets any fillables defined
            if "Fillables" in script:
                fillables = script["Fillables"]
                for fillable in fillables.keys():
                    # Gets the value assigned to the fillable
                    value = fillables[fillable]

                    # Gets all defined environment variables
                    value = get_config_attribute(value)

                    # Assigns the fillable to the script
                    scriptInstance.set_property(fillable, value)

            scriptInstance.set_internal_alias(scriptName)
            # Runs the script
            scriptInstance.set_output_path(outputPath)
            scriptInstance.run_script()
            scriptInstance.evaluate_script()
            scriptInstance.log_output()
            scriptInstance.export_to_output()

            scriptResults[scriptName] = scriptInstance.get_result()

        # Goes through every feed
        if "Feeds" not in scheme:
            return
        if "Api_Keys" not in scheme:
            return
        for feed in scheme["Feeds"].keys():
            scriptName = get_config_attribute(scheme["Feeds"][feed]["Script"])
            api_key = get_config_attribute(scheme["Feeds"][feed]["Api_Key"])
            guid = get_config_attribute(scheme["Feeds"][feed]["Guid"])
            if scriptName not in scriptResults:
                continue
            # Gets the api key
            if api_key not in scheme["Api_Keys"]:
                continue
            accessToken = get_config_attribute(scheme["Api_Keys"][api_key]["Access_Token"])
            secret = get_config_attribute(scheme["Api_Keys"][api_key]["Secret"])

            result = scriptResults[scriptName]

            # Pushes the script result
            feed = Feed.Feed()
            feed.set_guid(guid)
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
        configFilePath = os.path.join(SeeThruFeed.Base_Dir, 'config.toml')
        if not os.path.exists(configFilePath):
            return
        schemeConfig = open(configFilePath, 'r+')
        scheme = toml.loads(schemeConfig.read())

        if "Feeds" not in scheme:
            scheme["Feeds"] = {}

        # Adds the feed to the config
        scheme["Feeds"][name] = {
            "Script": script,
            "Api_Key": api_key,
            "Guid": guid
        }

        schemeConfig.seek(0)
        schemeConfig.write(toml.dumps(scheme))
        schemeConfig.truncate()
        schemeConfig.close()

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
        configFilePath = os.path.join(SeeThruFeed.Base_Dir, 'config.toml')
        if not os.path.exists(configFilePath):
            return
        schemeConfig = open(configFilePath, 'r+')
        scheme = toml.loads(schemeConfig.read())

        # Adds an api key
        if "Api_Keys" not in scheme:
            scheme["Api_Keys"] = {}

        # Adds the reference to the env file in the config
        scheme["Api_Keys"][reference] = {
            "Access_Token": f"$({reference.upper()}_ACCESS_TOKEN)",
            "Secret": f"$({reference.upper()}_SECRET)"
        }

        # Adds the access token and secret to the env file
        if no_env is None:
            envFile = open(os.path.join(SeeThruFeed.Base_Dir, ".env"), "a")
            envFile.write(f"{reference.upper()}_ACCESS_TOKEN={access_token}\n")
            envFile.write(f"{reference.upper()}_SECRET={secret}\n")

        schemeConfig.seek(0)
        schemeConfig.write(toml.dumps(scheme))
        schemeConfig.truncate()
        schemeConfig.close()


def exec():
    """
    Provides an entry point for the command line utility
    """
    SeeThruFeed(sys.argv)
