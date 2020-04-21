from Library.Components.Sockets.Socket import Socket
from Library.Components.HTTP.HTTPGet import HTTPGet
from Model.ServiceBase import ServiceBase
import json

class GenericTeamsService(ServiceBase):

    def __init__(self, **kwargs):
        super().__init__("GenericTeamsService", **kwargs)
        #Stores whether there is an issue with google hangouts
        self.hangouts_error = False

    def run(self):
        if not self.port_open():
            self.evaluate(None)
            return

        self.evaluate(None)

    def evaluate(self, value):
        # Takes the result to evaluate it
        self.status = "green"
        self.message = ""

        # Changes to red if the port is closed
        if not self.is_port_open:
            self.status = "red"
            self.message = "Could not connect to microsoft teams."
        
    def port_open(self):
        self.is_port_open = Socket("teams.microsoft.com", 443).run()
        return self.is_port_open