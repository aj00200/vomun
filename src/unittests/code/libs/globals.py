import unittest
import libs.globals

class RequiredVariables(unittest.TestCase):
    def test_global_vars_exists(self):
        '''Make sure libs.globals.global_vars exists.'''
        self.assertIsNotNone(libs.globals.global_vars)

    def test_global_vars_running(self):
        '''Make sure the running state is set to True by default.'''
        self.assertTrue(libs.globals.global_vars['running'])

    def test_global_vars_anonplus(self):
        '''Make sure libs.globals.global_vars["anon+"] exists.'''
        self.assertIsNotNone(libs.globals.global_vars['anon+'])

    def test_global_vars_anonplus_version(self):
        '''Make sure libs.globals.global_vars["anon+"]["VERSION"] exists.'''
        self.assertIsNotNone(libs.globals.global_vars['anon+']['VERSION'])
        self.assertGreater(libs.globals.global_vars['anon+']['VERSION'], 0)

    def test_global_vars_anonplus_banner(self):
        '''Make sure libs.globals.global_vars["anon+"]["banner"] exists'''
        self.assertIsNotNone(libs.globals.global_vars['anon+']['banner'])
