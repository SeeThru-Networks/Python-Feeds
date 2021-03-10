import unittest
from uuid import UUID

from seethrufeeds.feeds.api_key import ApiKey
from seethrufeeds.feeds.exceptions import InvalidAccessToken, InvalidSecretKey


class ApiKeyTestCase(unittest.TestCase):
    def test_api_key(self):
        api_key = ApiKey(UUID("0e3fa201-59b5-47bb-a875-e379ec3cd724"),
                         "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(api_key)
        self.assertEqual(str(api_key.access_token), "0e3fa201-59b5-47bb-a875-e379ec3cd724")
        self.assertEqual(str(api_key.secret_key), "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        self.assertRaises(InvalidAccessToken, ApiKey, "0e3fa201-59b5-47bb-a875-e379ec3cd724",
                                             "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        self.assertRaises(InvalidSecretKey, ApiKey, UUID("0e3fa201-59b5-47bb-a875-e379ec3cd724"), 2)

        self.assertRaises(InvalidSecretKey, ApiKey, UUID("0e3fa201-59b5-47bb-a875-e379ec3cd724"), "asfgbg")


if __name__ == '__main__':
    unittest.main()
