'''
Tests for enterprise.py
'''
from unittest import TestCase
from unittest.mock import patch

from libs.kafka.logging import LogMessage
from libs.mitre.enterprise import get_mitre_information_tactics_enterprise


class EnterpriseTests(TestCase):
    '''
    Tests for the enterprise script.
    '''

    def test_get_mitre_information_tactics_enterprise_throws_exception_when_given_None_as_vt_key_parameter(self):
        '''
        Test to check if the function throws an exception
        when None has been given as the tactics list
        parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_mitre_information_tactics_enterprise(None, "TEST_SERVICENAME"))

    def test_get_mitre_information_tactics_enterprise_returns_empty_dict_when_given_empty_list_as_parameter(self):
        '''
        Test to check if the function returns an empty dict
        when an empty list has been given as a parameter.
        '''
        test_list = []

        output = get_mitre_information_tactics_enterprise(test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 0)

    def test_get_mitre_information_tactics_enterprise_throws_exception_when_given_None_as_list_element(self):
        '''
        Test to check if the function throws an exception
        when None has been given as a list element.
        '''
        test_list = [None]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_mitre_information_tactics_enterprise(test_list, "TEST_SERVICENAME"))

    def test_get_mitre_information_tactics_enterprise_returns_valid_dict_when_given_response_with_valid_keys(self):
        '''
        Test to check if the function returns a valid dict
        when a valid response with valid keys has been given.
        '''

        test_list = ["TA0011"]

        output = get_mitre_information_tactics_enterprise(test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["TA0011"], dict)
        self.assertTrue(len(output["TA0011"]) == 4)
        self.assertIsNotNone(output["TA0011"]["TA-ID"])
        self.assertIsNotNone(output["TA0011"]["Title"])
        self.assertIsNotNone(output["TA0011"]["Summary"])
        self.assertIsNotNone(output["TA0011"]["Mitre_Link"])
        self.assertIsInstance(output["TA0011"]["TA-ID"], str)
        self.assertIsInstance(output["TA0011"]["Title"], str)
        self.assertIsInstance(output["TA0011"]["Summary"], str)
        self.assertIsInstance(output["TA0011"]["Mitre_Link"], str)
