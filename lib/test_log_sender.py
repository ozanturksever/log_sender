import os
import unittest
import time
from log_sender import log_sender

TEST_LOG_FILE0 = "/tmp/test0.log"
TEST_LOG_FILE1 = "/tmp/test1.log"
#TEST_CONFIG_CONTENT = "[files]\n%s = true\n%s = true\n" % (TEST_LOG_FILE0, TEST_LOG_FILE1)
TEST_CONFIG_CONTENT = '{"files":[{"filepath":"%s"}, {"filepath":"%s"}]}\n' % (TEST_LOG_FILE0, TEST_LOG_FILE1)
CONFIG_FILE = "/tmp/config.json"
END_LINE = "\n"

class test_log_sender(unittest.TestCase):
    def test_can_read_config(self):
        self.log_sender = log_sender(config_file=CONFIG_FILE, shutdown_after=0.1)
        list = self.log_sender.getTailList()
        self.assertTrue(TEST_LOG_FILE0 in list)
        self.assertTrue(TEST_LOG_FILE1 in list)

    def test_can_tail_file(self):
        lines = []
        def process(line):
            lines.append(line)

        self.log_sender = log_sender(processor_callback=process, config_file=CONFIG_FILE, shutdown_after=1)

        self.__insert_one_line(TEST_LOG_FILE0,"test line\n")
        time.sleep(0.1)
        self.__insert_one_line(TEST_LOG_FILE1,"test line2\n")
        self.log_sender.processLogs()
        self.assertEqual(lines[0], "test line")
        self.assertEqual(lines[1], "test line2")

    def setUp(self):
        self.__setup_test_config()
        self.test_files = {}
        for file in [TEST_LOG_FILE0, TEST_LOG_FILE1]:
            self.__open_test_file(file)

    def tearDown(self):
        for file in [TEST_LOG_FILE0, TEST_LOG_FILE1]:
            os.remove(file)
#        os.remove(CONFIG_FILE)

    def __setup_test_config(self):
        config_ini = open(CONFIG_FILE,"w")
        config_ini.write(TEST_CONFIG_CONTENT)
        config_ini.close()

    def __open_test_file(self, file):
        self.test_files[file] = open(file,"w")

    def __prepare_test_directory(self, directory):
        os.mkdir(directory)

    def __insert_one_line(self, file, line):
        self.test_files[file].write(line + END_LINE)
        self.test_files[file].flush()

if __name__ == '__main__':
    unittest.main()
