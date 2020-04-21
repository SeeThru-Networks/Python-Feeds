from Model.ComponentBase import ComponentBase


class HTTPBase(ComponentBase):

    def __init__(self):
        self.target_path = None
        self.cookies = None
        self.response = None

    def set_cookies(self, cookies):
        self.cookies = cookies

    def get_cookies(self):
        return self.response.cookies

    def get_response(self):
        return self.response.text

    def get_status_code(self):
        return self.response.status_code

    def get_response_url(self):
        return self.response.url
