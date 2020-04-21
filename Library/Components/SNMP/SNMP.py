# Connects to an SNMP feed, performs an SNMP Walk,
# and filters it to get the contents within a specified OID value.

from Model.ComponentBase import ComponentBase
from pysnmp.hlapi import *


class SNMP(ComponentBase):

    def __init__(self, host, community):
        self.host = host
        self.port = 161
        self.community = community

    def get_value(self, oid, search_oid):
        value = ""

        # For every entry in the SNMP table.
        for errorIndication, errorStatus, errorIndex, varBinds in bulkCmd(
                SnmpEngine(),
                CommunityData(self.community),
                UdpTransportTarget((self.host, self.port)),
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
        return value
