__author__ = 'ozanturksever'

class BaseProcessor(object):
    def __init__(self, name, conf):
        self.name = name
        self.config = conf
        self.last = None
        self.count = 0

    def get_name(self):
        return self.name

    def process(self, msg):
        self.last = msg
        self.count += 1

    def get_processed_msg_count(self):
        return self.count

    def _get_last_processed_msg(self):
        return self.last
