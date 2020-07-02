#!/usr/bin/env python3
import sys
import os
import toml
import importlib
import argparse
from datetime import datetime


class Program_Argument:
    def __init__(self, *args, **kargs):
        self.args = args
        self.extra = kargs


class SeeThru_Feed():
    Base_Dir = os.getcwd()
    Programs = {}

    @classmethod
    def SetupPrograms(cls):
        cls.Programs = {
            "createfeedscheme": {
                "procedure": SeeThru_Feed.CreateFeedScheme,
                "arguments": [
                    Program_Argument("name", action="store", type=str)
                ]
            },
            "createscript": {
                "procedure": SeeThru_Feed.CreateScript,
                "arguments": {
                    Program_Argument("name", action="store", type=str)
                }
            },
            "runfeedscheme": {
                "procedure": SeeThru_Feed.RunFeedScheme,
                "arguments": []
            }
        }

    def __init__(self, argv, base_dir=os.getcwd()):
        """
        Provides the core functionaility

        Arguments:
            argv {[string]} -- The cli args
            base_dir {string} -- The base directory to work from
        """
        SeeThru_Feed.Base_Dir = base_dir
        SeeThru_Feed.SetupPrograms()
        self.argv = argv

        if len(argv) == 1:  # If no arguments were given, print a help message
            return

        # Runs the appropriate program
        if argv[1] in SeeThru_Feed.Programs.keys():
            # Gets the program
            try:
                programName = argv[1]
                program = SeeThru_Feed.Programs[argv[1]]
                argv = argv[2:]
            except:
                print("Please provide a valid program")
                return
            # Creates the argparse program
            parser = argparse.ArgumentParser(prog=programName)
            # For every argument defined in the program
            for argument in program["arguments"]:
                parser.add_argument(*argument.args, **argument.extra)
            # Parses the arguments
            args = parser.parse_args(argv)

            program["procedure"](self, **vars(args))
            return

    def CreateFeedScheme(self, name):
        """
        Creates a new feed scheme of the given name in the
        current working directory

        Arguments:
            name {String} -- The name of the feed scheme
        """
        # Creates the directory structure
        self.CreateDir(name)
        self.TouchFile(os.path.join(name, '__init__.py'))
        self.CreateDir(os.path.join(name, 'Scripts'))
        self.TouchFile(os.path.join(os.path.join(
            name, 'Scripts'), '__init__.py'))
        self.CreateDir(os.path.join(name, 'Scripts/Vendor'))
        self.TouchFile(os.path.join(os.path.join(
            name, 'Scripts/Vendor'), '__init__.py'))
        self.CreateDir(os.path.join(name, 'Components'))
        self.TouchFile(os.path.join(os.path.join(
            name, 'Components'), '__init__.py'))
        self.CreateDir(os.path.join(name, 'Components/Vendor'))
        self.TouchFile(os.path.join(os.path.join(
            name, 'Components/Vendor'), '__init__.py'))
        self.CreateDir(os.path.join(name, 'Outputs'))

        # Creates the new script
        scriptFile = open(os.path.join(os.path.dirname(__file__),
                                       'templates/Manage_Template.template'), 'r')
        scriptTemplate = scriptFile.read()
        # Opens the new script file
        newScript = open(os.path.join(name, 'manage.py'), "w")
        newScript.write(scriptTemplate)
        # Closes the files
        newScript.close()
        scriptFile.close()

        if "--no-config" in self.argv:
            return

        # Creates a template config file
        # Opens the template file
        templateConfig = open(os.path.join(os.path.dirname(
            __file__), 'templates/configHeader_Template.toml'), 'r')
        configHeader = templateConfig.read()
        # Sets the default information
        configHeader = configHeader.replace(r"{{ Scheme_Name }}", name)
        configHeader = configHeader.replace(
            r"{{ Scheme_Description }}", "Enter a description for your feed scheme")
        configHeader = configHeader.replace(
            r"{{ Scheme_Author }}", "Enter the author of your feed scheme")
        configHeader = configHeader.replace(
            r"{{ Scheme_Owner }}", "Enter the owner for your feed scheme")
        configHeader = configHeader.replace(
            r"{{ Creation_Date }}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        # Opens a new config file for the feed scheme
        schemeConfig = open(os.path.join(name, 'config.toml'), 'w')
        # Writes the config header
        schemeConfig.write(configHeader)
        # Closes the files
        templateConfig.close()
        schemeConfig.close()

    def CreateScript(self, name):
        """
        Creates a new script and adds the script to the config file

        Arguments:
            name {String} -- The name of the feed scheme
            name {[type]} -- [description]
        """
        # Creates the new script
        scriptFile = open(os.path.join(os.path.dirname(
            __file__), 'templates/Script_Template.template'), 'r')
        scriptTemplate = scriptFile.read()
        # Sets the default information
        scriptTemplate = scriptTemplate.replace(
            r"{{ Script_Name }}", name)
        # Opens the new script file
        newScript = open(os.path.join(SeeThru_Feed.Base_Dir,
                                      "Scripts/{}.py".format(name)), "w")
        newScript.write(scriptTemplate)
        # Closes the files
        newScript.close()
        scriptFile.close()

        if "--no-config" in self.argv:
            return

        scriptConfigTemplate = open(os.path.join(os.path.dirname(
            __file__), 'templates/configScript_Template.toml'), 'r')
        configScript = scriptConfigTemplate.read()
        # Sets the default information
        configScript = configScript.replace(r"{{ Script_Name }}", name)
        configScript = configScript.replace(
            r"{{ Script_Object_Path }}", "Scripts.{}@{}".format(name, name))
        configScript = configScript.replace(
            r"{{ Script_Output_Path }}", "Outputs/{}.json".format(name))

        # Opens the config file for the feed scheme
        schemeConfig = open(os.path.join(
            SeeThru_Feed.Base_Dir, 'config.toml'), 'a')
        schemeConfig.write(configScript)
        # Closes the files
        scriptConfigTemplate.close()
        schemeConfig.close()

    def RunFeedScheme(self):
        """
        Runs the feed scheme
        """
        return
        # Parses a .env file if one exists
        if os.path.exists(os.path.join(SeeThru_Feed.Base_Dir, '.env')):
            # Opens the file and parses it
            envFile = open(os.path.join(SeeThru_Feed.Base_Dir, '.env'), "r")
            iter = 0
            while True:
                iter += 1
                line = envFile.readline()
                if not line:
                    break
                line = line.split("#")[0]
                # Finds key value pairs
                if "=" in line:
                    key, value = line.split("=")

                    key = key.strip("\n")
                    key = key.strip(" ")
                    if key.startswith('"'):
                        key = key.strip('"')
                    elif key.startswith("'"):
                        key = key.strip("'")

                    value = value.strip("\n")
                    value = value.strip(" ")
                    if value.startswith('"'):
                        value = value.strip('"')
                    elif value.startswith("'"):
                        value = value.strip("'")
                    os.environ[key] = value
            pass
        # Opens the config file and parses it
        if not os.path.exists(os.path.join(SeeThru_Feed.Base_Dir, 'config.toml')):
            print("[Error] There is no config file")
            return
        schemeConfig = open(os.path.join(
            SeeThru_Feed.Base_Dir, 'config.toml'), 'r')
        scheme = toml.loads(schemeConfig.read())
        schemeConfig.close()

        for script in scheme['Scripts']:
            Script_Name = list(script)[0]
            # Splits the object's module and the object's name from the Script_Object_Path
            objectModule = None
            objectName = None
            objectComponents = script[Script_Name]['Meta']['Script_Object_Path'].split(
                '@')
            objectModule = objectComponents[0]
            objectName = objectComponents[1] if len(
                objectComponents) > 1 else None

            # Imports the script
            module = importlib.import_module(objectModule)
            class_ = getattr(module, objectName)
            # Instantiates the script
            scriptInstance = class_()

            # Sets any fillables defined
            if 'Fillables' in script[Script_Name]:
                for fillable in script[Script_Name]["Fillables"]:
                    # Gets the value assigned to the fillable
                    value = script[Script_Name]["Fillables"][fillable]
                    # Checks if the value is a deferred value, i.e. the value is somewhere else
                    try:
                        value = dict(value)
                        if "type" not in value or "name" not in value:
                            print(
                                "[Error] Incorrectly configured value: {}".format(value))
                            return
                        # Checks for which type of deferred value it is
                        if value["type"] == "env":
                            # Looks for the value in the env file
                            if value["name"] not in os.environ:
                                print("[Error] Name {} not in env".format(
                                    value["name"]))
                                return
                            value = os.environ[value["name"]]
                    except:
                        pass
                    finally:
                        scriptInstance.SetProperty(fillable, value)

            scriptInstance.SetInternalAlias(Script_Name)
            # Runs the script
            scriptInstance.RunScript()\
                .SetOutputPath(script[Script_Name]['Meta']['Script_Output_Path'])\
                .EvaluateScript()\
                .LogOutput()\
                .ExportToOutput()

    # ------Utility Methods------
    def CreateDir(self, path):
        """
        Creates a given directory

        Arguments:
            path {os.path} -- The path of the new directory
        """
        path = os.path.join(SeeThru_Feed.Base_Dir, path)
        os.mkdir(path)

    def TouchFile(self, path):
        """
        Creates a new file

        Arguments:
            path {os.path} -- The path of the new file
        """
        path = os.path.join(SeeThru_Feed.Base_Dir, path)
        f = open(path, "w")
        f.close()


def exec():
    SeeThru_Feed(sys.argv)
