#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#

LINE_ONE = "first line"
LINE_TWO = "second line"
END_LINE = "\n"
TEST_LOG_FILE = "/tmp/test.log"

import unittest
import os
from rotatable_file import RotatableFile

class test_rotatable_file(unittest.TestCase):
    def test_can_pass_filename(self):
        self.assertEqual(TEST_LOG_FILE, self.rotatable_file.getFilePath())

    def test_can_tail_one_line(self):
        self.__insert_one_line(LINE_ONE)
        line = self.rotatable_file.getLine()
        self.assertEqual(LINE_ONE, line)

    def test_can_tail_two_lines(self):
        self.__insert_one_line(LINE_ONE)
        line_one = self.rotatable_file.getLine()
        self.assertEqual(LINE_ONE, line_one)

        self.__insert_one_line(LINE_TWO)
        line_two = self.rotatable_file.getLine()
        self.assertEqual(LINE_TWO, line_two)

    def test_can_tail_when_rotate(self):
        self.__insert_one_line(LINE_ONE)
        line_one = self.rotatable_file.getLine()
        self.assertEqual(LINE_ONE, line_one)

        self.__rotate_test_file()

        self.__insert_one_line(LINE_TWO)
        line_two = self.rotatable_file.getLine()
        self.assertEqual(LINE_TWO, line_two)

    def test_is_starts_from_bottom(self):
        self.__insert_one_line(LINE_ONE)
        self.__construct_rotatable_file()
        self.__insert_one_line(LINE_TWO)
        line = self.rotatable_file.getLine()
        self.assertEqual(LINE_TWO, line)

    def test_read_from_0_position(self):
        self.__insert_one_line(LINE_ONE)
        self.__insert_one_line(LINE_TWO)
        self.__construct_rotatable_file(position=0)
        line_one = self.rotatable_file.getLine()
        second_line = self.rotatable_file.getLine()
        self.assertEqual(line_one, LINE_ONE)
        self.assertEqual(second_line, LINE_TWO)

    def setUp(self):
        self.__open_test_file()
        self.__construct_rotatable_file()

    def __construct_rotatable_file(self, position = -1 ):
        self.rotatable_file = RotatableFile(filepath = TEST_LOG_FILE, position=position)
        self.rotatable_file.open()

    def __insert_one_line(self, line):
        self.test_file.write(line + END_LINE)
        self.test_file.flush()

    def __rotate_test_file(self):
        self.test_file.close()
        os.remove(TEST_LOG_FILE)
        self.__open_test_file()

    def __open_test_file(self):
        self.test_file = open(TEST_LOG_FILE,"w")


if __name__ == '__main__':
    unittest.main()
