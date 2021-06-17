'''
Tests for environment.py
'''

import os

from unittest import TestCase, mock

from environment import envvar

class EnvironmentTests(TestCase):
    '''
    Tests for the env-vars.
    '''

    @mock.patch.dict(os.environ, {"SERVER_NAME": "localhost"})
    def test_fenvvar_on_existing_envvar(self):
        '''
        Test to check if the env-var exists.
        '''
        servername = envvar("SERVER_NAME", "127.0.0.1")
        self.assertEqual(servername, "localhost")
