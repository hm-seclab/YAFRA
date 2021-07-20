'''
Tests for iso_handler.py
'''
from unittest import TestCase
from unittest.mock import patch

from libs.countrycodes.iso_handler import convert_alpha_2_to_alpha_3, convert_alpha_2_to_qualified_name
from libs.kafka.logging import LogMessage


class FilterTests(TestCase):
    '''
    Tests for iso_handler.
    '''

    def test_convert_alpha_2_to_alpha_3_returns_unknown_when_given_empty_string(self):
        '''
        Test to check if the function returns the string Unknown,
        when an empty string has been given as a parameter.
        '''
        test_string = ""

        output = convert_alpha_2_to_alpha_3(test_string, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, str)
        self.assertEqual(output, "Unknown")

    def test_convert_alpha_2_to_alpha_3_throws_exception_when_given_None_as_parameter(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, convert_alpha_2_to_alpha_3(None, "TEST_SERVICENAME"))

    def test_convert_alpha_2_to_alpha_3_calls_pycountry_countries_get_exactly_once_with_alpha_2_as_a_parameter(self):
        '''
        Test to check if the function calls the
        pycountry.countries.get method exactly once
        when alpha 2 has been given as a parameter.
        '''
        test_string = "111.111.111.111"

        with patch('pycountry.countries.get') as mock_requests:
            output = convert_alpha_2_to_alpha_3(test_string, "TEST_SERVICENAME")
            mock_requests.assert_called_once()

        self.assertIsNotNone(output)
        self.assertNotEqual(output, "Unknown")

    def test_convert_alpha_2_to_qualified_name_returns_unknown_when_given_empty_string(self):
        '''
        Test to check if the function returns the string Unknown,
        when an empty string has been given as a parameter.
        '''
        test_string = ""

        output = convert_alpha_2_to_qualified_name(test_string, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, str)
        self.assertEqual(output, "Unknown")

    def test_convert_alpha_2_to_qualified_name_throws_exception_when_given_None_as_parameter(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, convert_alpha_2_to_qualified_name(None, "TEST_SERVICENAME"))

    def test_convert_alpha_2_to_qualified_name_calls_pycountry_countries_get_exactly_once_with_alpha_2_as_a_parameter(self):
        '''
        Test to check if the function calls the
        pycountry.countries.get method exactly once
        when alpha 2 has been given as a parameter.
        '''
        test_string = "111.111.111.111"

        with patch('pycountry.countries.get') as mock_requests:
            output = convert_alpha_2_to_alpha_3(test_string, "TEST_SERVICENAME")
            mock_requests.assert_called_once()

        self.assertIsNotNone(output)
        self.assertNotEqual(output, "Unknown")