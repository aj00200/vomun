#! /usr/bin/env python
'''Start the program. Load segments of the program that need to be started and
run them.'''
import time

import libs

print(libs.globals['anon+']['banner'] %
        (libs.globals['anon+']['VERSION'],
        libs.globals['anon+']['BUILD']))

import libs.threadmanager
import libs.browser
import libs.events
import libs.logs

print('''
     == Warning! ==
This is an insecure beta!
This software has various
known weaknesses. Please,
do not depend on it to be
secure! Thank you, ~~Devs
''')

## Startup
if __name__ == '__main__':
    # Create the API Server. Used by external Applications.
    #import api.server
    #api.server.start()

    import libs.morado.morado
    libs.morado.morado.start()

    # Create the console. Later to be replaced with an extenal app
    #from libs.console import console
    #consoleO = console()
    #libs.threadmanager.register(consoleO)
    #consoleO.start()

    # Load and prepare our list of friends
    import libs.friends as friends
    friends.load_friends()

    # Load connection handlers and start
    import tunnels.directudp
    tunnels.directudp.start()

    # Start the web interface
    import uis.web.manager
    uis.web.manager.start()

    libs.browser.open('http://localhost:7777/')

    # Start the storage database
    import libs.storage.manager
    libs.storage.manager.start()

    # Start the API
    ## main loop
    while libs.globals['running']:
        time.sleep(1)

    ## cleanup
    libs.events.broadcast('shutdown')
    libs.threadmanager.killall()
    libs.threadmanager.close_sockets()
    friends.save_friends()
    libs.config.save()

    exit()

