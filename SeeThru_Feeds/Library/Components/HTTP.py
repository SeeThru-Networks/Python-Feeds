from SeeThru_Feeds.Model.Components.ComponentBase import ComponentBase
from SeeThru_Feeds.Model.Properties.Properties import FillableProperty, ResultProperty
import requests


class HTTPBase(ComponentBase):
    URL = FillableProperty(name="url", required=True)
    COOKIES = FillableProperty(name="cookies", required=False)
    HEADERS = FillableProperty(name="header", oftype=dict, required=False, default=None)
    RESPONSE = ResultProperty(name="response")
    STATUS_CODE = ResultProperty(name="status_code")
    RESPONSE_CONTENT = ResultProperty(name="response_content")
    RESPONSE_URL = ResultProperty(name="response_url")

    Component_Title = "HTTP Component"
    Component_Description = "This component provides a wrapper over the requests http methods to make them follow the component design rules"
    Component_Author = "SeeThru Networks"
    Component_Owner = "SeeThru Networks"


class HTTPGet(HTTPBase):
    def Component_Execute(self):
        response = requests.get(self.GetProperty(
            HTTPBase.URL), cookies=self.GetProperty(HTTPBase.COOKIES), headers=self.GetProperty(HTTPBase.HEADERS))

        self.SetProperty(HTTPGet.RESPONSE, response)
        self.SetProperty(HTTPGet.STATUS_CODE, response.status_code)
        self.SetProperty(HTTPGet.COOKIES, response.cookies)
        self.SetProperty(HTTPGet.RESPONSE_CONTENT, response.text)
        self.SetProperty(HTTPGet.RESPONSE_URL, response.url)


class HTTPPost(HTTPBase):
    DATA = FillableProperty(name="data")
    JSON = FillableProperty(name="json", ofType=dict, required=False)
    CONTENT_TYPE = FillableProperty(
        name="content_type", default="application/x-www-form-urlencoded")

    def Component_Execute(self):
        if self.GetProperty(HTTPBase.HEADERS) is None:
            self.SetProperty(HTTPBase.HEADERS, {'Content-Type': self.GetProperty(self.CONTENT_TYPE)})

        response = requests.post(
            self.GetProperty(HTTPPost.URL),
            cookies=self.GetProperty(HTTPPost.COOKIES),
            data=self.GetProperty(HTTPPost.DATA),
            json=self.GetProperty(HTTPPost.JSON),
            headers=self.GetProperty(HTTPBase.HEADERS)
        )
        self.SetProperty(HTTPPost.RESPONSE, response)
        self.SetProperty(HTTPPost.STATUS_CODE, response.status_code)
        self.SetProperty(HTTPPost.RESPONSE_CONTENT, response.text)
        self.SetProperty(HTTPPost.RESPONSE_URL, response.url)
