import os
import unittest
import time
from text_file import TextFile

TEST_FILE_PATH = '/tmp/file.txt'
TEST_FILE_PATH_PROCESSED = '/tmp/processed_file.txt'

class test_text_file(unittest.TestCase):
    def test_can_read_file(self):
        content = self.__get_file_content()
        self.assertEqual('line 1line 2line 3', content)

    def test_close_fd_after_eof(self):
        self.__get_file_content()
        self.assertFalse(self.text_file.isOpen())

    def test_rotate_after_eof(self):
        self.__get_file_content()
        self.assertFalse(os.path.exists(TEST_FILE_PATH))
        self.assertTrue(os.path.exists(TEST_FILE_PATH_PROCESSED))

    def setUp(self):
        self.text_file = TextFile(filepath=TEST_FILE_PATH)
        f = open(TEST_FILE_PATH,"w")
        f.write("line 1\nline 2\n\nline 3\n")
        f.close()

    def __get_file_content(self):
        content = ''
        while 1:
            line = self.text_file.getLine()
            if line == '\0':
                break
            content += line
        return content
