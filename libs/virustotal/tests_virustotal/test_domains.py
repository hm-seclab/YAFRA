'''
Tests for domains.py
'''
import json
from unittest import TestCase
from unittest.mock import patch, Mock

from libs.core.get_path import get_path
from libs.kafka.logging import LogMessage
from libs.virustotal.domains import get_vt_information_domains


class DomainsTests(TestCase):
    '''
    Tests for the domains script.
    '''

    def test_get_vt_information_domains_throws_exception_when_given_None_as_vt_key_parameter(self):
        '''
        Test to check if the function throws an exception
        when None has been given as the virus total
        api key parameter.
        '''
        test_list = []

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_vt_information_domains(None, test_list, "TEST_SERVICENAME"))

    def test_get_vt_information_domains_throws_exception_when_given_None_as_domains_parameter(self):
        '''
        Test to check if the function throws an exception
        when None has been given as the domains parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_vt_information_domains("TEST_API_KEY", None, "TEST_SERVICENAME"))

    def test_get_vt_information_domains_returns_empty_dict_when_given_empty_list_as_parameter(self):
        '''
        Test to check if the function returns an empty dict
        when an empty list has been given as a parameter.
        '''
        test_list = []

        output = get_vt_information_domains("TEST_API_KEY", test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 0)

    def test_get_vt_information_domains_throws_exception_when_given_None_as_list_element(self):
        '''
        Test to check if the function throws an exception
        when None has been given as a list element.
        '''
        test_list = [None]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_vt_information_domains(None, test_list, "TEST_SERVICENAME"))

    def test_get_vt_information_domains_throws_exception_when_given_None_as_response(self):
        '''
        Test to check if the function throws an exception
        when None has been given as the response.
        '''

        mock_get_patcher = patch('requests.get')

        test_list = ["TEST_DOMAIN"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = None

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_vt_information_domains("TEST_API_KEY", test_list, "TEST_SERVICENAME"))

        mock_get_patcher.stop()

    def test_get_vt_information_domains_throws_exception_when_given_None_as_the_response_status_code(self):
        '''
        Test to check if the function throws an exception
        when None has been given as the response status code.
        '''

        mock_get_patcher = patch('requests.get')

        test_list = ["TEST_DOMAIN"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=None, text="TEST")

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_vt_information_domains("TEST_API_KEY", test_list, "TEST_SERVICENAME"))

        mock_get_patcher.stop()

    def test_get_vt_information_domains_throws_exception_when_given_None_as_the_response_text(self):
        '''
        Test to check if the function throws an exception
        when None has been given as the response text.
        '''

        mock_get_patcher = patch('requests.get')

        test_list = ["TEST_DOMAIN"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=200, text=None)

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_vt_information_domains("TEST_API_KEY", test_list, "TEST_SERVICENAME"))

        mock_get_patcher.stop()

    def test_get_vt_information_domains_throws_exception_when_getting_400_response(self):
        '''
        Test to check if the function throws an exception
        when the response has 400 as the status code.
        '''

        mock_get_patcher = patch('requests.get')

        test_list = ["TEST_DOMAIN"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=400, text="TEST_TEXT")

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_vt_information_domains("TEST_API_KEY", test_list, "TEST_SERVICENAME"))

        mock_get_patcher.stop()

    def test_get_vt_information_domains_throws_exception_when_getting_500_response(self):
        '''
        Test to check if the function throws an exception
        when the response has 500 as the response status code.
        '''

        mock_get_patcher = patch('requests.get')

        test_list = ["TEST_DOMAIN"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=500, text="TEST_TEXT")

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_vt_information_domains("TEST_API_KEY", test_list, "TEST_SERVICENAME"))

        mock_get_patcher.stop()

    def test_get_vt_information_domainsreturns_valid_dict_when_given_response_with_valid_keys(self):
        '''
        Test to check if the function returns a valid dict
        when a valid response with valid keys has been given.
        '''

        mock_get_patcher = patch('requests.get')

        path = get_path(__file__, 'resources/vt_response_valid.json')

        with open(str(path)) as test_json_file:
            test_text = json.load(test_json_file)
            test_text = json.dumps(test_text)
            test_list = ["VT_TEST"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=200, text=test_text)

        output = get_vt_information_domains("TEST_API_KEY", test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["VT_TEST"], dict)
        self.assertTrue(len(output["VT_TEST"]) == 7)
        self.assertIsNotNone(output["VT_TEST"]["Possible_subdomains"])
        self.assertIsNotNone(output["VT_TEST"]["Sibbling_domains"])
        self.assertIsNotNone(output["VT_TEST"]["Categories"])
        self.assertIsNotNone(output["VT_TEST"]["IPs"])
        self.assertIsNotNone(output["VT_TEST"]["Detected_files"])
        self.assertIsNotNone(output["VT_TEST"]["Undetected_files"])
        self.assertIsNotNone(output["VT_TEST"]["Vendor"])
        self.assertIsInstance(output["VT_TEST"]["Possible_subdomains"], list)
        self.assertIsInstance(output["VT_TEST"]["Sibbling_domains"], list)
        self.assertIsInstance(output["VT_TEST"]["Categories"], str)
        self.assertIsInstance(output["VT_TEST"]["IPs"], list)
        self.assertIsInstance(output["VT_TEST"]["Detected_files"], int)
        self.assertIsInstance(output["VT_TEST"]["Undetected_files"], int)
        self.assertIsInstance(output["VT_TEST"]["Vendor"], str)
        self.assertTrue(len(output["VT_TEST"]["Possible_subdomains"]) == 2)
        self.assertTrue(len(output["VT_TEST"]["Sibbling_domains"]) == 0)
        self.assertTrue(len(output["VT_TEST"]["IPs"]) == 2)
