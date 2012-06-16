from src.helpers.config.config import Config
from src.processor.syslog_processor import SyslogProcessor
from src.tests.test_helper import CONFIG_FILE

__author__ = 'ozanturksever'

import unittest
from src.tests import test_helper

class test_syslog_processor(unittest.TestCase):
    def setUp(self):
        test_helper.setUp()
        self.__config_server = Config(config_file=CONFIG_FILE)
        conf = self.__config_server.get('processor')['syslog0']
        self.p = SyslogProcessor('syslog0', conf)

    def tearDown(self):
        test_helper.tearDown()
        self.__config_server.shutdown()

    def test_can_process_msg(self):
        self.p.process('test')
        self.assertEqual('test', self.p._get_last_processed_msg())

    def test_get_syslog_server(self):
        self.assertEqual('1.1.1.1',self.p._get_syslog_host())
