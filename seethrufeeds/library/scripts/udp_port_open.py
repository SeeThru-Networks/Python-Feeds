from seethrufeeds.model.Scripts.script_state import DefaultStates, State, StateEngine
from seethrufeeds.model.Scripts.script_base import ScriptBase
from seethrufeeds.model.Properties.properties import FillableProperty, ResultProperty
from seethrufeeds.library.components.socket import UDPPortOpen as PortOpen
import os


class UDPPortOpen(ScriptBase, StateEngine):
    class MessageStates(DefaultStates):
        port_closed = State("port_closed", State.error, "Cannot create a tcp socket to given host and port")

    host = FillableProperty(name="host", required=True, of_type=str)
    port = FillableProperty(name="port", required=False, of_type=[str, int], default=443)

    is_port_open = ResultProperty(name="is_port_open")
    # Stores the error Message given by UDPPortOpen component
    ERROR_MSG = ResultProperty(name="error_msg", default=None)

    Attr_Title = "UDP Port Open"
    Attr_Description = "A script which tests sending data with a udp socket to a given host and port"
    Attr_Author = "SeeThru Networks"
    Attr_Owner = "SeeThru Networks"

    # ------ Script Overrides ------
    def script_run(self):
        udp_test = PortOpen()\
            .set_property(PortOpen.TARGET_HOST, self.host.value)\
            .set_property(PortOpen.PORT, self.port.value)\
            .run()
        self.is_port_open.value = udp_test.SUCCEEDED.value
        self.assert_true(self.is_port_open.value, self.MessageStates.port_closed)

        # Sets the error Message if any
        error_no = udp_test.get_property(PortOpen.ERROR_NO)
        if error_no:
            self.set_property(self.ERROR_MSG, os.strerror(error_no))
