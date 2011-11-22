#! /usr/bin/env python
'''Run unit tests on Project Vomun'''
import unittest
import sys

# Load the unit tests
from unittests.code.libs.config import *
from unittests.code.libs.errors import *
from unittests.code.libs.friends import *
from unittests.code.libs.globals import *
from unittests.code.libs.browser import *
from unittests.code.libs.encryption.rsa import *
from unittests.code.libs.encryption.base import *

# Load additional tests
if '--config' in sys.argv:
    from unittests.setup.config import *

if __name__ == '__main__':
    unittest.main()
