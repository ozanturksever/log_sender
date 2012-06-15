import gevent
from tailers.rotatable_file import RotatableFile

SLEEP_TIME = 0.1

class TailFile(gevent.Greenlet):
    def __init__(self, file, logQueue):
        self.__file = file
        self.__shutdown = False
        self.__logQueue = logQueue
        gevent.Greenlet.__init__(self)

    def run(self):
        self.__rotatable_file = RotatableFile(self.__file)
        while 1:
            if self.__shutdown:
                break
            line = self.__rotatable_file.getLine()
            if line == '' or line == '\0':
                gevent.sleep(SLEEP_TIME)
                continue
            self.__logQueue.put(line)

    def shutdown(self):
        self.__shutdown = True