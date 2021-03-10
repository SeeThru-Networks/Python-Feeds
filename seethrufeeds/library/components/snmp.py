from seethrufeeds.model.components.component_base import ComponentBase
from seethrufeeds.model.Properties.properties import FillableProperty, ResultProperty
from pysnmp.hlapi import *


class SNMPWalkToOID(ComponentBase):
    SNMP_HOST = FillableProperty(name="snmp_host", required=True, of_type=str)
    SNMP_PORT = FillableProperty(
        name="snmp_port", default=161, required=True, of_type=int)
    COMMUNITY = FillableProperty(name="community", required=True)

    VALUE = ResultProperty(name="oid_value")

    Component_Title = "SNMP Walk"
    Component_Description = "Connects to an SNMP feed, performs an SNMP Walk, and filters it to get the contents within a specified OID value"
    Component_Author = "SeeThru Networks"
    Component_Owner = "SeeThru Networks"

    def component_execute(self):
        value = ""

        # For every entry in the SNMP table.
        for errorIndication, errorStatus, errorIndex, varBinds in bulkCmd(
                SnmpEngine(),
                CommunityData(self.get_property(self.COMMUNITY)),
                UdpTransportTarget(
                    (self.get_property(self.SNMP_HOST), self.get_property(self.SNMP_PORT))),
                ContextData(),
                0, 50,
                ObjectType(ObjectIdentity(oid)),
                maxCalls=10
        ):
            # Clear the store for the OID key = value pair.
            value = ""

            # Do nothing if there was an SNMP error and return the value ""
            if errorIndication or errorStatus:
                break

            else:
                # Otherwise, take the OID key = value pairs and populate the value store.
                for varBind in varBinds:
                    value = (' = '.join([x.prettyPrint() for x in varBind]))

                # If the entry is the one we're looking for, then remove the "key = "
                # prefix from the value string and return the raw value.
                if search_oid in value:
                    value = value.replace(search_oid + " = ", "")
                    break

            # Then move onto the next OID entry in the SNMP feed.

        # Once we call break, the last value will be outputted
        self.set_property(self.VALUE, value)
