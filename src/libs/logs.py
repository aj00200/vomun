import sys
import libs.events
OUTPUT = True
LEVEL = 1

if '-v' in sys.argv:
    LEVEL = 0

class Logger(libs.events.Handler):
    '''Print events as they happen. TODO: Write to a log file'''
    def got_message(self, message):
        self._output('Got a message')
        self._output('  Message was: %s' % message.message)

    def got_connect(self, connection):
        self._output('Got a connection')

    def got_shutdown(self):
        self._output('Got shutdown request.')

    def logthis(self, message, level = 0):
        if level >= LEVEL:
            self._output(message, bullet = 'info')

    def _output(self, message, bullet = '*'):
        '''Print text if the OUTPUT variable is set to True.'''
        if OUTPUT:
            print('[%s] %s' % (bullet, message))

libs.events.register_handler(Logger())