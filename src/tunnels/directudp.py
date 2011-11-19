import time
import socket
import threading
import libs.threadmanager
import tunnels.base
import libs.events
from libs.packets import make_packet
from libs.construct import *

connections = {}

class Tunnel(tunnels.base):
    '''UDP Tunnel class'''
    def connect(self, node):
        self.connection = Connection(node)
        
    def disconnect(self):
        self.connection.disconnect()
    
class Connection(tunnels.base.Connection):
    '''UDP "connection" to a peer'''
    def __init__(self, node): # TODO switch to a global node class
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((node.ip, node.port))
    
        self.data = ""
        self.packages = {}
        
        
        #handshake is ended in friends.handle_packets
    def send(self, message):
        print('Sending: ' + message)
        self.sock.send(message)
        
    def disconnect(self):
        '''Do nothing, UDP does not need to close any connections.'''
        pass

    
    
class Listener(libs.threadmanager.Thread):
    '''Listen for UDP connections on our port'''
    def __init__(self, port = 1337):
        super(Listener, self).__init__()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', port)) # TODO: bind other addresses
        self.sock.setblocking(False)
        
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
        
    def run(self):
        while not self._stop.isSet():
            try:
                data = self.sock.recvfrom(4096)
                ip = data[1][0]
                friend = libs.friends.get_friend_by_ip(ip)
                friend.connection = self.sock
                friend.data += data[0] # Send data to the Friend object
                print('recv: ' + data[0])
                friend.parse_packets()
                friend.connection = self.sock
            except socket.error as error:
                if error.errno == 11: # No new messages
                    time.sleep(1)   
            except AttributeError as error:
                print('Got a message from an unknown IP address.')
                # TODO: how to handle this - maybe they are using a dynamic IP
                #       address and they really are a friend.
        
        
def start():
    listener = Listener()
    listener.start()
    libs.threadmanager.register(listener)
    
