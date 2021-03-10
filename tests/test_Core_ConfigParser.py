from unittest import TestCase
import seethrufeeds.core.config_parser as ConfigParser


class TestCoreConfigParser(TestCase):
    def test_create_config(self):
        config = ConfigParser.Config.new("Generic")
        self.assertTrue(config.Header.Scheme_Name == "Generic")

        config.add_script("Foo")
        self.assertTrue(len(config.Scripts) == 1)
        self.assertTrue(config.Scripts["Foo"].Meta.Script_Object_Path == "Scripts.Foo@Foo")
        self.assertTrue(config.Scripts["Foo"].Meta.Script_Output_Path == "Outputs/Foo")

        config.add_api_key("Api_Key", "Access_Token", "Secret")
        self.assertTrue(len(config.Api_Keys) == 1)
        self.assertTrue(config.Api_Keys["Api_Key"].Access_Token == "Access_Token")
        self.assertTrue(config.Api_Keys["Api_Key"].Secret == "Secret")

        config.add_feed("Foo", "Foo", "Foo", "guid")
        self.assertTrue(len(config.Feeds) == 1)
        self.assertTrue(config.Feeds["Foo"].Script == "Foo")
        self.assertTrue(config.Feeds["Foo"].Api_Key == "Foo")
        self.assertTrue(config.Feeds["Foo"].Guid == "guid")

    def test_dump_config(self):
        config = ConfigParser.Config.new("Generic")
        google = config.add_script("Google")
        google.add_fillable("host", "https://google.com")
        config.add_feed("GoogleFeed", "Google", "Default", "abcdefgh-ijkl-mnop-qrst-uvwxyz123456")
        output = config.dump()
        self.assertTrue("Header" in output)

        self.assertTrue("Scripts" in output)
        self.assertTrue("Google" in output["Scripts"])
        self.assertTrue("Meta" in output["Scripts"]["Google"])
        self.assertTrue("Script_Name" in output["Scripts"]["Google"]["Meta"])
        self.assertTrue(output["Scripts"]["Google"]["Meta"]["Script_Name"] == "Google")
        self.assertTrue("Script_Object_Path" in output["Scripts"]["Google"]["Meta"])
        self.assertTrue(output["Scripts"]["Google"]["Meta"]["Script_Object_Path"] == "Scripts.Google@Google")
        self.assertTrue("Script_Output_Path" in output["Scripts"]["Google"]["Meta"])
        self.assertTrue(output["Scripts"]["Google"]["Meta"]["Script_Output_Path"] == "Outputs/Google")

        self.assertTrue("Fillables" in output["Scripts"]["Google"])
        self.assertTrue("host" in output["Scripts"]["Google"]["Fillables"])
        self.assertTrue(output["Scripts"]["Google"]["Fillables"]["host"] == "https://google.com")

        self.assertTrue("Feeds" in output)
        self.assertTrue("GoogleFeed" in output["Feeds"])
        self.assertTrue(output["Feeds"]["GoogleFeed"]['Script'] == "Google")
        self.assertTrue(output["Feeds"]["GoogleFeed"]['Api_Key'] == "Default")
        self.assertTrue(output["Feeds"]["GoogleFeed"]['Guid'] == "abcdefgh-ijkl-mnop-qrst-uvwxyz123456")

    def test_add_scriptstate(self):
        config = ConfigParser.Config.new("Generic")
        google = config.add_script("Google")
        google.add_state("OK", "green", "Test message")

        self.assertTrue(config.Scripts["Google"].States["OK"].Name == "OK")
        self.assertTrue(config.Scripts["Google"].States["OK"].Status == "green")
        self.assertTrue(config.Scripts["Google"].States["OK"].Message == "Test message")

        output = config.dump()
        self.assertTrue(output["Scripts"]["Google"]["States"]["OK"]["Name"] == "OK")
        self.assertTrue(output["Scripts"]["Google"]["States"]["OK"]["Status"] == "green")
        self.assertTrue(output["Scripts"]["Google"]["States"]["OK"]["Message"] == "Test message")
