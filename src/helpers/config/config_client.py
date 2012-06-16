import msgpack

__author__ = 'ozanturksever'
from gevent_zeromq import zmq
from gevent import spawn

class ConfigClient(object):
    def __init__(self):
        self.__context = zmq.Context()
        self.__socket = self.__context.socket(zmq.REQ)
        self.__socket.connect('tcp://localhost:10001')

    def get(self, key):
        return self.__send_recv({'func':'get', 'args': (key)})

    def getWatchFiles(self):
        return self.__send_recv({'func':'getWatchFiles'})

    def getProcessor(self, name):
        return self.__send_recv({'func':'getProcessor', 'args':(name)})

    def __send_recv(self, rawmsg):
        msg = msgpack.packb(rawmsg)
        self.__socket.send(msg)
        resp = self.__socket.recv()
        return msgpack.unpackb(resp)

    def shutdown(self):
        self.__socket.close()
        self.__context.term()

    def __del__(self):
        self.shutdown()