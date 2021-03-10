from seethrufeeds.model.components.component_base import ComponentBase
from seethrufeeds.model.Properties.properties import FillableProperty, ResultProperty
import mysql.connector


class ConnectionOpen(ComponentBase):
    HOST = FillableProperty(name="Host", required=True)
    USER = FillableProperty(name="User", required=True)
    PASSWD = FillableProperty(name="password", required=True)
    DATABASE = FillableProperty(name="Database", required=True)
    CAN_CONNECT = ResultProperty(name="Can_Connect")

    Component_Title = "ConnectionOpen Database Component"
    Component_Description = "This component tests to see if it can open a database connection with the given details"
    Component_Author = "SeeThru Networks"
    Component_Owner = "SeeThru Networks"

    def component_execute(self):
        try:
            connection = mysql.connector.connect(
                host=self.get_property(ConnectionOpen.HOST),
                user=self.get_property(ConnectionOpen.USER),
                passwd=self.get_property(ConnectionOpen.PASSWD),
                database=self.get_property(ConnectionOpen.DATABASE)
            )
            connection.close()
            # Assumes that a valid connection was made
            self.set_property(ConnectionOpen.CAN_CONNECT, True)
        except:
            self.set_property(ConnectionOpen.CAN_CONNECT, False)
