import seethrufeeds.core.exceptions.config as ConfigExceptions

class State:
    Name: str
    Status: str
    Message: str

    def __init__(self, name: str, status: str, message: str):
        self.Name = name
        self.Status = status
        self.Message = message

    @staticmethod
    def new(name: str, status: str, message: str) -> "State":
        """
                Creates a new script state, with given attributes

                Args:
                    name (str): The name of the state
                    status (str): The status to give the script state
                    message (str): The message to give the script state

                Returns:
                    State: The new script state

                """
        return State(name, status, message)

    @staticmethod
    def load(data: dict, script_name: str) -> "State":
        """
        Parses the given data into a script state
        Args:
            data: The data to parse
            script_name: The name of the script

        Returns:
            State: The state
        """
        if "Name" not in data:
            raise ConfigExceptions.ScriptStateException("A script state has no name", script_name)
        if "Status" not in data:
            raise ConfigExceptions.ScriptStateException(f"The script state {data['Name']} has no status", script_name)
        if "Message" not in data:
            raise ConfigExceptions.ScriptStateException(f"The script state {data['Name']} has no message", script_name)
        return State(
            data["Name"],
            data["Status"],
            data["Message"]
        )

    def dump(self) -> dict:
        """
        Dumps the state into a dictionary

        Returns:
            dict: The dumped data
        """
        return {
            "Name": self.Name,
            "Status": self.Status,
            "Message": self.Message
        }
