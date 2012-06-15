import json
import os
import signal
import sys
from lib.transport import syslog
from lib.log_sender import log_sender

CONFIG_FILE = 'config.json'

def shutdown(signal, frame):
    log_sender.shutdown(0)

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
        print "--------------------"
        print err
        sys.exit(1)
        pass

    log_sender = log_sender(processor_callback=processor)
    log_sender.join()
