from seethrufeeds.model.components.component_base import ComponentBase
from seethrufeeds.model.Properties.properties import FillableProperty, ResultProperty
import socket


class PortOpen(ComponentBase):
    TARGET_HOST = FillableProperty(
        name="target_host", required=True, of_type=str)
    PORT = FillableProperty(name="port", default=443,
                            required=True, of_type=int)
    SUCCEEDED = ResultProperty(name="succeeded")

    Component_Title = "PortOpen Socket Component"
    Component_Description = "This component will test to see if it can open a tcp connection with the given host and port"
    Component_Author = "SeeThru Networks"
    Component_Owner = "SeeThru Networks"

    def component_execute(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)

        try:
            # Attempts a connection to the socket
            sock.connect((self.get_property(PortOpen.TARGET_HOST),
                          self.get_property(PortOpen.PORT)))
            sock.close()
            self.set_property(PortOpen.SUCCEEDED, True)
        except:
            self.set_property(PortOpen.SUCCEEDED, False)


class UDPPortOpen(ComponentBase):
    TARGET_HOST = FillableProperty(
        name="target_host", required=True, of_type=str)
    PORT = FillableProperty(name="port", default=443,
                            required=True, of_type=int)
    # Stores whether the udp data send was successful
    SUCCEEDED = ResultProperty(name="succeeded")
    # If not successful, then this stores the os level error number for the socket connection
    ERROR_NO = ResultProperty(name="error_no", default=0)

    Component_Title = "UDPPortOpen Socket Component"
    Component_Description = "This component will test to see if it can send data over a udp socket with the given host and port"
    Component_Author = "SeeThru Networks"
    Component_Owner = "SeeThru Networks"

    def component_execute(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(5)

        try:
            # Attempts a connection to the socket
            sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            sock.sendto(b"Test", (self.get_property(
                self.TARGET_HOST), self.get_property(self.PORT)))
            sock.close()
            self.set_property(self.SUCCEEDED, True)
        except socket.error as error:
            self.set_property(self.ERROR_NO, error.errno)
            self.set_property(self.SUCCEEDED, False)
        except:
            self.set_property(self.SUCCEEDED, False)
