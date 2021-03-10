from seethrufeeds.model.components.component_base import ComponentBase
from seethrufeeds.model.Properties.properties import FillableProperty, ResultProperty
import requests


class HTTPBase(ComponentBase):
    URL = FillableProperty(name="url", required=True)
    COOKIES = FillableProperty(name="cookies", required=False)
    HEADERS = FillableProperty(name="header", required=False, default=None, of_type=dict)
    RESPONSE = ResultProperty(name="response")
    STATUS_CODE = ResultProperty(name="status_code")
    RESPONSE_CONTENT = ResultProperty(name="response_content")
    RESPONSE_URL = ResultProperty(name="response_url")

    Component_Title = "HTTP Component"
    Component_Description = "This component provides a wrapper over the requests http methods to make them follow the component design rules"
    Component_Author = "SeeThru Networks"
    Component_Owner = "SeeThru Networks"


class HTTPGet(HTTPBase):
    def component_execute(self):
        response = requests.get(self.get_property(
            HTTPBase.URL), cookies=self.get_property(HTTPBase.COOKIES), headers=self.get_property(HTTPBase.HEADERS))

        self.set_property(HTTPGet.RESPONSE, response)
        self.set_property(HTTPGet.STATUS_CODE, response.status_code)
        self.set_property(HTTPGet.COOKIES, response.cookies)
        self.set_property(HTTPGet.RESPONSE_CONTENT, response.text)
        self.set_property(HTTPGet.RESPONSE_URL, response.url)


class HTTPPost(HTTPBase):
    DATA = FillableProperty(name="data")
    JSON = FillableProperty(name="json", of_type=dict, required=False)
    CONTENT_TYPE = FillableProperty(
        name="content_type", default="application/x-www-form-urlencoded")

    def component_execute(self):
        if self.get_property(HTTPBase.HEADERS) is None:
            self.set_property(HTTPBase.HEADERS, {'Content-Type': self.get_property(self.CONTENT_TYPE)})

        response = requests.post(
            self.get_property(HTTPPost.URL),
            cookies=self.get_property(HTTPPost.COOKIES),
            data=self.get_property(HTTPPost.DATA),
            json=self.get_property(HTTPPost.JSON),
            headers=self.get_property(HTTPBase.HEADERS)
        )
        self.set_property(HTTPPost.RESPONSE, response)
        self.set_property(HTTPPost.STATUS_CODE, response.status_code)
        self.set_property(HTTPPost.RESPONSE_CONTENT, response.text)
        self.set_property(HTTPPost.RESPONSE_URL, response.url)
