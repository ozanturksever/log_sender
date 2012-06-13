#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
START_FROM_END = -1

__author__ = 'Ozan Turksever (ozan.turksever@logsign.net)'
__copyright__ = 'Copyright (c) 2012 Innotim Yazilim Ltd.'
__license__ = 'GPLv2'
__version__ = '0.0.1'

import os

DEFAULT_SEEK_OFFSET = 0
SEEK_FROM_END = 2

class RotatableFile(object):
    def __init__(self, filepath, position=START_FROM_END, close_on_EOF = False):
        self.__filepath = filepath
        self.__file = None
        self.__opened = False
        self.__start_position = position
        self.__seekedOnce = False
        self.__close_on_EOF = close_on_EOF

    def getLine(self):
        if not self.__tryOpen():
            return '\0'
        if self.__isRotated():
            self.__reOpen()
        try:
            line = self.__file.readline()
            if line:
                return line.strip()
            if self.__close_on_EOF:
                self.close()
            return '\0'
        except Exception:
            return '\0'

    def getFilePath(self):
        return self.__filepath

    def open(self):
        return self.__tryOpen()

    def close(self):
        self.__file.close()
        self.__opened = False

    def isOpen(self):
        return self.__opened

    def __tryOpen(self):
        if self.__opened and self.__file:
            return True
        if self.__open():
            if self.__start_position == START_FROM_END:
                self.__seekToEnd()
            elif self.__start_position > -1:
                self.__seekOnce(self.__start_position)
            self.initial_stat = os.stat(self.__filepath)
            return True
        return False

    def __isRotated(self):
        try:
            stat = os.stat(self.__filepath)
            rotated = stat.st_ino != self.initial_stat.st_ino
            return rotated
        except Exception:
            return True
            pass

    def __open(self):
        try:
            self.__file = open(self.__filepath, "r")
            self.__opened = True
            return True
        except Exception:
            self.__opened = False
            return False
            pass

    def __seekToEnd(self):
        self.__file.seek(DEFAULT_SEEK_OFFSET, SEEK_FROM_END)

    def __seekOnce(self, position):
        if not self.__seekedOnce:
            self.__file.seek(position)
            self.__seekedOnce = True

    def __reOpen(self):
        self.close()
        self.__open()


    def __del__(self):
        if self.__file:
            self.close()

    def __str__(self):
        return "<rotatable_file instance file=%s>" % self.__filepath
