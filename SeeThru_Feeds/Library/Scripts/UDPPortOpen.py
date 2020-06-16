from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptBase
from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptResult
from SeeThru_Feeds.Model.Properties.Properties import FillableProperty, ResultProperty
from SeeThru_Feeds.Library.Components.Socket import UDPPortOpen as PortOpen
import socket, os

class UDPPortOpen(ScriptBase):
    HOST = FillableProperty(name="host", required=True, ofType=str)
    PORT = FillableProperty(name="port", required=False, ofType=[str, int], default=443)

    IS_PORT_OPEN = ResultProperty(name="is_port_open")
    # Stores the error message given by UDPPortOpen component
    ERROR_MSG = ResultProperty(name="error_msg", default=None)

    Script_Title = "UDP Port Open"
    Script_Description = "A script which tests sending data with a udp socket to a given host and port"
    Script_Author = "SeeThru Networks"
    Script_Owner = "SeeThru Networks"

    # ------ Script Overrides ------
    def Script_Run(self): 
        host = self.GetProperty(self.HOST)
        port = self.GetProperty(self.PORT)
        udp_test = PortOpen().SetProperty(PortOpen.TARGET_HOST, host).SetProperty(PortOpen.PORT, port).Run()
        self.SetProperty(self.IS_PORT_OPEN, udp_test.GetProperty(PortOpen.SUCCEEDED))
        #Sets the error message if any
        error_no = udp_test.GetProperty(PortOpen.ERROR_NO)
        if error_no: 
            self.SetProperty(self.ERROR_MSG, os.strerror(error_no))

    def Script_Evaluate(self, result):
        result.SetStatus("green")
        result.SetMessage("")

        # Changes to red if the port is closed
        if not self.GetProperty(self.IS_PORT_OPEN):
            result.SetStatus("red")
            result.SetMessage("Could not create a tcp socket to given host and port")
        # IF there is an error message given by the os, then that is used
        if self.GetProperty(self.ERROR_MSG) != None:
            result.SetStatus("red")
            result.SetMessage(self.GetProperty(self.ERROR_MSG))