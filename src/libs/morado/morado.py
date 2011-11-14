import asyncore
import socket
import json
import SocketServer
import traceback

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


class APIRequestHandler(SocketServer.BaseRequestHandler):
    def read(self,size):
        size = int(size)
        datareturn = ""
        
        while len(datareturn) < size:
            try:
                datareturn += self.request.recv(1)
            except IOError:
                pass

        return datareturn


    def handle(self):
        size = int(self.read(4))
        while True:
            try:
                data =  self.read(size)
                retdata = self.handle_api(data)
                retjson = json.dumps(retdata,cls=ComplexEncoder)
                length = len(retjson)
                self.request.send("%4i%s" % (length,retjson))

                print "api returned", retjson
                size = int(self.read(4))
                print size
            except Exception as ex:
                print "error", traceback.format_exc()



    
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

class APIServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class APIThread(libs.threadmanager.Thread):
    def __init__(self):
        libs.threadmanager.Thread.__init__(self)
        self.server = APIServer(("0.0.0.0", 9999), APIRequestHandler)
        libs.threadmanager.register_socket(self.server.socket)

    def run(self):
        self.server.serve_forever()

    def stop(self):
        self._stop.set()
        self.server.shutdown()

def start():
    '''Start the API interface. Create the Server object and the listener
    we use to listen for events from this interface.
    '''
    libs.globals.global_vars["apiserver"] = APIThread()
    libs.threadmanager.register(libs.globals.global_vars["apiserver"])
    libs.globals.global_vars["apiserver"].start()
    #api.functions.register()

#ip, port = server.server_address

#server.serve_forever()