#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from copy import copy
import glob
import os
from src.helpers.file_watcher import FileWatcher
from src.manager.base_manager import BaseManager
from gevent import spawn, sleep

__author__ = 'Ozan Turksever (ozan.turksever@logsign.net)'
__copyright__ = 'Copyright (c) 2012 Innotim Yazilim Ltd.'
__license__ = 'GPLv2'
__version__ = '0.0.1'

class WatchFileManager(BaseManager):
    def __init__(self, processor_manager, shutdown_after=None):
        super(WatchFileManager, self).__init__(processor_manager, shutdown_after=shutdown_after)
        self.__active_files = []
        self.refresh_files()
        self._add_greenlet(spawn(self.__periodic_refresh))


    def __periodic_refresh(self):
        while not self._shutdown:
            sleep(3)
            self.refresh_files()

    def refresh_files(self):
        self.__watch_files = []
        for file_conf in self._config.get('files'):
            if self._is_glob(file_conf):
                self.add_glob(file_conf)
            else:
                self.add_file(file_conf)
        self.__startWatching()

    def add_glob(self, file_conf):
        for filepath in glob.glob(file_conf['filepath']):
            new_conf = copy(file_conf)
            new_conf['filepath'] = filepath
            new_conf['name'] = filepath
            self.add_file(new_conf)

    def add_file(self, conf):
        files = [f['filepath'] for f in self.__watch_files]
        if os.path.exists(conf['filepath']) and (not conf['filepath'] in files):
            self.__watch_files.append(conf)

    def _is_glob(self, conf):
        exists = os.path.exists(conf['filepath'])
        if exists:
            return False
        return True

    def get_watch_list(self):
        return self.__watch_files

    def get_active_files(self):
        return self.__active_files

    def __startWatching(self):
        for file in self.get_watch_list():
            if file['filepath'] in self.__active_files:
                continue
            watcher = FileWatcher(file, self._logQueue)
            watcher.start()
            self.__active_files.append(file['filepath'])
            self._add_greenlet(watcher)
        self.__refresh_greenlets()

    def __refresh_greenlets(self):
        files = [f['filepath'] for f in self.__watch_files]
        for g in self._get_greenlets():
            if type(g) == FileWatcher:
                if not g.get_file()['filepath'] in files:
                    try:
                        self.__active_files.remove(g.get_file()['filepath'])
                        g.shutdown()
                        g.kill()
                        self._remove_greenlet(g)
                    except Exception, err:
                        print "ERROR:",err
                        pass
