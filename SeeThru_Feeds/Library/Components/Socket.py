from SeeThru_Feeds.Model.Components.ComponentBase import ComponentBase
from SeeThru_Feeds.Model.Properties.Properties import FillableProperty, ResultProperty
import socket

class PortOpen(ComponentBase):
    TARGET_HOST = FillableProperty(name="target_host", required=True, ofType=str)
    PORT = FillableProperty(name="port", default=443, required=True, ofType=int)
    SUCCEEDED = ResultProperty(name="succeeded")

    Component_Title = "PortOpen Socket Component"
    Component_Description = "This component will test to see if it can open a tcp connection with the given host and port"
    Component_Author = "SeeThru Networks"
    Component_Owner = "SeeThru Networks"

    def Component_Execute(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        try:
            # Attempts a connection to the socket
            sock.connect((self.GetProperty(PortOpen.TARGET_HOST), self.GetProperty(PortOpen.PORT)))
            sock.close()
            self.SetProperty(PortOpen.SUCCEEDED, True)
        except:
            self.SetProperty(PortOpen.SUCCEEDED, False)
