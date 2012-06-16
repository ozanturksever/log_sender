import unittest
import msgpack
from src.helpers.config.config import Config
from gevent_zeromq import zmq
from gevent import spawn
from gevent import sleep
from src.tests.test_helper import TEST_CONFIG_CONTENT, CONFIG_FILE, TEST_LOG_FILE0, TEST_LOG_FILE1

__author__ = 'ozanturksever'

class test_config(unittest.TestCase):
    def setUp(self):
        open("/tmp/config.json", "w").write(TEST_CONFIG_CONTENT)
        self.config = Config(config_file=CONFIG_FILE)

    def tearDown(self):
        self.config.shutdown()

    def test_can_read_config_file(self):
        conf = self.config.getConfig()
        self.assertEqual(type(conf), dict)
        self.assertEqual(type(conf.get('files')), list)

    def test_can_read_config_file_with_default_cfg(self):
        self.config.shutdown()
        conf = Config()
        self.assertEqual(conf.__class__, Config)
        self.assertEqual(type(conf.get('files')), list)
        conf.shutdown()

    def test_get_watched_file_list(self):
        files = self.config.getWatchFiles()
        self.assertEqual(type(files), list)
        self.assertEqual(files[0]['filepath'], TEST_LOG_FILE0)
        self.assertEqual(files[1]['filepath'], TEST_LOG_FILE1)

    def test_can_get_msg_from_socket(self):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://localhost:10001')
        socket.send(msgpack.packb({'func': 'get', 'args': ('files')}))
        files = msgpack.unpackb(socket.recv())
        self.assertEqual(files[0]['filepath'], TEST_LOG_FILE0)
        self.assertEqual(files[1]['filepath'], TEST_LOG_FILE1)

    def test_get_processor_config(self):
        conf = self.config.getProcessor('syslog0')
        self.assertEqual(conf['host'],'1.1.1.1')