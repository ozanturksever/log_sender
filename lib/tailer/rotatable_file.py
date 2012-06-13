#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#

__author__ = 'Ozan Turksever (ozan.turksever@logsign.net)'
__copyright__ = 'Copyright (c) 2012 Innotim Yazilim Ltd.'
__license__ = 'GPLv2'
__version__ = '0.0.1'

import os

DEFAULT_SEEK_OFFSET = 0
SEEK_FROM_END = 2

class RotatableFile:
    def __init__(self, filename):
        self.filename = filename
        self.file = None
        self.__opened = False

    def getLine(self):
        if not self.__tryOpen():
            return ""
        if self.__isRotated():
            self.__reOpen()
        try:
            line = self.file.readline()
            return line.strip()
        except Exception:
            return ""

    def getFileName(self):
        return self.filename

    def open(self):
        return self.__tryOpen()

    def __tryOpen(self):
        if self.__opened and self.file:
            return True
        if self.__open():
            self.__seekToEnd()
            self.initial_stat = os.stat(self.filename)
            return True
        return False

    def __isRotated(self):
        try:
            stat = os.stat(self.filename)
            rotated = stat.st_ino != self.initial_stat.st_ino
            return rotated
        except Exception:
            return True
            pass

    def __open(self):
        try:
            self.file = open(self.filename, "r")
            self.__opened = True
            return True
        except Exception:
            self.__opened = False
            return False
            pass

    def __seekToEnd(self):
        self.file.seek(DEFAULT_SEEK_OFFSET, SEEK_FROM_END)

    def __reOpen(self):
        self.__close()
        self.__open()

    def __close(self):
        self.file.close()
        self.__opened = False

    def __del__(self):
        if self.file:
            self.__close()

    def __str__(self):
        return "<rotatable_file instance file=%s>" % self.filename
