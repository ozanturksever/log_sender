#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#

__author__ = 'Ozan Turksever (ozan.turksever@logsign.net)'
__copyright__ = 'Copyright (c) 2012 Innotim Yazilim Ltd.'
__license__ = 'GPLv2'
__version__ = '0.0.1'

from Queue import Queue
import os
import signal
import sys
from transport import syslog
from tailer.rotatable_file import rotatable_file
import ConfigParser
import threading
import time

CONFIG_INI = 'config.ini'
SLEEP_TIME = 0.1
QUEUE_SIZE = 10000
BLOCK = True
QUEUE_BLOCK_SEC = 1

class log_sender:
    def __init__(self, processor_callback=None, config_file=CONFIG_INI, shutdown_after=None):
        self.__logQueue = Queue(QUEUE_SIZE)
        self.__processor_callback = processor_callback
        self.__config_file = config_file
        self.__watch_files = []
        self.__tailThreads = []
        self.__readConfig()
        self.__startTailingThreads()
        self.__shutdown = False
        if shutdown_after:
            t = threading.Timer(shutdown_after, self.shutdown)
            t.start()

    def processLogs(self):
        while not self.__shutdown:
            try:
                line = self.__logQueue.get(BLOCK, QUEUE_BLOCK_SEC)
                if self.__processor_callback:
                    self.__processor_callback(line)
            except Exception, err:
                pass

    def shutdown(self):
        for thread in self.__tailThreads:
            thread.shutdown()
        self.__shutdown = True

    def getTailList(self):
        return self.__watch_files

    def __startTailingThreads(self):
        for file in self.__watch_files:
            tailThread = TailThread(file, self.__logQueue)
            tailThread.start()
            self.__tailThreads.append(tailThread)

    def __readConfig(self):
        config = ConfigParser.RawConfigParser()
        config.read(self.__config_file)
        for (file,status) in config.items("files"):
            self.__watch_files.append(file)


class TailThread(threading.Thread):
    def __init__(self, file, logQueue):
        self.__file = file
        self.__shutdown = False
        self.__logQueue = logQueue
        threading.Thread.__init__(self)

    def run(self):
        self.__rotatable_file = rotatable_file(self.__file)
        while 1:
            if self.__shutdown:
                break
            line = self.__rotatable_file.getLine()
            if line == '':
                time.sleep(SLEEP_TIME)
                continue
            self.__logQueue.put(line)

    def shutdown(self):
        self.__shutdown = True

def shutdown(signal, frame):
    print "shutting down"
    log_sender.shutdown()

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def processor(line):
    syslog.udp_send(message=line, host=syslog_server)

if __name__ == '__main__':
    if not os.path.exists(CONFIG_INI):
        print "no configuration found in path."
        print "path: %s" % os.getcwd()
        print "config file: %s" % CONFIG_INI
        sys.exit(1)
    try:
        config = ConfigParser.RawConfigParser()
        config.read(CONFIG_INI)
        syslog_server = config.get('main','syslog_server')
        print "Will send logs to: %s" % syslog_server
        for (file, status) in config.items("files"):
            print "tailing file: %s" % file
    except Exception, err:
        print "configuration error!"
        print err
        sys.exit(1)
        pass

    log_sender = log_sender(processor_callback=processor)
    log_sender.processLogs()
