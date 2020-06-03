from SeeThru_Feeds.Model.Scripts.ScriptResult import ScriptResult
from SeeThru_Feeds.Model.Properties.PropertyManager import PropertyManager
from pathlib import Path

class ScriptBase(PropertyManager):

    def __init__(self, *args, **kwargs):
        """
        Initialises the script
        ! If you must use __init__ in the subclass, you must call super().__init__() from that initialiser
        ! otherwise override Prepare and that'll be called after the super class is initialised
        """
        self.OutputPath = None

        self.Prepare(*args, **kwargs)
    
    def Prepare(self, *args, **kwargs):
        """
        This can be overriden if there *needs* to be special preparation steps
        """
        pass

    def Script_Run(self): 
        """
        This function should be overridden by a subclass
        This is where your script should start running

        Raises:
            NotImplementedError: There is no execution method defined, please define it with 'Script_Run'
        """
        raise NotImplementedError("There is no execution method defined, please define it with 'Script_Run'")
    def RunScript(self):
        """
        Runs the script

        Returns:
            ScriptBase -- The script
        """
        # Ensures that all of the fillables are met before the script is ran
        self.CheckFillables()
        self.Script_Run()
        return self

    def Script_Evaluate(self, result):
        """
        This function should fill the status and message attributes of the result attribute
        based upon the results of the script using SetStatus and SetMessage

        Arguments:
            result {ScriptResult} -- The result

        Raises:
            NotImplementedError: There is not evaluation method defined, please define it with 'Script_Evaluate'
        """
        raise NotImplementedError("There is not evaluation method defined, please define it with 'Script_Evaluate'")
    def EvaluateScript(self):
        """
        Evaluates the script result

        Returns:
            ScriptBase -- The script
        """
        # Creates a new script result
        self.ScriptResult = ScriptResult()
        self.ScriptResult.SetStatus("green")
        self.ScriptResult.SetMessage("")
        self.Script_Evaluate(self.ScriptResult)
        # Fills the timestamp of the script result
        self.ScriptResult.GenerateTimestamp()
        return self

    def SetOutputPath(self, path):
        """
        Sets the output path for the result of the script

        Arguments:
            path {str} -- The path

        Raises:
            TypeError: The 'path' argument must be a str

        Returns:
            ScriptBase -- The script
        """
        if type(path) != str: raise TypeError("The 'path' argument must be a str")
        self.ScriptOutputPath = path
        return self

    def ExportToOutput(self):
        """
        Exports the result of the script to a file path defined with SetOutputPath

        Raises:
            Exception: There is no output path specificed
            Any: Exceptions raised by file

        Returns:
            ScriptBase -- The script
        """
        if self.ScriptOutputPath == None: raise Exception("There is no output path specificed")
        filePath = Path(self.ScriptOutputPath)
        if filePath.parent.exists(): 
            file = open(self.ScriptOutputPath, "w")
            file.write(self.ScriptResult.GenerateJson())
            file.close()
        else: raise Exception("Directory for output file '{}' does not exist".format(self.ScriptOutputPath))
        return self
    def LogOutput(self):
        """
        Logs the result of the script

        Returns:
            ScriptBase -- The script
        """
        if (self.GetInternalAlias() != None): print("--{}".format(self.GetInternalAlias()))
        print("Status: {}\nMessage: {}".format(self.ScriptResult.status, self.ScriptResult.message))
        return self
    
    # The Script_Title attribute should be set in your script
    Script_Title = None
    @classmethod
    def GetTitle(cls):
        """
        Returns a title of the script

        Raises:
            NotImplementedError: There is no title defined, please define it as 'Script_Title='

        Returns:
            string -- The script's title
        """
        if cls.Script_Title == None: raise NotImplementedError("There is no title defined, please define it as 'Script_Title='")
        return cls.Script_Title
    # The Script_Description attribute should be set in your script
    Script_Description = None
    @classmethod
    def GetDescription(cls):
        """
        Returns a description of the script

        Raises:
            NotImplementedError: There is no description defined, please define it as 'Script_Description='

        Returns:
            string -- The script's description
        """
        if cls.Script_Description == None: raise NotImplementedError("There is no description defined, please define it as 'Script_Description='")
        return cls.Script_Description
    # The Script_Author attribute should be set in your script
    Script_Author = None
    @classmethod
    def GetAuthor(cls):
        """
        Returns the author of the script

        Raises:
            NotImplementedError: There is no author defined, please define it as 'Script_Author='

        Returns:
            string -- The script's author
        """
        if cls.Script_Author == None: raise NotImplementedError("There is no author defined, please define it as 'Script_Author='")
        return cls.Script_Author
    # The Script_Owner attribute should be set in your script
    Script_Owner = None
    @classmethod
    def GetOwner(cls):
        """
        Returns a owner of the script

        Raises:
            NotImplementedError: There is no owner defined, please define it as 'Script_Owner='

        Returns:
            string -- The script's owner
        """
        if cls.Script_Owner == None: raise NotImplementedError("There is no owner defined, please define it as 'Script_Owner='")
        return cls.Script_Owner
    # The Script_SupportLink attribute should be set in your script
    Script_SupportLink = None
    @classmethod
    def GetSupportLink(cls):
        """
        Returns a support link of the script

        Raises:
            NotImplementedError: There is no supportLink defined, please define it as 'Script_SupportLink='

        Returns:
            string -- The script's support link
        """
        if cls.Script_SupportLink == None: raise NotImplementedError("There is no supportLink defined, please define it as 'Script_SupportLink='")
        return cls.Script_SupportLink
    # The Script_DocLink attribute should be set in your script
    Script_DocLink = None
    @classmethod
    def GetDocLink(cls):
        """
        Returns a doc link of the script

        Raises:
            NotImplementedError: There is no DocLink defined, please define it as 'Script_DocLink='

        Returns:
            string -- The script's doc link
        """
        if cls.Script_DocLink == None: raise NotImplementedError("There is no DocLink defined, please define it as 'Script_DocLink='")
        return cls.Script_DocLink
    # The Script_LicenseLink attribute should be set in your script
    Script_LicenseLink = None
    @classmethod
    def GetLicenseLink(cls):
        """
        Returns a license link of the script

        Raises:
            NotImplementedError: There is no LicenseLink defined, please define it as 'Script_LicenseLink='

        Returns:
            string -- The script's license link
        """
        if cls.Script_LicenseLink == None: raise NotImplementedError("There is no LicenseLink defined, please define it as 'Script_LicenseLink='")
        return cls.Script_LicenseLink
    
    def GetInternalAlias(self):
        """
        Returns an internal alias of the script, if it is set, it will can be used internally

        Returns:
            string -- The script's internal alias
        """
        try:
            return self.Script_Alias
        except: 
            self.Script_Alias = None
            return self.Script_Alias
    def SetInternalAlias(self, alias):
        """
        Sets a new internal alias for the script

        Arguments:
            alias {String} -- The new internal alias
        """
        self.Script_Alias = alias