from copy import copy
import os
import shutil
from src.reader.rotatable_file_reader import RotatableFileReader

__author__ = 'ozanturksever'

class TextFileReader(RotatableFileReader):
    def __init__(self, filepath, position = 0, moveinfo = None):
        self.__moveinfo = moveinfo
        super(TextFileReader, self).__init__(filepath=filepath, position=position, close_on_EOF=True)
        self.__filepath = filepath

    def close(self):
        super(TextFileReader, self).close()
        if self.__moveinfo:
            self._move()

    def _move(self):
        name = os.path.basename(self.getFilePath())
        new_name = copy(name)

        if self.__moveinfo.get('prefix'):
            new_name = ''.join([self.__moveinfo.get('prefix'),new_name])

        if self.__moveinfo.get('postfix'):
            new_name = ''.join([new_name, self.__moveinfo.get('postfix')])

        dstdir = os.path.dirname(self.getFilePath())
        if self.__moveinfo.get('dstdir'):
            dstdir = self.__moveinfo.get('dstdir')

        if os.path.exists(self.getFilePath()):
            shutil.move(self.getFilePath(),
                dstdir + '/' + new_name)
