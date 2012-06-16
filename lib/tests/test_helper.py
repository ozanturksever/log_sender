import os

__author__ = 'ozanturksever'
TEST_LOG_FILE0 = "/tmp/test0.log"
TEST_LOG_FILE1 = "/tmp/test1.log"
TEST_CONFIG_CONTENT = '{"key0":"value0", "key1":"value1","files":[{"filepath":"%s"}, {"filepath":"%s"}]}\n' % (
TEST_LOG_FILE0, TEST_LOG_FILE1)
CONFIG_FILE = "/tmp/config.json"
END_LINE = "\n"
LINE_ONE = "first line"
LINE_TWO = "second line"
TEST_LOG_FILE = "/tmp/test.log"
TEST_FILE_PATH = '/tmp/file.txt'
TEST_FILE_PATH_PROCESSED = '/tmp/processed_file.txt'

def setUp():
    config_ini = open(CONFIG_FILE,"w")
    config_ini.write(TEST_CONFIG_CONTENT)
    config_ini.close()

def tearDown():
    for f in [TEST_LOG_FILE, TEST_LOG_FILE0, TEST_LOG_FILE1, TEST_FILE_PATH, TEST_FILE_PATH_PROCESSED, CONFIG_FILE]:
        try:
            os.remove(f)
        except:
            pass