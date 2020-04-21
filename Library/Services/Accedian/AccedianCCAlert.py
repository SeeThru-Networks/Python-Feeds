from Library.Components.SNMP.SNMP import SNMP
from Model.ServiceBase import ServiceBase


class AccedianCCAlert(ServiceBase):

    def __init__(self, host, community, oid, search_oid, **kwargs):
        super().__init__("AccedianCCAlert", **kwargs)
        self.host = host
        self.community = community
        self.oid = oid
        self.search_oid = search_oid

    def run(self):
        value = self.get_value()
        self.evaluate(value)

    def get_value(self):
        # Obtains a CC value from an accedian unit.
        snmp = SNMP(self.host, self.community)
        return snmp.get_value(self.oid, self.search_oid)

    def evaluate(self, value):
        # Takes a CC alert value and evaluates it.

        if value == "1":
            self.status = "red"
            self.message = "There is a CC alert."

        elif value == "2":
            self.status = "green"
            self.message = "There is no CC alert."

        else:
            self.status = "red"
            self.message = "Could not connect to the SNMP feed or locate a CC alert."
