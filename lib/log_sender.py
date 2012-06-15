#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import json
from tail_file import TailFile

__author__ = 'Ozan Turksever (ozan.turksever@logsign.net)'
__copyright__ = 'Copyright (c) 2012 Innotim Yazilim Ltd.'
__license__ = 'GPLv2'
__version__ = '0.0.1'

from gevent.queue import Queue
import gevent

QUEUE_SIZE = 10000
CONFIG_FILE = 'config.json'

class log_sender:
    def __init__(self, processor_callback=None, config_file=CONFIG_FILE, shutdown_after=None):
        self.__logQueue = Queue(QUEUE_SIZE)
        self.__processor_callback = processor_callback
        self.__config_file = config_file
        self.__watch_files = []
        self.__tailGreenlets = []
        self.__greenlets = []
        self.__readConfig()
        self.__startTailingThreads()
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

    def join(self):
        gevent.joinall(self.__greenlets)

    def _addGreenlet(self, greenlet):
        self.__greenlets.append(greenlet)

    def shutdown(self, when):
        print "Will shutdown after %d secs" % when
        gevent.sleep(when)
        self.__shutdown = True
        for thread in self.__tailGreenlets:
            thread.shutdown()

        for thread in self.__greenlets:
            thread.kill()
        print "shutdown complete"

    def getTailList(self):
        return self.__watch_files

    def __startTailingThreads(self):
        for file in self.__watch_files:
            tailGreenlet = TailFile(file, self.__logQueue)
            tailGreenlet.start()
            self._addGreenlet(tailGreenlet)
            self.__tailGreenlets.append(tailGreenlet)

    def __readConfig(self):
        config = json.loads(open(self.__config_file).read())
        for file_config in config['files']:
            self.__watch_files.append(file_config['filepath'])

