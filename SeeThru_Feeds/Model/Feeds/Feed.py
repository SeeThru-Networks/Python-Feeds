import json

from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptBase
from SeeThru_Feeds.Model.Scripts.ScriptResult import ScriptResult

import requests

class Feed:
    def __init__(self):
        self.AccessToken = None
        self.Secret = None
        self.Guid = None
        self.ScriptResult = None

    def set_api_key(self, access_token, secret):
        self.AccessToken = access_token
        self.Secret = secret

    def set_script(self, script: ScriptBase):
        self.ScriptResult = script.get_result()

    def set_guid(self, guid: str):
        self.Guid = guid

    def set_script_result(self, result: ScriptResult):
        self.ScriptResult = result

    def push(self):
        headers = {
            "X-Access-Token": self.AccessToken,
            "X-Secret": self.Secret
        }
        data = {
            "guid": self.Guid,
            "color": self.ScriptResult.get_status(),
            "message": self.ScriptResult.get_message(),
            "timestamp": self.ScriptResult.get_timestamp(),
            "version": "2020.1.1"
        }

        response = requests.post(f"https://api.seethrunetworks.com/feed/{self.Guid}/update", data=data, headers=headers)

        if response.status_code != 200:
            return False
        responseJson = json.loads(response.content)
        if not responseJson["success"]:
            return responseJson["message"]
        return ""
