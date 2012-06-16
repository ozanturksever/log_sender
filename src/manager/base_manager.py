from gevent import spawn
from gevent import sleep
from gevent.queue import Queue
from src.helpers.config.config_client import ConfigClient

__author__ = 'ozanturksever'
QUEUE_SIZE = 10000

class BaseManager(object):
    def __init__(self, processor_manager, shutdown_after=None):
        self._shutdown = False
        self._logQueue = Queue(QUEUE_SIZE)
        self.__greenlets = []
        self._config = ConfigClient()
        self.processor_manager = processor_manager
        if shutdown_after:
            self._add_greenlet(spawn(self.shutdown, shutdown_after))

        self._add_greenlet(spawn(self.__processLogs))

    def __processLogs(self):
        while not self._shutdown:
            try:
                (processor_name, line) = self._logQueue.get(True, 1)
                processor = self.processor_manager.get_processor(processor_name)
                if processor:
                    processor.process(line)
            except Exception, err:
                sleep(0.1)
                pass
            sleep(0)

    def _add_greenlet(self, greenlet):
        self.__greenlets.append(greenlet)

    def _get_greenlets(self):
        return self.__greenlets

    def _remove_greenlet(self, greenlet):
        return self.__greenlets.remove(greenlet)

    def get_processed_msg_count(self):
        count = 0
        for p in self.processor_manager.get_processors():
            count += p.get_processed_msg_count()
        return count

    def shutdown(self, when):
        sleep(when)
        self._shutdown = True
        for g in self.__greenlets:
            if 'shutdown' in dir(g):
                g.shutdown()
            g.kill()
