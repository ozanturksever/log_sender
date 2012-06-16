import gevent
from src.reader.rotatable_file_reader import RotatableFileReader
from src.reader.text_file_reader import TextFileReader

SLEEP_TIME = 0.1
START_FROM_END = -1
START_FROM_TOP = 0

class FileWatcher(gevent.Greenlet):
    def __init__(self, file, logQueue):
        self.__file = file

        self.__startposition = START_FROM_END
        if file.get('startposition') == 'top':
            self.__startposition = START_FROM_TOP

        self.__move_on_EOF = False
        if file.get('moveoneof'):
            self.__move_on_EOF = True

        self.__shutdown = False
        self.__logQueue = logQueue
        gevent.Greenlet.__init__(self)


    def get_file(self):
        return self.__file

    def run(self):
        if self.__move_on_EOF:
            self.__fd = TextFileReader(self.__file['filepath'], position=self.__startposition,
                moveinfo=self.__file.get('moveoneof'))
        else:
            self.__fd = RotatableFileReader(self.__file['filepath'], position=self.__startposition)

        while 1:
            if self.__shutdown:
                break
            line = self.__fd.getLine()
            if line == '' or line == '\0':
                gevent.sleep(SLEEP_TIME)
                continue
                #TODO: handle queue full
            self.__logQueue.put((self.__file['processor'], line))

    def shutdown(self):
        self.__shutdown = True