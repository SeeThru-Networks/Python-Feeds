from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptBase
from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptResult
from SeeThru_Feeds.Model.Properties.Properties import FillableProperty, ResultProperty
from SeeThru_Feeds.Library.Components.Socket import PortOpen
import socket


class TCPPortOpen(ScriptBase):
    HOST = FillableProperty(name="host", required=True, of_type=str)
    PORT = FillableProperty(name="port", required=False,
                            of_type=[str, int], default=443)

    IS_PORT_OPEN = ResultProperty(name="is_port_open")

    Script_Title = "TCP Port Open"
    Script_Description = "A script which tests creating a tcp socket to a given host and port"
    Script_Author = "SeeThru Networks"
    Script_Owner = "SeeThru Networks"

    # ------ Script Overrides ------
    def script_run(self):
        host = self.get_property(self.HOST)
        port = self.get_property(self.PORT)
        is_port_open = PortOpen().set_property(PortOpen.TARGET_HOST, host).set_property(
            PortOpen.PORT, port).run().get_property(PortOpen.SUCCEEDED)
        self.set_property(self.IS_PORT_OPEN, is_port_open)

    def script_evaluate(self, result):
        result.set_status("green")
        result.set_message("")

        # Changes to red if the port is closed
        if not self.get_property(self.IS_PORT_OPEN):
            result.set_status("red")
            result.set_message(
                "Could not create a tcp socket to given host and port")
