import unittest
from datetime import datetime

from seethrufeeds.feeds.feed_result import FeedResult, StatusEnum


class FeedResultTestCase(unittest.TestCase):
    def test_create_result(self):
        result = FeedResult(StatusEnum.ok, "Foo Bar")
        self.assertEqual(result.status, StatusEnum.ok)
        self.assertEqual(result.get_status(), StatusEnum.ok)
        self.assertEqual(result.get_status_value(), "green")
        self.assertEqual(result.message, "Foo Bar")
        self.assertEqual(result.get_message(), "Foo Bar")

        self.assertRaises(TypeError, FeedResult, "green", "Foo Bar")
        self.assertRaises(TypeError, FeedResult, StatusEnum.ok, "Foo Bar", "")

        timestamp = datetime.strptime("2021-02-03 15:15:15", "%Y-%m-%d %H:%M:%S")
        result = FeedResult(StatusEnum.ok, "", timestamp)
        self.assertEqual(result.get_timestamp_str(), "2021-02-03 15:15:15")


if __name__ == '__main__':
    unittest.main()
