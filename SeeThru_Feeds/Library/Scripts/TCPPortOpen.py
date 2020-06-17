from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptBase
from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptResult
from SeeThru_Feeds.Model.Properties.Properties import FillableProperty, ResultProperty
from SeeThru_Feeds.Library.Components.Socket import PortOpen
import socket


class TCPPortOpen(ScriptBase):
    HOST = FillableProperty(name="host", required=True, ofType=str)
    PORT = FillableProperty(name="port", required=False,
                            ofType=[str, int], default=443)

    IS_PORT_OPEN = ResultProperty(name="is_port_open")

    Script_Title = "TCP Port Open"
    Script_Description = "A script which tests creating a tcp socket to a given host and port"
    Script_Author = "SeeThru Networks"
    Script_Owner = "SeeThru Networks"

    # ------ Script Overrides ------
    def Script_Run(self):
        host = self.GetProperty(self.HOST)
        port = self.GetProperty(self.PORT)
        is_port_open = PortOpen().SetProperty(PortOpen.TARGET_HOST, host).SetProperty(
            PortOpen.PORT, port).Run().GetProperty(PortOpen.SUCCEEDED)
        self.SetProperty(self.IS_PORT_OPEN, is_port_open)

    def Script_Evaluate(self, result):
        result.SetStatus("green")
        result.SetMessage("")

        # Changes to red if the port is closed
        if not self.GetProperty(self.IS_PORT_OPEN):
            result.SetStatus("red")
            result.SetMessage(
                "Could not create a tcp socket to given host and port")
