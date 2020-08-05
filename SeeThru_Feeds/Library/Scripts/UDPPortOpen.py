from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptBase
from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptResult
from SeeThru_Feeds.Model.Properties.Properties import FillableProperty, ResultProperty
from SeeThru_Feeds.Library.Components.Socket import UDPPortOpen as PortOpen
import socket
import os


class UDPPortOpen(ScriptBase):
    HOST = FillableProperty(name="host", required=True, of_type=str)
    PORT = FillableProperty(name="port", required=False,
                            of_type=[str, int], default=443)

    IS_PORT_OPEN = ResultProperty(name="is_port_open")
    # Stores the error Message given by UDPPortOpen component
    ERROR_MSG = ResultProperty(name="error_msg", default=None)

    Script_Title = "UDP Port Open"
    Script_Description = "A script which tests sending data with a udp socket to a given host and port"
    Script_Author = "SeeThru Networks"
    Script_Owner = "SeeThru Networks"

    # ------ Script Overrides ------
    def script_run(self):
        host = self.get_property(self.HOST)
        port = self.get_property(self.PORT)
        udp_test = PortOpen().set_property(PortOpen.TARGET_HOST,
                                           host).set_property(PortOpen.PORT, port).run()
        self.set_property(self.IS_PORT_OPEN,
                          udp_test.get_property(PortOpen.SUCCEEDED))
        # Sets the error Message if any
        error_no = udp_test.get_property(PortOpen.ERROR_NO)
        if error_no:
            self.set_property(self.ERROR_MSG, os.strerror(error_no))

    def script_evaluate(self, result):
        result.set_status("green")
        result.set_message("")

        # Changes to red if the port is closed
        if not self.get_property(self.IS_PORT_OPEN):
            result.set_status("red")
            result.set_message(
                "Could not create a tcp socket to given host and port")
        # IF there is an error Message given by the os, then that is used
        if self.get_property(self.ERROR_MSG) != None:
            result.set_status("red")
            result.set_message(self.get_property(self.ERROR_MSG))
