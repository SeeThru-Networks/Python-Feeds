"""
Stores script state
A script can choose to use states rather than an evaluation method,
the script state gets set during the script runtime
Each state has a default status and message, these can be overwritten elsewhere if a custom status or message is needed
"""


class StateAssertException(Exception):
    pass


class State:
    """
    Defines a possible state, with a status and message pair
    """
    green = "green"
    ok = green
    amber = "amber"
    warning = amber
    red = "red"
    error = red

    def __init__(self, name, status, message):
        self._name = name
        self._status = status
        self._message = message

    @property
    def name(self):
        return self._name

    @property
    def status(self):
        return self._status

    @property
    def message(self):
        return self._message


class DefaultStates:
    """
    Defines the possible states that a script can have
    """
    OK = State("ok", State.ok, "")
    WARNING = State("warning", State.warning, "There is a warning")
    ERROR = State("error", State.error, "There is an error")


class StateEngine:
    """
    Stores evaluation states, this can be used as an alternative to script_evaluate,
    where the state is set as the script runs
    """
    class MessageStates(DefaultStates):
        """
        Creates the default state options, this can be overwritten if custom states are required
        """
        pass

    _state = DefaultStates.OK
    _configurations = {}

    def configure_state(self, state, status, message):
        """
        Configures a custom state for the script

        Args:
            state (str): The name of the state to configure
            status (str): The status of the state
            message (str): The message of the state

        Returns:
            bool: Whether the operation was succesfull
        """
        status = status.lower()
        if status not in ["green", "amber", "red"]:
            raise ValueError("Please provide a valid status")
        # Matches the state with an existing state
        for variable in dir(self.MessageStates):
            var = getattr(self.MessageStates, variable)
            if isinstance(var, State):
                if var.name == state:
                    # Stores the state in the configuration, not overriding the MessageStates
                    self._configurations[state] = State(state, status, message)
                    # Checks if the currently set state should be reset
                    if self._state.name == state:
                        self._state = self._configurations[state]
                    return True
        return False

    def set_state(self, state):
        """
        Sets the state of the script
        This can be used as an alternative to evaluation

        Args:
            state (State): The state

        Returns:
            ScriptBase: The script
        """
        if type(state) != State:
            raise TypeError("Please provide a valid state")
        # Uses the state in the configurations if one exists for the state name
        if state.name in self._configurations:
            self._state = self._configurations[state.name]
        else:
            self._state = state

        return self

    def get_state(self):
        """
        Returns the state of the script

        Returns:
           State: The state of the script
        """
        return self._state

    def assert_true(self, condition, state):
        """
        Asserts that the condition is true,
        If not, the state is set and the script is ended

        Args:
            condition (bool): The condition
            state (State): The state to set to
        """
        if not condition:
            self._state = state
            # Raises an exception to escape the run method
            raise StateAssertException()
