import gevent
from src.reader.rotatable_file_reader import RotatableFileReader

SLEEP_TIME = 0.1

class FileWatcher(gevent.Greenlet):
    def __init__(self, file, logQueue):
        self.__file = file
        self.__shutdown = False
        self.__logQueue = logQueue
        gevent.Greenlet.__init__(self)


    def get_file(self):
        return self.__file

    def run(self):
        self.__rotatable_file = RotatableFileReader(self.__file['filepath'])
        while 1:
            if self.__shutdown:
                break
            line = self.__rotatable_file.getLine()
            if line == '' or line == '\0':
                gevent.sleep(SLEEP_TIME)
                continue
            #TODO: handle queue full
            self.__logQueue.put((self.__file['processor'],line))

    def shutdown(self):
        self.__shutdown = True