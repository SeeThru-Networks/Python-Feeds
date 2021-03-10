from datetime import datetime


class ScriptResult:
    def __init__(self, status=None, message=None):
        """
        Creates a new script result

        Args:
            status: The status of the result
            message: The message of the result
        """
        self.Status = status
        self.Message = message
        self.Timestamp = None

    def set_status(self, status):
        """
        Sets the Status of the result to a specific value

        Arguments:
            status (str): The status of the result

        Returns:
            ScriptResult: The script result

        Raises:
            TypeError: Invalid type of 'Status', it must be str
            ValueError: Invalid value for 'Status'
        """
        if type(status) != str:
            raise TypeError("Invalid type of 'Status', it must be str")
        if status.lower() not in ["red", "amber", "green"]:
            raise ValueError("Invalid value for 'Status'")
        self.Status = status.lower()

        return self

    def set_message(self, message):
        """
        Sets the Message of the result to a specific value

        Arguments:
            message (str): The message of the result

        Returns:
            ScriptResult: The script result

        Raises:
            TypeError: Invalid type of 'Message', it must be str
            ValueError: Message is too long, it must be below 256 characters
        """
        if type(message) != str:
            raise TypeError("Invalid type of 'Message', it must be str")
        self.Message = message

        return self

    def generate_timestamp(self):
        """
        Generates a Timestamp for the result

        Returns:
            ScriptResult: The script result
        """
        self.Timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        return self

    def generate_json(self):
        """
        Generates the json result result

        Returns:
            str: The json string
        """
        if self.Status is None or self.Message is None or self.Timestamp is None:
            raise Exception("Not all values are provided for the result")
        return "{\"color\":\"%s\", \"Message\":\"%s\", \"time\":\"%s\"}" % (self.Status, self.Message, self.Timestamp)

    def get_status(self):
        """
        Returns the Status of the result

        Returns:
            str: The Status
        """
        return self.Status

    def get_message(self):
        """
        Returns the Message of the result

        Returns:
            str: The Message
        """
        return self.Message

    def get_timestamp(self):
        """
        Returns the status of the script result

        Returns:
            str: The timestamp
        """
        return self.Timestamp
