import asyncore
import asynchat
import socket
import json
import SocketServer
import traceback
import os
import sys

path =  os.getcwd()
sys.path.append(path)

import libs.threadmanager
import libs.globals
import libs.morado.functions

def errorfunc(*args):
    return "Function not found"


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return obj.__str__()
        except:
            return json.JSONEncoder.default(self, obj)


class APIHandler(asynchat.async_chat):
    def __init__(self,sock):
        asynchat.async_chat.__init__(self,sock)
        self.data = 0
        self.buffer = ""
        self.size = -1
        self.set_terminator(4)

    def read(self,size):
        size = int(size)
        datareturn = ""
        
        while len(datareturn) < size:
            try:
                datareturn += self.request.recv(1)
            except IOError:
                pass

        return datareturn
    
    def collect_incoming_data(self, data):        
        self.buffer += data

    def found_terminator(self):
        if self.size == -1:
            self.size = int(self.buffer[0:4])
            self.set_terminator(self.size)
            self.buffer = self.buffer[5:]       #size = int(self.read(4))
        
        else:
            try:
                data =  self.buffer
                retdata = self.handle_api(data)
                retjson = json.dumps(retdata,cls=ComplexEncoder)
                length = len(retjson)
                self.push("%4i%s" % (length,retjson))

                print "api returned", retjson
                self.data = 0
                self.buffer = ""
                self.size = -1
                self.set_terminator(4)
            except Exception as ex:
                print "error", traceback.format_exc()
                self.size = -1



    
    def handle_api(self,data):


        request = json.loads(data)
        function = request["function"]
        args = request["args"]

        try:
            ret =  libs.globals.global_vars["apifunctions"][function](*args)
            if isinstance(ret,dict):
                return ret
            else:
                return {"returnvalue": ret} # if a function doesnt return a dict,
                                            # make a dict

        except Exception as ex:
            print libs.globals.global_vars["apifunctions"]
            ex = traceback.format_exc()
            print ex
            return {"error2": ex}


class APIServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is None:
            pass
        else:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = APIHandler(sock)

#class APIServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
#    pass

"""class APIThread(libs.threadmanager.Thread):
    def __init__(self):
        libs.threadmanager.Thread.__init__(self)
        self.server = APIServer(("0.0.0.0", 9999), APIRequestHandler)
        libs.threadmanager.register_socket(self.server.socket)

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self._stop.set()
        self.server.shutdown()"""

class APIServerThead(libs.threadmanager.Thread):

    def run(self):
        libs.globals.global_vars["apiserver"] = APIServer('localhost', 9999)
        while libs.globals.global_vars["running"]:
            asyncore.loop(timeout = 5, count = 1)

def start():
    '''Start the API interface. Create the Server object and the listener
    we use to listen for events from this interface.
    '''
    """libs.globals.global_vars["apiserver"] = APIServer('localhost', 9999)
    libs.threadmanager.register(libs.globals.global_vars["apiserver"])
    libs.globals.global_vars["apiserver"].start()"""
    #api.functions.register()
    libs.globals.global_vars["APIServerThread"] = APIServerThead()
    libs.threadmanager.register(libs.globals.global_vars["APIServerThread"])
    libs.globals.global_vars["APIServerThread"].start()

if __name__ == "__main__":
    start()
#ip, port = server.server_address

#server.serve_forever()