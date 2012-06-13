#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import json

__author__ = 'Ozan Turksever (ozan.turksever@logsign.net)'
__copyright__ = 'Copyright (c) 2012 Innotim Yazilim Ltd.'
__license__ = 'GPLv2'
__version__ = '0.0.1'

from gevent.queue import Queue
import os
import signal
import sys
from transport import syslog
from tailers.rotatable_file import RotatableFile
import gevent

CONFIG_FILE = 'config.json'
SLEEP_TIME = 0.1
QUEUE_SIZE = 10000

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

    def join(self):
        gevent.joinall(self.__greenlets)

    def _addGreenlet(self, greenlet):
        self.__greenlets.append(greenlet)

    def __processLogs(self, callback):
        while not self.__shutdown:
            try:
                line = self.__logQueue.get(True, 1)
                if callback:
                    callback(line)
            except Exception, err:
                pass
            gevent.sleep(0)

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
            tailGreenlet = TailGreenlet(file, self.__logQueue)
            tailGreenlet.start()
            self._addGreenlet(tailGreenlet)
            self.__tailGreenlets.append(tailGreenlet)

    def __readConfig(self):
        config = json.loads(open(self.__config_file).read())
        for file_config in config['files']:
            self.__watch_files.append(file_config['filepath'])

class TailGreenlet(gevent.Greenlet):
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

def shutdown(signal, frame):
    log_sender.shutdown()

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def processor(line):
    syslog.udp_send(message=line, host=config['syslog_server'])

if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        print "no configuration found in path."
        print "path: %s" % os.getcwd()
        print "config file: %s" % CONFIG_FILE
        sys.exit(1)
    try:
        config = json.loads(open(CONFIG_FILE).read())
        print "Will send logs to: %s" % config['syslog_server']
        for file_config in config['files']:
            print "tailing file: %s (%s)" % (file_config['name'],file_config['filepath'])
    except Exception, err:
        print "configuration error!"
        print err
        sys.exit(1)
        pass

    log_sender = log_sender(processor_callback=processor)
    log_sender.join()
