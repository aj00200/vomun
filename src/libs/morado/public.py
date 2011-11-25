import socket
import json

import sys

def read(socket, size):
    size = int(size)
    datareturn = ""
        
    while len(datareturn) < size:
        try:
            datareturn += socket.recv(1)
        except IOError:
            return datareturn

    return datareturn



class _Method:
    def __init__(self,socket, funcname):
        self.func = funcname
        self.socket = socket

    def __call__(self,func,*args,**kwargs):
        self.req = self._make_request(self.func, *args,**kwargs)
        self.socket.send(self.req)
        length = int(read(self.socket, 4))

        return json.loads(read(self.socket, length))

    def _make_request(self, func, *args, **kwargs):

        request = {}
        request["function"] = func
        request["args"] = args
        request["kwargs"] = kwargs


        js = json.dumps(request)
        print js
        size = len(js)
        req = "%4i%s" % (size, js)
        return req

class VomunAPI:
    def __init__(self,server="127.0.0.1",port=3451):
        self.socket = socket.socket()
        self.socket.connect((server, port))

    def __getattr__(self, name):
        # magic method dispatcher
        return _Method(self.socket, name)

if __name__ == "__main__":
    api = VomunAPI()

    print api.__getattr__(sys.argv[1])(*sys.argv[1:])

    #print api.__getattr__(sys.argv[1])()

    #print api.get_functions()
