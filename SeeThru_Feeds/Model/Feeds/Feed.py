import json

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

    def set_script(self, script):
        self.ScriptResult = script.get_result()

    def set_guid(self, guid):
        self.Guid = guid

    def set_script_result(self, result):
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
        response_json = json.loads(response.content)
        if not response_json["success"]:
            return response_json["message"]
        return ""

    @staticmethod
    def generate(access_token: str, secret: str, name: str, description: str) -> "Feed":
        headers = {
            "X-Access-Token": access_token,
            "X-Secret": secret
        }
        data = {
            "name": name,
            "description": description,
        }

        response = requests.post("https://api.seethrunetworks.com/feed/create", data=data, headers=headers)

        # TODO: Throw custom exceptions for different errors
        response_json = json.loads(response.content)
        if response.status_code != 200:
            raise Exception(response_json["message"])

        if not response_json["success"]:
            raise Exception(response_json["message"])

        # Returns a new feed
        guid = response_json["result"]["guid"]
        feed = Feed()
        feed.set_api_key(access_token=access_token, secret=secret)
        feed.set_guid(guid)
        return feed
