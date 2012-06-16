import unittest
from src.helpers.config.config import Config
from src.manager.processor_manager import ProcessorManager
from src.tests import test_helper
from src.tests.test_helper import CONFIG_FILE

class test_processor_manager(unittest.TestCase):
    def setUp(self):
        test_helper.setUp()
        self.__config_server = Config(CONFIG_FILE)
        self.pm = ProcessorManager()

    def tearDown(self):
        test_helper.tearDown()
        self.__config_server.shutdown()

    def test_can_custruct_processors(self):
        list = self.pm.get_processors()
        self.assertTrue(len(list) > 0)

    def test_get_processor(self):
        p = self.pm.get_processor('syslog0')
        self.assertTrue('syslog0', p.get_name())

        p = self.pm.get_processor('syslog1')
        self.assertTrue('syslog1', p.get_name())
