from Model.ServiceBase import ServiceBase
from zabbix_api import ZabbixAPI


class ZabbixService(ServiceBase):

    # TODO: service_id might need to be dynamic in future, use service.get to search services by name.

    def __init__(self, host, username, password, service_id, **kwargs):
        super().__init__("ZabbixService", **kwargs)
        self.host = host
        self.username = username
        self.password = password
        self.service_id = service_id

    def run(self):
        value = self.get_value()
        self.evaluate(value)

    def get_value(self):
        # Obtains a status value from the Zabbix Service.
        zapi = ZabbixAPI(self.host)
        zapi.validate_certs = False
        zapi.login(self.username, self.password)

        response = zapi.service.getsla({"serviceids": str(self.service_id)})

        return response[str(self.service_id)]['status']

    def evaluate(self, value):
        # Take response from Zabbix and evaluate RAG.
        # Check that the value is actually an int, not a NoneType (i.e. connection error)

        if value == "0":
            self.status = "green"
            self.message = ""

        elif value == "2" or value == "4":
            self.status = "red"
            self.message = "The Zabbix service is in an Error state."

        else:
            self.status = "red"
            self.message = "Unexpected response from Zabbix."
