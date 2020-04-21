import requests
from Library.Components.HTTP.HTTPBase import HTTPBase


class HTTPPost(HTTPBase):

    def __init__(self, target_path, data, json=None, content_type="application/x-www-form-urlencoded"):
        super().__init__()
        self.target_path = target_path
        self.data = data
        self.json = json
        self.content_type = content_type

    def run(self):
        self.response = requests.post(
            self.target_path,
            cookies=self.cookies,
            data=self.data,
            json=self.json,
            headers={'Content-Type': self.content_type}
        )
