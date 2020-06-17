from datetime import datetime

class ScriptResult:
    def __init__(self, status=None, message=None):
        self.status = status
        self.message = message
        self.timestamp = None
    
    def SetStatus(self, status):
        """
        Sets the status of the result to a specific value

        Arguments:
            status {String} -- The status of the result

        Raises:
            TypeError: Invalid type of 'status', it must be str
            ValueError: Invalid value for 'status'
        """
        if type(status) != str: raise TypeError("Invalid type of 'status', it must be str")
        if status.lower() not in ["red", "amber", "green"]: raise ValueError("Invalid value for 'status'")
        self.status = status.lower()

    def SetMessage(self, message):
        """
        Sets the message of the result to a speific value

        Arguments:
            message {string} -- The message of the result

        Raises:
            TypeError: Invalid type of 'message', it must be str
            ValueError: Message is too long, it must be below 256 characters
        """
        if type(message) != str: raise TypeError("Invalid type of 'message', it must be str")
        if len(message) >= 256: raise ValueError("Message is too long, it must be below 256 characters")
        self.message = message

    def GenerateTimestamp(self):
        """
        Generates a timestamp for the result
        """
        self.timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    
    def GenerateJson(self):
        if self.status == None or self.message == None or self.timestamp == None: raise Exception("Not all values are provided for the result")
        return "{\"color\":\"%s\", \"message\":\"%s\", \"time\":\"%s\"}" % (self.status, self.message, self.timestamp)

    def GetStatus(self):
        """
        Returns the status of the result

        Returns:
            string: The status
        """
        return self.status
    def GetMessage(self):
        """
        Returns the message of the result

        Returns:
            string: The message
        """
        return self.message