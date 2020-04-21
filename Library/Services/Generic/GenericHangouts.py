from Library.Components.Sockets.Socket import Socket
from Library.Components.HTTP.HTTPGet import HTTPGet
from Model.ServiceBase import ServiceBase
import json

class GenericHangoutsService(ServiceBase):

    def __init__(self, **kwargs):
        super().__init__("GenericHangoutsService", **kwargs)
        #Stores whether there is an issue with google hangouts
        self.hangouts_error = False

    def run(self):
        if not self.port_open():
            self.evaluate(None)
            return

        self.get_status_page()

        self.evaluate(None)

    def evaluate(self, value):
        # Takes the result to evaluate it
        self.status = "green"
        self.message = ""

        # Changes to red if the port is closed
        if not self.is_port_open:
            self.status = "red"
            self.message = "Could not connect to google hangouts."
        
        #Checks if there is a hangouts error
        if self.hangouts_error:
            self.status = "red"
            self.message = "There is an issue with hangouts, please look at https://www.google.com/appsstatus/json/en"

    def port_open(self):
        self.is_port_open = Socket("hangouts.google.com", 443).run()
        return self.is_port_open

    def get_status_page(self):
        #Gets the google status page json
        page = HTTPGet("https://www.google.com/appsstatus/json/en")
        page.run()
        try:
            #Converts the response to json, ommiting dashboard.jsonp
            response = json.loads(page.get_response()[16:-2])
            #Loops through all the messages and finds any google hangouts messages
            for i in range(len(response['messages'])-1, 0, -1):
                message = response['messages'][i]
                #The google hangouts id in the json response is 22
                if message['service'] == 22:
                    #A type code of 3 seems to signify that the issue has been resolved, otherwise there may be an issue
                    self.hangouts_error = not message['type'] == 3
                    return
        except:
            return