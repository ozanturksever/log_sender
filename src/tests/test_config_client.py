import unittest
from src.helpers.config.config_client import ConfigClient
from src.helpers.config.config import Config
from src.tests import test_helper
from src.tests.test_helper import CONFIG_FILE, TEST_CONFIG_CONTENT, TEST_LOG_FILE0, TEST_LOG_FILE1

class test_config_client(unittest.TestCase):
    def setUp(self):
        test_helper.setUp()
        self.config_server = Config(config_file=CONFIG_FILE)
        self.config_client = ConfigClient()

    def tearDown(self):
        test_helper.tearDown()
        self.config_client.shutdown()
        self.config_server.shutdown()

    def test_can_construct(self):
        self.assertTrue(self.config_client != None)

    def test_get_a_value(self):
        self.assertEqual('value0', self.config_client.get('key0'))
        self.assertEqual('value1', self.config_client.get('key1'))

    def test_get_watched_file_list(self):
        files = self.config_client.getWatchFiles()
        self.assertTrue(type(files) in [list, tuple])
        self.assertEqual(files[0]['filepath'], TEST_LOG_FILE0)
        self.assertEqual(files[1]['filepath'], TEST_LOG_FILE1)

    def test_get_processor_config(self):
        conf = self.config_client.getProcessor('syslog0')
        self.assertEqual(conf['host'],'1.1.1.1')