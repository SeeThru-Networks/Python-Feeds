import unittest

from seethrufeeds.feeds.feed_result import StatusEnum
from seethrufeeds.model.scripts.script_base import ScriptBase
from seethrufeeds.model.scripts.script_state import StatesEnum


class ScriptTestCase(unittest.TestCase):
    def test_script_attribution(self):
        # Creates a test script
        class TestScript(ScriptBase):
            attribute_title = "Test Script"
            attribute_author = "Test Author"

            def run(self): pass

        instance = TestScript()

        self.assertEqual(instance.get_title(), "Test Script")
        self.assertEqual(instance.get_author(), "Test Author")
        self.assertRaises(NotImplementedError, instance.get_description)
        self.assertRaises(NotImplementedError, instance.get_docs_link)
        self.assertRaises(NotImplementedError, instance.get_license_link)
        self.assertRaises(NotImplementedError, instance.get_support_link)

    def test_script_state(self):
        # Creates a test script
        class TestScript(ScriptBase):
            def run(self):
                self.state = StatesEnum.error

        instance = TestScript()
        instance.run()

        result = instance.get_result()
        self.assertEqual(result.status, StatusEnum.red)
        self.assertEqual(result.message, "Error message")

        instance.state = ""
        self.assertRaises(TypeError, instance.get_result)


if __name__ == '__main__':
    unittest.main()
