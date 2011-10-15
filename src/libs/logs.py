import libs.events
OUTPUT = True

import libs.globals


class Logger(libs.events.Handler):
    '''Print events as they happen. TODO: Write to a log file'''
    def got_message(self, message):
        self._output('Got a message')
        self._output('  Message was: %s' % message.msg)

    def got_connect(self, connection):
        self._output('Got a connection')

    def info(self,message):
        self._output('[info] %s' % message)

    def _output(self, message):
        if OUTPUT:
            print('[*] %s' % message)

libs.globals.global_vars['logger'] = Logger()
libs.events.register_handler(libs.globals.global_vars['logger'])