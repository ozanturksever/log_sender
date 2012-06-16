import os
import signal
import sys
import gevent
from src.helpers.config.config import Config
from src.manager.processor_manager import ProcessorManager
from src.manager.watch_file_manager import WatchFileManager

CONFIG_FILE = 'config.json'

def shutdown(signal, frame):
    watchFileManager.shutdown(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def getProcessor():
    output = config.get('processor')
    if output == 'syslog':
        return processor_syslog

if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        print "no configuration found in path."
        print "path: %s" % os.getcwd()
        print "config file: %s" % CONFIG_FILE
        sys.exit(1)

    config = Config()
    try:
        print "start"
    except Exception, err:
        print "configuration error!"
        print "--------------------"
        print err
        sys.exit(1)
        pass

    watchFileManager = WatchFileManager(ProcessorManager())
    while True:
        gevent.sleep(120)
