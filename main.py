import os
import signal
import sys
import gevent
from lib.helpers.config.config import Config
from lib.transport import syslog
from lib.managers.watch_file_manager import WatchFileManager

CONFIG_FILE = 'config.json'

def shutdown(signal, frame):
    log_sender.shutdown(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def processor(line):
    print line
    syslog.udp_send(message=line, host=config['syslog_server'])

if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        print "no configuration found in path."
        print "path: %s" % os.getcwd()
        print "config file: %s" % CONFIG_FILE
        sys.exit(1)

    config = Config()
    try:
        print "Will send logs to: %s" % config.get('syslog_server')
        for file_config in config.getWatchFiles():
            print "tailing file: %s (%s)" % (file_config['name'],file_config['filepath'])
    except Exception, err:
        print "configuration error!"
        print "--------------------"
        print err
        sys.exit(1)
        pass

    log_sender = WatchFileManager(processor_callback=processor)
    while True:
        gevent.sleep(0)
