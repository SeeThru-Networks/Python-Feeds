from SeeThru_Feeds.Model.Attribution import Attribution
from SeeThru_Feeds.Model.Scripts.ScriptResult import ScriptResult
from SeeThru_Feeds.Model.Properties.PropertyManager import PropertyManager
from SeeThru_Feeds.Model.Feeds.Feed import Feed
from pathlib import Path

import SeeThru_Feeds.Model.Scripts.ScriptState as ScriptState


class ScriptBase(PropertyManager, Attribution):
    def __init__(self, *args, **kwargs):
        """
        Initialises the script
        ! If you must use __init__ in the subclass, you must call super().__init__() from that initializer
        ! otherwise override prepare and that'll be called after the super class is initialised
        """
        super().__init__()
        self._script_alias = None
        self._script_result = None
        self._script_output_path = None
        self._guid = None

        self.prepare(*args, **kwargs)

    def prepare(self, *args, **kwargs):
        """
        This can be overridden if there *needs* to be special preparation steps
        """
        pass

    # region Run

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
        try:
            # All fillables are checked on the setter, this performs one final check
            self.check_fillables()
            self.script_run()
        except ScriptState.StateAssertException as _:
            pass
        return self

    # endregion

    # region Evaluation

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
        self._script_result = ScriptResult()
        self._script_result.set_status("green")
        self._script_result.set_message("")

        # If the state engine is being used
        if issubclass(self.__class__, ScriptState.StateEngine):
            try:
                # The script evaluate only load sets the state with the state engine
                self.script_evaluate(self._script_result)
            except NotImplementedError as _:
                pass
            finally:
                self: ScriptState.StateEngine
                state = self.get_state()
                self._script_result.set_status(state.status)
                self._script_result.set_message(state.message)
        else:
            self.script_evaluate(self._script_result)
        # Fills the Timestamp of the script result
        self._script_result.generate_timestamp()
        return self

    # endregion

    # region Output

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
        self._script_output_path = path
        return self

    def export_to_output(self):
        """
        Exports the result of the script to a file path defined with set_output_path

        Raises:
            Exception: There is no output path specified

        Returns:
            ScriptBase: The script
        """
        if self._script_output_path is None:
            raise Exception("There is no output path specified")

        if self._script_result is None:
            self.evaluate_script()

        filePath = Path(self._script_output_path)
        filePath.parent.mkdir(parents=True, exist_ok=True)
        with open(filePath, "w") as file:
            file.write(self._script_result.generate_json())
        return self

    # endregion

    # region Result

    def log_output(self):
        """
        Logs the result of the script

        Returns:
            ScriptBase: The script
        """
        if self.get_internal_alias() is not None:
            print(f"--{self.get_internal_alias()}")
        print(f"Status: {self._script_result.Status}")
        print(f"Message: {self._script_result.Message}")
        return self

    def get_result(self):
        """
        Returns the ScriptResult of the script, it will evaluate the script if the script result doesn't exist

        Returns:
            ScriptResult: The script result of the script
        """
        if self._script_result is None:
            self.evaluate_script()
        return self._script_result

    # endregion

    # region Feeds

    def set_feed_guid(self, guid):
        """
        Sets the feed guid for the script

        Args:
            guid (str): The feed guid

        Returns:
            ScriptBase: The script
        """
        self._guid = guid

        return self

    def push_as_feed(self, access_token, secret):
        """
        Uses the script result as a feed and pushes the result

        Args:
            access_token (str): The access token of the api key
            secret (str): The secret of the api key
        """
        if self._guid is None:
            raise ValueError("No guid has been provided")

        feed = Feed()
        feed.set_script_result(self.get_result())
        feed.set_guid(self._guid)
        feed.set_api_key(access_token, secret)
        return feed.push()

    # endregion

    def get_internal_alias(self):
        """
        Returns an internal alias, if it is set, it can be used internally

        Returns:
            str: The internal alias
        """
        return self._script_alias

    def set_internal_alias(self, alias):
        """
        Sets a new internal alias

        Arguments:
            alias (str): The new internal alias

        Returns:
            ScriptBase: The class
        """
        self._script_alias = alias

        return self
