from typing import Any, Dict

from . import meta as ScriptMeta, state as ScriptState

from seethrufeeds.core.exceptions import config as ConfigExceptions

class Script:
    Meta: "ScriptMeta.Meta"
    Fillables: Dict[str, Any]
    States: Dict[str, "ScriptState.State"]

    def __init__(self,
                 meta: "ScriptMeta",
                 fillables: Dict[str, Any],
                 states: Dict[str, "ScriptState"]):
        self.Meta = meta
        self.Fillables = fillables
        self.States = states

    @staticmethod
    def new(name: str) -> "Script":
        """
            Creates a new script, with default attributes

            Args:
                name (str): The name of the script

            Returns:
                ConfigScript: The new script
            """
        meta = ScriptMeta.Meta.new(name)
        return Script(meta, {}, {})

    def add_fillable(self, name: str, value: Any) -> Any:
        """
            Adds a new fillable to the script

            Args:
                name (str): The name of the fillable
                value (Any): The value to give the fillable

            Returns:
                Any: The value
            """
        self.Fillables[name] = value
        return value

    def add_state(self, name: str, status: str, message: str) -> ScriptState:
        """
            Adds a new state to the script

            Args:
                name (str): The name of the state
                status (str): The status to give the script state
                message (str): The message to give the script state

            Returns:
                State: The new state
            """
        state = ScriptState.State.new(name, status, message)
        self.States[name] = state
        return state

    @staticmethod
    def load(data: dict, name: str)-> "Script":
        """
        Parses the given data into a script

        Args:
            data: The data to parse
            name: The name of the script

        Returns:
            Script: The script created
        """
        # Loads the meta
        if "Meta" in data:
            meta = ScriptMeta.Meta.load(data["Meta"], name)
        else:
            raise ConfigExceptions.ScriptMetaException("No meta given for script", name)
        # Loads the fillable properties set
        fillables = {}
        if "Fillables" in data:
            fillables = data["Fillables"]
        # Loads the script states
        states = {}
        if "States" in data:
            states = data["States"]
            if type(states) != dict:
                raise ConfigExceptions.ScriptException("Invalid state given", name)
            # Loads the state into internal object model
            states = {
                key: ScriptState.State.load(states[key], name) for key in states.keys()
            }
        return Script(
            meta,
            fillables,
            states
        )

    def dump(self) -> dict:
        """
        Dumps the config part into a dictionary
        Returns:
            dict: The data
        """
        data = {
            "Meta": self.Meta.dump()
        }
        if len(self.Fillables) != 0:
            data["Fillables"] = self.Fillables
        if len(self.States) != 0:
            # Turns internal representation of state into dictionary
            data["States"] = {
                key: self.States[key].dump() for key in self.States.keys()
            }
        return data
