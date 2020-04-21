import requests
from Library.Components.HTTP.HTTPBase import HTTPBase


class HTTPGet(HTTPBase):

    def __init__(self, target):
        super().__init__()
        self.target_path = target

    def run(self):
        self.response = requests.get(self.target_path, cookies=self.cookies)