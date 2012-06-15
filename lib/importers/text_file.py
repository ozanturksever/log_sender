import os
import shutil
from tailers.rotatable_file import RotatableFile
import time

__author__ = 'ozanturksever'

class TextFile(RotatableFile):
    def __init__(self, filepath):
        super(TextFile, self).__init__(filepath=filepath, position=0, close_on_EOF=True)
        self.__filepath = filepath

    def close(self):
        super(TextFile, self).close()
        if os.path.exists(self.getFilePath()):
            shutil.move(self.getFilePath(),
                os.path.dirname(self.getFilePath()) + '/processed_' + os.path.basename(self.getFilePath()))
