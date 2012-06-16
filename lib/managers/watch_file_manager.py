#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from lib.helpers.file_watcher import FileWatcher
from lib.helpers.config.config_client import ConfigClient

__author__ = 'Ozan Turksever (ozan.turksever@logsign.net)'
__copyright__ = 'Copyright (c) 2012 Innotim Yazilim Ltd.'
__license__ = 'GPLv2'
__version__ = '0.0.1'

from gevent.queue import Queue
import gevent

QUEUE_SIZE = 10000

class WatchFileManager:
    def __init__(self, processor_callback=None, shutdown_after=None):
        self.__logQueue = Queue(QUEUE_SIZE)
        self.__processor_callback = processor_callback
        config = ConfigClient()
        self.__watch_files = [f['filepath'] for f in config.getWatchFiles()]
        self.__watchGreenlets = []
        self.__greenlets = []
        self.__startWatching()
        self.__shutdown = False

        self._addGreenlet(gevent.spawn(self.__processLogs, callback=self.__processor_callback))
        if shutdown_after:
            self.__greenlets.append(gevent.spawn(self.shutdown, shutdown_after))

    def __processLogs(self, callback):
        while not self.__shutdown:
            try:
                line = self.__logQueue.get(True, 1)
                if callback:
                    callback(line)
            except Exception, err:
                pass
            gevent.sleep(0)

    def _addGreenlet(self, greenlet):
        self.__greenlets.append(greenlet)

    def shutdown(self, when):
        print "Will shutdown after %d secs" % when
        gevent.sleep(when)
        self.__shutdown = True
        for thread in self.__watchGreenlets:
            thread.shutdown()

        for thread in self.__greenlets:
            thread.kill()
        print "shutdown complete"

    def getWatchList(self):
        return self.__watch_files

    def __startWatching(self):
        for file in self.__watch_files:
            watcher = FileWatcher(file, self.__logQueue)
            watcher.start()
            self._addGreenlet(watcher)
            self.__watchGreenlets.append(watcher)
