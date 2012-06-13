#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import json

__author__ = 'Ozan Turksever (ozan.turksever@logsign.net)'
__copyright__ = 'Copyright (c) 2012 Innotim Yazilim Ltd.'
__license__ = 'GPLv2'
__version__ = '0.0.1'

from Queue import Queue
import os
import signal
import sys
from transport import syslog
from tailer.rotatable_file import RotatableFile
import threading
import time

CONFIG_FILE = 'config.json'
SLEEP_TIME = 0.1
QUEUE_SIZE = 10000
BLOCK = True
QUEUE_BLOCK_SEC = 1

class log_sender:
    def __init__(self, processor_callback=None, config_file=CONFIG_FILE, shutdown_after=None):
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
        config = json.loads(open(self.__config_file).read())
        for file_config in config['files']:
            self.__watch_files.append(file_config['filepath'])

class TailThread(threading.Thread):
    def __init__(self, file, logQueue):
        self.__file = file
        self.__shutdown = False
        self.__logQueue = logQueue
        threading.Thread.__init__(self)

    def run(self):
        self.__rotatable_file = RotatableFile(self.__file)
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
    log_sender.processLogs()
