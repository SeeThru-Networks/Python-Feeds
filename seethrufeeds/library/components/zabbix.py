from seethrufeeds.model.components.component_base import ComponentBase
from seethrufeeds.model.Properties.properties import FillableProperty, ResultProperty

from typing import List, Union

from pyzabbix.api import ZabbixAPI


class HistoryValue:
    clock: int
    itemid: str
    ns: int

    def __init__(self, data):
        for key in data.keys():
            if key == "value":
                if "_set_value" in dir(self):
                    self._set_value(data[key])
                    continue
            setattr(self, key, data[key])


class FloatHistory(HistoryValue):
    value: float

    def _set_value(self, value):
        self.value = float(value)


class IntegerHistory(HistoryValue):
    value: int

    def _set_value(self, value):
        self.value = int(value)


class StringHistory(HistoryValue):
    value: str


class TextHistory(HistoryValue):
    id: str
    value: str


class LogHistory(HistoryValue):
    id: str
    logeventid: int
    severity: int
    source: str
    timestamp: int
    value: str


class ZabbixItem:
    itemid: str
    delay: str
    hostid: str
    interfaceid: str
    key_: str
    name: str
    type: int
    url: str
    value_type: int
    allow_traps: int
    authtype: int
    description: str
    error: str
    flags: int
    follow_redirects: int
    headers: dict
    history: str
    http_proxy: str
    inventory_link: int
    ipmi_sensor: str
    jmx_endpoint: str
    lastclock: int
    lastns: int
    lastvalue: str
    logtimefmt: str
    master_itemid: int
    output_format: int
    params: str
    password: str
    post_type: int
    posts: str
    prevvalue: str
    privatekey: str
    publickey: str
    query_fields: list
    request_method: int
    retrieve_method: int
    retrieve_mode: int
    snmp_oid: str
    ssl_cert_file: str
    ssl_key_file: str
    ssl_key_password: str
    state: int
    status: int
    stauts_codes: str
    templateid: str
    timeout: str
    trapper_hosts: str
    trends: str
    units: str
    username: str
    valuemapid: str
    verify_host: int
    verify_peer: int

    value_history: List[Union[FloatHistory, IntegerHistory, StringHistory, TextHistory, LogHistory]]

    def __init__(self, item_data):
        for key in item_data.keys():
            setattr(self, key, item_data[key])
        self.value_history = []


class Zabbix(ComponentBase):
    url = FillableProperty("url", required=True, of_type=str)
    username = FillableProperty("username", required=True, of_type=str)
    password = FillableProperty("password", required=True, of_type=str)
    """
    The host that contains the items
    """
    host = FillableProperty("host", required=True, of_type=str)
    history_count = FillableProperty("history_count", required=False, default=10, of_type=int)

    items = ResultProperty("items")

    Component_Title = "Zabbix Component"
    Component_Description = "Gets the recent history of every item of a zabbix host"
    Component_Author = "SeeThru Networks"
    Component_Owner = "SeeThru Networks"

    def component_execute(self):
        with ZabbixAPI(url=self.url.value, user=self.username.value, password=self.password.value) as zabbix:
            # Gets all of the items for the given host
            # noinspection PyTypeChecker
            api_items = zabbix.do_request("item.get", {
                "output": "extend",
                "filter": {
                    "host": [
                        self.host.value
                    ]
                },
                "sortfield": "name"
            })
            # Converts the items into an internal representation
            self.items.value = []
            # Stores a mapping between id and item
            mapping = {}
            for item in api_items["result"]:
                newItem = ZabbixItem(item)
                self.items.value.append(newItem)
                mapping[newItem.itemid] = newItem

            # Gets the value history for each item
            # noinspection PyTypeChecker
            history = zabbix.do_request("history.get", {
                "output": "extend",
                "history": 0,
                "itemids": [item.itemid for item in self.items.value],
                "sortfield": "clock",
                "sortorder": "DESC",
                "limit": self.history_count.value * len(self.items.value)
            })

            # Adds the history to each item
            for historyValue in history["result"]:
                item = mapping[historyValue["itemid"]]
                if item.value_type == '0':  # Numeric Float
                    item.value_history.append(FloatHistory(historyValue))
                elif item.value_type == '1':  # Character
                    item.value_history.append(StringHistory(historyValue))
                elif item.value_type == '2':  # Log
                    item.value_history.append(LogHistory(historyValue))
                elif item.value_type == '3':  # Numeric unsigned (int)
                    item.value_history.append(IntegerHistory(historyValue))
                elif item.value_type == '4':  # Text
                    item.value_history.append(TextHistory(historyValue))
