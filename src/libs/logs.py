import libs.events
OUTPUT = True


class Logger(libs.events.Handler):
    '''Print events as they happen. TODO: Write to a log file'''
    def got_message(self, message):
        self._output('Got a message')
        self._output('  Message was: %s' % message.message)

    def got_connect(self, connection):
        self._output('Got a connection')

    def info(self,message):
        self._output('[info] %s' % message)

    def _output(self, message):
        if OUTPUT:
            print('[*] %s' % message)

libs.events.register_handler(Logger())