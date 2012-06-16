#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from gevent import socket
from base_processor import BaseProcessor

FACILITY = {
    'kern': 0, 'user': 1, 'mail': 2, 'daemon': 3,
    'auth': 4, 'syslog': 5, 'lpr': 6, 'news': 7,
    'uucp': 8, 'cron': 9, 'authpriv': 10, 'ftp': 11,
    'local0': 16, 'local1': 17, 'local2': 18, 'local3': 19,
    'local4': 20, 'local5': 21, 'local6': 22, 'local7': 23,
    }

LEVEL = {
    'emerg': 0, 'alert':1, 'crit': 2, 'err': 3,
    'warning': 4, 'notice': 5, 'info': 6, 'debug': 7
}

class SyslogProcessor(BaseProcessor):
    def __init__(self, name, conf):
        super(SyslogProcessor, self).__init__(name, conf)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def process(self, msg):
        data = '<%d>%s' % (LEVEL['notice'] + FACILITY['daemon']*8, msg)
        self.__sock.sendto(data, (self._get_syslog_host(), self._get_syslog_port()))
        super(SyslogProcessor, self).process(msg)

    def _get_syslog_host(self):
        return self.config['host']

    def _get_syslog_port(self):
        return self.config['port']