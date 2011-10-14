'''This module manages running threads and kills them all when the program
needs to exist. Threads should stop when thread.stop() is called.
'''
import threading
threads = []
joinlist = []
def register(thread):
    if isinstance(thread, Thread):
        threads.append(thread)
    else:
        raise Exception('Must be a subclass of libs.threadmanager.Thread')
    
def registerForJoin(thread):
    if isinstance(thread, Thread):
        joinlist.append(thread)
    else:
        raise Exception('Must be a subclass of libs.threadmanager.Thread')

def doJoins(timeout=None):
    for thread in joinlist:
        thread.join(timeout)

def killall():
    for thread in threads:
        thread.stop()

class Thread(threading.Thread):
    def __init__(self):
        super(Thread, self).__init__()
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()