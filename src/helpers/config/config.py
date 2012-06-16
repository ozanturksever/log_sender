import json
from gevent_zeromq import zmq
from gevent import spawn, sleep
import msgpack

__author__ = 'ozanturksever'

CONFIG_FILE='config.json'

class Config:
    def __init__(self, config_file=CONFIG_FILE):
        self.__config_file = config_file
        self.__loadConfig()
        self.__start_server()

    def __loadConfig(self):
        self.__config =  json.loads(open(self.__config_file).read())

    def getConfig(self):
        return self.__config

    def getWatchFiles(self):
        return self.__config['files']

    def getProcessor(self, name):
        return self.__config['processor'][name]

    def get(self, key):
        return self.__config.get(key)

    def __start_server(self):
        self.__context = zmq.Context()
        self.__socket = self.__context.socket(zmq.REP)
        self.__socket.bind('tcp://127.0.0.1:10001')
        spawn(self.__serve, self.__socket)


    def __serve(self,socket):
        while True:
            if socket.closed:
                sleep(0.1)
                continue
            raw_msg = socket.recv()
            try:
                msg = msgpack.unpackb(raw_msg)
                if msg.has_key('args'):
                    resp = getattr(self, msg['func'])(msg['args'])
                else:
                    resp = getattr(self, msg['func'])()
            except Exception, err:
                resp = ('failed: %s' % err)
                pass
            socket.send(msgpack.packb(resp))

    def shutdown(self):
        self.__socket.close()
        self.__context.term()

    def __del__(self):
        self.shutdown()
