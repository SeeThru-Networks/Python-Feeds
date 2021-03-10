from seethrufeeds.model.Scripts.script_state import State, DefaultStates, StateEngine
from seethrufeeds.model.Scripts.script_base import ScriptBase
from seethrufeeds.model.Properties.properties import FillableProperty, ResultProperty
from seethrufeeds.library.components.socket import PortOpen


class TCPPortOpen(ScriptBase, StateEngine):
    class MessageStates(DefaultStates):
        port_closed = State("port_closed", State.error, "Cannot create a tcp socket to given host and port")

    host = FillableProperty(name="host", required=True, of_type=str)
    port = FillableProperty(name="port", required=False, of_type=[str, int], default=443)

    is_port_open = ResultProperty(name="is_port_open")

    Attr_Title = "TCP Port Open"
    Attr_Description = "A script which tests creating a tcp socket to a given host and port"
    Attr_Author = "SeeThru Networks"
    Attr_Owner = "SeeThru Networks"

    # ------ Script Overrides ------
    def script_run(self):
        # Checks to see if the port is open for tcp connections
        is_port_open = PortOpen()\
            .set_property(PortOpen.TARGET_HOST, self.host.value)\
            .set_property(PortOpen.PORT, self.port.value)\
            .run()\
            .get_property(PortOpen.SUCCEEDED)

        self.is_port_open.value = is_port_open

        # Sets the state to port closed
        if not self.is_port_open.value:
            self.set_state(self.MessageStates.port_closed)
