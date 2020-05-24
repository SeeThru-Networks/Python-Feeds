#!/usr/bin/env python
import sys, os, toml, importlib
from datetime import datetime

class SeeThru_Feed():
    Base_Dir = os.getcwd()

    def __init__(self, argv):
        """
        Provides the core functionaility

        Arguments:
            args {[string]} -- The cli args
        """
        if len(argv) == 1: return
        if argv[1] == "createfeedscheme":
            if len(argv) < 3: return
            schemeName = argv[2]
            self.CreateFeedScheme(schemeName)
        elif argv[1] == "createscript":
            if len(argv) < 3: return
            self.CreateScript(argv[2])
        elif argv[1] == "runfeedscheme":
            self.RunFeedScheme()

    def CreateFeedScheme(self, schemeName):
        """
        Creates a new feed scheme of the given name in the
        current working directory

        Arguments:
            schemeName {String} -- The name of the feed scheme
        """
        # Creates the directory structure
        self.CreateDir(schemeName)
        self.TouchFile(os.path.join(schemeName, '__init__.py'))
        self.CreateDir(os.path.join(schemeName, 'Scripts'))
        self.TouchFile(os.path.join(os.path.join(schemeName, 'Scripts'), '__init__.py'))
        self.CreateDir(os.path.join(schemeName, 'Scripts/Vendor'))
        self.TouchFile(os.path.join(os.path.join(schemeName, 'Scripts/Vendor'), '__init__.py'))
        self.CreateDir(os.path.join(schemeName, 'Components'))
        self.TouchFile(os.path.join(os.path.join(schemeName, 'Components'), '__init__.py'))
        self.CreateDir(os.path.join(schemeName, 'Components/Vendor'))
        self.TouchFile(os.path.join(os.path.join(schemeName, 'Components/Vendor'), '__init__.py'))
        self.CreateDir(os.path.join(schemeName, 'Outputs'))

        # Creates the new script
        scriptFile = open(os.path.join(os.path.dirname(__file__), 'templates/Manage_Template.py'), 'r')
        scriptTemplate = scriptFile.read()
        # Opens the new script file
        newScript = open(os.path.join(schemeName, 'manage.py'), "w")
        newScript.write(scriptTemplate)
        # Closes the files
        newScript.close()
        scriptFile.close()

        # Creates a template config file
        # Opens the template file
        templateConfig = open(os.path.join(os.path.dirname(__file__), 'templates/configHeader_Template.toml'), 'r')
        configHeader = templateConfig.read()
        # Sets the default information
        configHeader = configHeader.replace(r"{{ Scheme_Name }}", schemeName)
        configHeader = configHeader.replace(r"{{ Scheme_Description }}", "Enter a description for your feed scheme")
        configHeader = configHeader.replace(r"{{ Scheme_Author }}", "Enter the author of your feed scheme")
        configHeader = configHeader.replace(r"{{ Scheme_Owner }}", "Enter the owner for your feed scheme")
        configHeader = configHeader.replace(r"{{ Creation_Date }}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Opens a new config file for the feed scheme
        schemeConfig = open(os.path.join(schemeName, 'config.toml'), 'w')
        # Writes the config header
        schemeConfig.write(configHeader)
        # Closes the files
        templateConfig.close()
        schemeConfig.close()

    def CreateScript(self, scriptName):
        """
        Creates a new script and adds the script to the config file

        Arguments:
            schemeName {String} -- The name of the feed scheme
            scriptName {[type]} -- [description]
        """
        # Creates the new script
        scriptFile = open(os.path.join(os.path.dirname(__file__), 'templates/Script_Template.py'), 'r')
        scriptTemplate = scriptFile.read()
        # Sets the default information
        scriptTemplate = scriptTemplate.replace(r"{{ Script_Name }}", scriptName)
        # Opens the new script file
        newScript = open(os.path.join(SeeThru_Feed.Base_Dir, "Scripts/{}.py".format(scriptName)), "w")
        newScript.write(scriptTemplate)
        # Closes the files
        newScript.close()
        scriptFile.close()


        scriptConfigTemplate = open(os.path.join(os.path.dirname(__file__), 'templates/configScript_Template.toml'), 'r')
        configScript = scriptConfigTemplate.read()
        # Sets the default information
        configScript = configScript.replace(r"{{ Script_Name }}", scriptName)
        configScript = configScript.replace(r"{{ Script_Object_Path }}", "Scripts.{}".format(scriptName))
        configScript = configScript.replace(r"{{ Script_Output_Path }}", scriptName)

        # Opens the config file for the feed scheme
        schemeConfig = open(os.path.join(SeeThru_Feed.Base_Dir, 'config.toml'), 'a')
        schemeConfig.write(configScript)
        # Closes the files
        scriptConfigTemplate.close()
        schemeConfig.close()
    
    def RunFeedScheme(self):
        """
        Runs the feed scheme
        """
        # Opens the config file and parses it
        schemeConfig = open(os.path.join(SeeThru_Feed.Base_Dir, 'config.toml'), 'r')
        scheme = toml.loads(schemeConfig.read())
        schemeConfig.close()

        for script in scheme['Scripts']:
            Script_Name = list(script)[0]
            # Imports the script
            module = importlib.import_module(script[Script_Name]['Script_Object_Path'])
            class_ = getattr(module, Script_Name)
            # Instantiates the script
            scriptInstance = class_()
            # Sets any fillables defined
            for fillable in script[Script_Name]["Fillables"]:
                scriptInstance.SetProperty(fillable, script[Script_Name]["Fillables"][fillable])
            # Runs the script
            scriptInstance.RunScript()\
                .SetOutputPath(script[Script_Name]['Script_Output_Path'])\
                .EvaluateScript()\
                .LogOutput()

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
    print(sys.argv)
    SeeThru_Feed(sys.argv)