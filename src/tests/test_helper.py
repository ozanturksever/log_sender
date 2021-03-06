import glob
import os

__author__ = 'ozanturksever'

CONFIG_FILE = "/tmp/config.json"
TEST_LOG_FILE0 = "/tmp/test0.log"
TEST_LOG_FILE1 = "/tmp/test1.log"
TEST_LOG_FILE2 = "/tmp/test2.log"
TEST_LOG_FILE = "/tmp/test.log"
TEST_FILE_PATH = '/tmp/file.txt'
TEST_FILE_PATH_PROCESSED = '/tmp/processed_file.txt'
TEST_DIR = '/tmp/logs'
TEST_DIR_FILE0 = 'test0.log'

END_LINE = "\n"
LINE_ONE = "first line"
LINE_TWO = "second line"

TEST_CONFIG_CONTENT = """
{
    "key0":"value0",
    "key1":"value1",
    "files": [
        {"name":"testfile0", "filepath": "%s", "processor":"test"},
        {"name":"testfile1", "filepath": "%s", "processor":"test"},
        {"name":"testdir", "filepath": "%s/*.log", "processor":"test"},
        {
            "name":"testfile2",
            "filepath": "%s",
            "startposition": "top",
            "moveoneof": {
                "dstdir":"/tmp/",
                "prefix":"processed_",
                "postfix":".done"
            },
            "processor":"test"
        }
    ],
    "processor": {
        "syslog0": { "type":"syslog", "host":"1.1.1.1", "port": 514},
        "syslog1": { "type":"syslog", "host":"2.2.2.2", "port": 514},
        "test": {"type":"test"}
    }
}
""" % (TEST_LOG_FILE0, TEST_LOG_FILE1, TEST_DIR, TEST_LOG_FILE2)

def setUp():
    config_ini = open(CONFIG_FILE, "w")
    config_ini.write(TEST_CONFIG_CONTENT)
    config_ini.close()
    if not os.path.exists(TEST_DIR):
        os.mkdir(TEST_DIR)


def tearDown():
    for f in [TEST_LOG_FILE, TEST_LOG_FILE0, TEST_LOG_FILE1, TEST_FILE_PATH, TEST_FILE_PATH_PROCESSED, CONFIG_FILE]:
        try:
            os.remove(f)
        except:
            pass
    if os.path.exists(TEST_DIR):
        for f in glob.glob(TEST_DIR + '/*'):
            os.remove(f)
        os.rmdir(TEST_DIR)