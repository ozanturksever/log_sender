from tailers.rotatable_file import RotatableFile

__author__ = 'ozanturksever'

class TextFile(RotatableFile):
    def __init__(self, filepath):
        super(TextFile, self).__init__(filepath=filepath, position=0, close_on_EOF=True)
        self.__filepath = filepath

