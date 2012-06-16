import os
import unittest
import gevent
from lib.log_sender import log_sender
from lib.helpers.config.config import Config
from lib.tests import test_helper
from lib.tests.test_helper import TEST_LOG_FILE0, TEST_LOG_FILE1, CONFIG_FILE, TEST_CONFIG_CONTENT, END_LINE

class test_log_sender(unittest.TestCase):
    def test_can_read_config(self):
        self.log_sender = log_sender(shutdown_after=0.1)
        list = self.log_sender.getWatchList()
        self.assertTrue(TEST_LOG_FILE0 in list)
        self.assertTrue(TEST_LOG_FILE1 in list)

    def test_can_tail_file(self):
        lines = []
        def process(line):
            lines.append(line)

        self.log_sender = log_sender(processor_callback=process, shutdown_after=1)
        self.log_sender._addGreenlet(gevent.spawn(self.__insert_lines))
        gevent.sleep(0.5)
        self.assertTrue("test line" in lines)
        self.assertTrue("test line2" in lines)

    def __insert_lines(self):
        self.__insert_one_line(TEST_LOG_FILE0,"test line\n")
        gevent.sleep(0.1)
        self.__insert_one_line(TEST_LOG_FILE1,"test line2\n")

    def setUp(self):
        test_helper.setUp()
        self.__config_server = Config(config_file=CONFIG_FILE)
        self.test_files = {}
        for file in [TEST_LOG_FILE0, TEST_LOG_FILE1]:
            self.__open_test_file(file)

    def tearDown(self):
        test_helper.tearDown()
        self.__config_server.shutdown()

    def __open_test_file(self, file):
        self.test_files[file] = open(file,"w")

    def __prepare_test_directory(self, directory):
        os.mkdir(directory)

    def __insert_one_line(self, file, line):
        self.test_files[file].write(line + END_LINE)
        self.test_files[file].flush()

if __name__ == '__main__':
    unittest.main()
