import unittest
import time
from log_sender import log_sender

TEST_LOG_FILE0 = "/tmp/test0.log"
TEST_LOG_FILE1 = "/tmp/test1.log"
TEST_CONFIG_CONTENT = "[files]\n%s = true\n%s = true\n" % (TEST_LOG_FILE0, TEST_LOG_FILE1)
CONFIG_FILE = "/tmp/config.ini"
END_LINE = "\n"

class test_log_sender(unittest.TestCase):
    def setUp(self):
        self.__setup_test_config()
        self.test_files = {}
        for file in [TEST_LOG_FILE0, TEST_LOG_FILE1]:
            self.__open_test_file(file)

    def __setup_test_config(self):
        config_ini = open(CONFIG_FILE,"w")
        config_ini.write(TEST_CONFIG_CONTENT)
        config_ini.close()

    def __open_test_file(self, file):
        self.test_files[file] = open(file,"w")

    def __insert_one_line(self, file, line):
        self.test_files[file].write(line + END_LINE)
        self.test_files[file].flush()

    def test_can_read_config(self):
        self.log_sender = log_sender(config_file=CONFIG_FILE, shutdown_after=0.1)
        list = self.log_sender.getTailList()
        self.assertEqual(list[0], TEST_LOG_FILE0)
        self.assertEqual(list[1], TEST_LOG_FILE1)

    def test_can_tail_file(self):
        lines = []
        def process(line):
            lines.append(line)

        self.log_sender = log_sender(processor_callback=process, config_file=CONFIG_FILE, shutdown_after=1)

        self.__insert_one_line(TEST_LOG_FILE0,"test line\n")
        time.sleep(0.5)
        self.__insert_one_line(TEST_LOG_FILE1,"test line2\n")
        self.log_sender.processLogs()
        self.assertEqual(lines[0], "test line")
        self.assertEqual(lines[1], "test line2")

if __name__ == '__main__':
    unittest.main()
