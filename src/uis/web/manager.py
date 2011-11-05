'''The localhost webserver for creating UIs that can be accessed through an
Internet browser (Firefox prefered).'''
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import libs.threadmanager
import uis.web.handler
import libs.globals
import libs.events


class MyHandler(BaseHTTPRequestHandler):
    '''Handles events from the web server and passes them out as events to
    libs.events via the broadcast function. The event is sent to the
    web_ui_request method of all registered event handlers.'''
    
    def do_GET(self):
        '''Handle GET requests'''
        libs.events.broadcast('web_ui_request', self.path, self)

##    def do_POST(self):
##        '''Handle POST requests'''
##        global rootnode
##        try:
##            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
##            if ctype == 'multipart/form-data':
##                query = cgi.parse_multipart(self.rfile, pdict)
##            self.send_response(301)
##            
##            self.end_headers()
##            upfilecontent = query.get('upfile')
##            print('filecontent', upfilecontent[0])
##            self.wfile.write('<html>POST OK.<br /><br />');
##            self.wfile.write(upfilecontent[0]);
##            
##        except:
##            pass

class Server(libs.threadmanager.Thread):
    '''Contains the webserver within a stopable and registered thread'''
    def run(self):
        '''Contains the server setup and main loop.'''
        self.server = HTTPServer(('', 7777), MyHandler)
        libs.threadmanager.register_socket(self.server.socket)
        print('Webserver running on port 7777 : Started')
        while not self._stop.isSet():
            try:
                self.server.handle_request()
            except KeyboardInterrupt:
                print('^C received, shutting down web server')
                self.server.socket.close()
                self._stop.set()
            
## Start the server and handler            
def start():
    '''Start the user interface. Create the Server object and the listener
    we use to listen for events from this interface.
    '''
    server = Server()
    handler = uis.web.handler.Handler()

    libs.threadmanager.register(server)
    server.start()

    libs.events.register_handler(handler)
