from seethrufeeds.model.Scripts.script_state import State, DefaultStates, StateEngine
from seethrufeeds.model.Scripts.script_base import ScriptBase
from seethrufeeds.model.Properties.properties import FillableProperty, ResultProperty
import requests, json


class StatusPage(ScriptBase, StateEngine):
    class MessageStates(DefaultStates):
        cannot_load_status = State("cannot_load_status", State.amber, "The statuspage couldn't be loaded")
        ERROR = State("ERROR", State.red, "Partial System Outage")
        WARNING = State("WARNING", State.amber, "Minor Service Outage")
        OK = State("OK", State.green, "All Systems Operational")

    id = FillableProperty("id", required=True, of_type=str)

    def script_run(self):
        try:
            response = requests.get(f"https://{self.id.value}.statuspage.io/api/v2/status.json")
            try:
                statuspage = json.loads(response.content)
                # Gets the status
                self.assert_true("status" in statuspage, self.MessageStates.cannot_load_status)
                statuspage = statuspage["status"]

                self.assert_true("indicator" in statuspage, self.MessageStates.cannot_load_status)
                indicator = statuspage["indicator"]

                if indicator == "none":
                    self.set_state(self.MessageStates.OK)
                    return
                elif indicator == "minor":
                    self.set_state(self.MessageStates.WARNING)
                    return
                elif indicator == "major":
                    self.set_state(self.MessageStates.ERROR)
                else:
                    self.set_state(self.MessageStates.cannot_load_status)

            except:
                self.set_state(self.MessageStates.cannot_load_status)
        except:
            self.set_state(self.MessageStates.cannot_load_status)


if __name__=="__main__":
    page = StatusPage()
    page.configure_state("OK", "green", "Zoom is operational")
    page.configure_state("WARNING", "amber", "There is a minor issue with zoom")
    page.configure_state("ERROR", "red", "There is a major issue with zoom")
    page.id.value = "14qjgk812kgk"
    page.run_script().evaluate_script().log_output()
