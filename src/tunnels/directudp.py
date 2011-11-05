import time
import socket
import threading
import libs.threadmanager
import tunnels.base
import libs.events
from libs.packets import make_packet
from libs.construct import *
connections = {}

    
class Connection(tunnels.base.Connection):
    '''UDP "connection" to a peer'''
    def __init__(self, node): # TODO switch to a global node class
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect((node.ip, node.port))
    
        self.data = ""
        self.packages = {}
        
        self.beginHandshake()
        #self.send('{"type":"connect_request"}')
        
    def beginHandshake(self):
        connectionRequest = libs.packets.packets[0]
        ip = "192.168.1.104"
        key="5416435343454"
        # encryptionmethod = "aes"
        packet = make_packet("ConnectionRequest", encryptionmethod="rsa",ip=ip,
                           iplength = len(ip), key = key, keylength = len(key))
        self.send(packet)
        
        #handshake is ended in friends.handle_packets
    def send(self, message):
        print('Sending: ' + message)
        self.sock.send(message)

    
    
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
            except socket.error, error:
                if error.errno == 11: # No new messages
                    time.sleep(1)       
        
        
def start():
    listener = Listener()
    listener.start()
    libs.threadmanager.register(listener)
    
