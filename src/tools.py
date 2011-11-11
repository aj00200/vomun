#! /usr/bin/env python
print('''
============================
= Anon+ Tools v0.0.0b0pre1
============================
''')

import sys
import xmlrpclib

api = xmlrpclib.ServerProxy('http://localhost:3451/')

def out(message):
    print(' [*] %s' % message)

if '--shutdown' in sys.argv:
    out('Shutting down Anon+')
    api.shutdown()

print('''
Goodbye :)
''')