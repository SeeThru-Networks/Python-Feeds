from Library.Components.Sockets.Socket import Socket
from Library.Components.HTTP.HTTPGet import HTTPGet
from Model.ServiceBase import ServiceBase
import json

class GenericZoomService(ServiceBase):

    def __init__(self, **kwargs):
        super().__init__("GenericZoomService", **kwargs)
        #Stores whether all the systems are operational
        self.all_operational = False
        self.status_valid_json = True

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
            self.message = "Could not connect to zoom."
        
        #Changes to red if the status page couldn't be accessed
        elif not self.status_valid_json:
            self.status = "red"
            self.message = "Could not load statistics"
        
        #Changes to amber if not all the zoom systems are operational
        elif not self.all_operational:
            self.status = "amber"
            self.message = "Not all systems are operational, head to status.zoom.us"

    def port_open(self):
        self.is_port_open = Socket("zoom.us", 443).run()
        return self.is_port_open

    def get_status_page(self):
        #Gets the statuspage io page
        page = HTTPGet("https://14qjgk812kgk.statuspage.io/api/v2/status.json")
        page.run()
        try:
            #Gets the contents of the response
            contents = json.loads(page.get_response())

            self.all_operational = contents['status']['description'] == "All Systems Operational"
            if not self.all_operational:
                try:
                    file = open("/var/lib/seethru/zoomOutageLog.log", "a")
                    file.write(page.get_response())
                    file.close()
                except:
                    file = open("/var/lib/seethru/zoomOutageLog.log", "w")
                    file.write(page.get_response())
                    file.close()
        except:
            self.status_valid_json = False