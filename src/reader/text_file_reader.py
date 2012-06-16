import os
import shutil
from src.reader.rotatable_file_reader import RotatableFileReader

__author__ = 'ozanturksever'

class TextFileReader(RotatableFileReader):
    def __init__(self, filepath):
        super(TextFileReader, self).__init__(filepath=filepath, position=0, close_on_EOF=True)
        self.__filepath = filepath

    def close(self):
        super(TextFileReader, self).close()
        if os.path.exists(self.getFilePath()):
            shutil.move(self.getFilePath(),
                os.path.dirname(self.getFilePath()) + '/processed_' + os.path.basename(self.getFilePath()))
