import os

import pprint
import unittest
import gevent
from src.helpers.config.config import Config
from src.manager.processor_manager import ProcessorManager
from src.manager.watch_file_manager import WatchFileManager
from src.tests import test_helper
from src.tests.test_helper import TEST_LOG_FILE0, TEST_LOG_FILE1, CONFIG_FILE, TEST_CONFIG_CONTENT, END_LINE, TEST_DIR, TEST_DIR_FILE0, TEST_LOG_FILE2

class test_watch_file_manager(unittest.TestCase):
    def test_can_read_config(self):
        self.manager = WatchFileManager(ProcessorManager(), shutdown_after=0.1)
        list = self.manager.get_watch_list()
        files = [f['filepath'] for f in list]
        self.assertTrue(TEST_LOG_FILE0 in files)
        self.assertTrue(TEST_LOG_FILE1 in files)

    def test_can_tail_file(self):
        self.manager = WatchFileManager(ProcessorManager(),shutdown_after=1)
        self.manager._add_greenlet(gevent.spawn(self.__insert_lines))
        gevent.sleep(0.9)
        count = self.manager.get_processed_msg_count()
        self.assertEqual(count, 2)

    def test_can_tail_file_in_dir(self):
        self.manager = WatchFileManager(ProcessorManager(),shutdown_after=1)
        self.manager._add_greenlet(gevent.spawn(self.__insert_lines_to_dirfile))
        gevent.sleep(1)
        count = self.manager.get_processed_msg_count()
        self.assertEqual(count, 1)

    def test_can_tail_new_file_in_dir(self):
        self.manager = WatchFileManager(ProcessorManager(),shutdown_after=1)
        self.__open_test_file(TEST_DIR+'/test_new.log')
        gevent.sleep(0.1)
        self.manager.refresh_files()
        self.manager._add_greenlet(gevent.spawn(self.__insert_one_line, TEST_DIR+'/test_new.log', 'test'))
        gevent.sleep(0.5)
        count = self.manager.get_processed_msg_count()
        self.assertEqual(count, 1)

    def test_can_close_after_deleted_file(self):
        self.__open_test_file(TEST_DIR+'/test.log')
        self.manager = WatchFileManager(ProcessorManager(),shutdown_after=1)
        os.remove(TEST_DIR+'/test.log')
        self.manager.refresh_files()
        files = [f['filepath'] for f in self.manager.get_watch_list()]
        self.assertTrue(TEST_DIR+'/test.log' not in files)
        files = self.manager.get_active_files()
        self.assertTrue(TEST_DIR+'/test.log' not in files)

    def test_can_tail_from_top(self):
        self.__insert_one_line(TEST_LOG_FILE2, "first line\n")
        self.__insert_one_line(TEST_LOG_FILE2, "second line\n")
        self.manager = WatchFileManager(ProcessorManager(),shutdown_after=1)
        gevent.sleep(0.9)
        count = self.manager.get_processed_msg_count()
        self.assertEqual(count, 2)

    def test_move_on_eof(self):
        self.__insert_one_line(TEST_LOG_FILE2, "first line\n")
        self.manager = WatchFileManager(ProcessorManager(),shutdown_after=1)
        gevent.sleep(0.9)
        dst = "/tmp/processed_%s.done" % os.path.basename(TEST_LOG_FILE2)
        self.assertTrue(os.path.exists(dst))

    def __insert_lines(self):
        self.__insert_one_line(TEST_LOG_FILE0, "test line\n")
        gevent.sleep(0.1)
        self.__insert_one_line(TEST_LOG_FILE1, "test line2\n")

    def __insert_lines_to_dirfile(self):
        self.__insert_one_line(TEST_DIR+'/'+TEST_DIR_FILE0, "test line\n")

    def setUp(self):
        test_helper.setUp()
        self.__config_server = Config(config_file=CONFIG_FILE)
        self.test_files = {}
        for file in [TEST_LOG_FILE0, TEST_LOG_FILE1, TEST_LOG_FILE2]:
            self.__open_test_file(file)

        for file in [TEST_DIR+'/'+TEST_DIR_FILE0]:
            self.__open_test_file(file)

    def tearDown(self):
        test_helper.tearDown()
        self.__config_server.shutdown()

    def __open_test_file(self, file):
        self.test_files[file] = open(file, "w")

    def __prepare_test_directory(self, directory):
        os.mkdir(directory)

    def __insert_one_line(self, file, line):
        self.test_files[file].write(line + END_LINE)
        self.test_files[file].flush()

if __name__ == '__main__':
    unittest.main()
