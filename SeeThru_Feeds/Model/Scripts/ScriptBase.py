from SeeThru_Feeds.Model.Scripts.ScriptResult import ScriptResult
from SeeThru_Feeds.Model.Properties.PropertyManager import PropertyManager
from pathlib import Path


class ScriptBase(PropertyManager):

    def __init__(self, *args, **kwargs):
        """
        Initialises the script
        ! If you must use __init__ in the subclass, you must call super().__init__() from that initializer
        ! otherwise override prepare and that'll be called after the super class is initialised
        """
        super().__init__()
        self.Script_Alias = None
        self.ScriptResult = None
        self.ScriptOutputPath = None

        self.prepare(*args, **kwargs)

    def prepare(self, *args, **kwargs):
        """
        This can be overridden if there *needs* to be special preparation steps
        """
        pass

    def script_run(self):
        """
        This function should be overridden by a subclass
        This is where your script should start running

        Raises:
            NotImplementedError: There is no execution method defined, please define it with 'script_run'
        """
        raise NotImplementedError("There is no execution method defined, please define it with 'script_run'")

    def run_script(self):
        """
        Runs the script

        Returns:
            ScriptBase: The script
        """
        # All fillables are checked on the setter, this performs one final check
        self.check_fillables()
        self.script_run()
        return self

    def script_evaluate(self, result):
        """
        This function should fill the Status and Message attributes of the result attribute
        based upon the results of the script using set_status and set_message

        Arguments:
            result (ScriptResult): The result

        Raises:
            NotImplementedError: There is not evaluation method defined, please define it with 'script_evaluate'
        """
        raise NotImplementedError("There is no evaluation method defined, please define it with 'script_evaluate'")

    def evaluate_script(self):
        """
        Evaluates the script result

        Returns:
            ScriptBase: The script
        """
        # Creates a new script result
        self.ScriptResult = ScriptResult()
        self.ScriptResult.set_status("green")
        self.ScriptResult.set_message("")
        self.script_evaluate(self.ScriptResult)
        # Fills the Timestamp of the script result
        self.ScriptResult.generate_timestamp()
        return self

    def set_output_path(self, path):
        """
        Sets the output path for the result of the script

        Arguments:
            path (str): The output path

        Raises:
            TypeError: The 'path' argument must be a str

        Returns:
            ScriptBase: The script
        """
        if type(path) != str:
            raise TypeError("The 'path' argument must be a str")
        self.ScriptOutputPath = path
        return self

    def export_to_output(self):
        """
        Exports the result of the script to a file path defined with set_output_path

        Raises:
            Exception: There is no output path specified

        Returns:
            ScriptBase: The script
        """
        if self.ScriptOutputPath is None:
            raise Exception("There is no output path specified")

        if self.ScriptResult is None:
            self.evaluate_script()

        filePath = Path(self.ScriptOutputPath)
        if filePath.parent.exists():
            file = open(self.ScriptOutputPath, "w")
            file.write(self.ScriptResult.generate_json())
            file.close()
        else:
            raise Exception("Directory for output file '{}' does not exist".format(self.ScriptOutputPath))
        return self

    def log_output(self):
        """
        Logs the result of the script

        Returns:
            ScriptBase: The script
        """
        if self.get_internal_alias() is not None:
            print("--{}".format(self.get_internal_alias()))
        print(f"Status: {self.ScriptResult.Status}")
        print(f"Message: {self.ScriptResult.Message}")
        return self

    def get_result(self):
        """
        Returns the ScriptResult of the script, it will evaluate the script if the script result doesn't exist

        Returns:
            ScriptResult: The script result of the script
        """
        if self.ScriptResult is None:
            self.evaluate_script()
        return self.ScriptResult

    # The Script_Title attribute should be set in your script
    Script_Title = None

    @classmethod
    def get_title(cls):
        """
        Returns a title of the script

        Raises:
            NotImplementedError: There is no title defined, please define it as 'Script_Title='

        Returns:
            str: The script's title
        """
        if cls.Script_Title is None:
            raise NotImplementedError("There is no title defined, please define it as 'Script_Title='")
        return cls.Script_Title
    # The Script_Description attribute should be set in your script
    Script_Description = None

    @classmethod
    def get_description(cls):
        """
        Returns a description of the script

        Raises:
            NotImplementedError: There is no description defined, please define it as 'Script_Description='

        Returns:
            str: The script's description
        """
        if cls.Script_Description is None:
            raise NotImplementedError("There is no description defined, please define it as 'Script_Description='")
        return cls.Script_Description
    # The Script_Author attribute should be set in your script
    Script_Author = None

    @classmethod
    def get_author(cls):
        """
        Returns the author of the script

        Raises:
            NotImplementedError: There is no author defined, please define it as 'Script_Author='

        Returns:
            str: The script's author
        """
        if cls.Script_Author is None:
            raise NotImplementedError("There is no author defined, please define it as 'Script_Author='")
        return cls.Script_Author
    # The Script_Owner attribute should be set in your script
    Script_Owner = None

    @classmethod
    def get_owner(cls):
        """
        Returns a owner of the script

        Raises:
            NotImplementedError: There is no owner defined, please define it as 'Script_Owner='

        Returns:
            str: The script's owner
        """
        if cls.Script_Owner is None:
            raise NotImplementedError("There is no owner defined, please define it as 'Script_Owner='")
        return cls.Script_Owner
    # The Script_SupportLink attribute should be set in your script
    Script_SupportLink = None

    @classmethod
    def get_support_link(cls):
        """
        Returns a support link of the script

        Raises:
            NotImplementedError: There is no supportLink defined, please define it as 'Script_SupportLink='

        Returns:
            str: The script's support link
        """
        if cls.Script_SupportLink is None:
            raise NotImplementedError("There is no supportLink defined, please define it as 'Script_SupportLink='")
        return cls.Script_SupportLink
    # The Script_DocLink attribute should be set in your script
    Script_DocLink = None

    @classmethod
    def get_docs_link(cls):
        """
        Returns a doc link of the script

        Raises:
            NotImplementedError: There is no DocLink defined, please define it as 'Script_DocLink='

        Returns:
            str: The script's doc link
        """
        if cls.Script_DocLink is None:
            raise NotImplementedError("There is no DocLink defined, please define it as 'Script_DocLink='")
        return cls.Script_DocLink
    # The Script_LicenseLink attribute should be set in your script
    Script_LicenseLink = None

    @classmethod
    def get_license_link(cls):
        """
        Returns a license link of the script

        Raises:
            NotImplementedError: There is no LicenseLink defined, please define it as 'Script_LicenseLink='

        Returns:
            str: The script's license link
        """
        if cls.Script_LicenseLink is None:
            raise NotImplementedError("There is no LicenseLink defined, please define it as 'Script_LicenseLink='")
        return cls.Script_LicenseLink

    def get_internal_alias(self):
        """
        Returns an internal alias of the script, if it is set, it will can be used internally

        Returns:
            str: The script's internal alias
        """
        return self.Script_Alias

    def set_internal_alias(self, alias):
        """
        Sets a new internal alias for the script

        Arguments:
            alias (str): The new internal alias

        Returns:
            ScriptBase: The script
        """
        self.Script_Alias = alias

        return self
