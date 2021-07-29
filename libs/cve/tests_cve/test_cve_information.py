'''
Tests for cve_information.py
'''
import json
from unittest import TestCase
from unittest.mock import patch, Mock

from libs.core.get_path import get_path
from libs.cve.cve_information import get_cve_information
from libs.kafka.logging import LogMessage


class CveInformationTests(TestCase):
    '''
    Tests for cve information
    '''

    def test_get_cve_information_returns_empty_dict_when_given_empty_list_as_parameter(self):
        '''
        Test to check if the function returns an empty dict
        when an empty list has been given as a parameter.
        '''
        test_list = []

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 0)

    def test_get_cve_information_throws_exception_when_given_None_as_parameter(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_cve_information(None, "TEST_SERVICENAME"))

    def test_get_cve_information_throws_exception_when_given_None_as_list_element(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a list element.
        '''
        test_list = [None]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, get_cve_information(test_list, "TEST_SERVICENAME"))

    def test_get_cve_information_returns_empty_dict_when_not_given_string_as_parameter(self):
        '''
        Test to check if the function returns an empty dict
        when a string has not been given as a parameter.
        '''
        test_list_int = [1, 2]
        test_list_list = [[], []]
        test_list_list_string = [["a"], ["b"]]
        test_list_dict = [{}]
        dict_string = {}
        dict_string["key1"] = [1, 2]
        test_list_dict_string = [dict_string]

        output_int = get_cve_information(test_list_int, "TEST_SERVICENAME")
        output_list = get_cve_information(test_list_list, "TEST_SERVICENAME")
        output_list_string = get_cve_information(test_list_list_string, "TEST_SERVICENAME")
        output_dict = get_cve_information(test_list_dict, "TEST_SERVICENAME")
        output_dict_string = get_cve_information(test_list_dict_string, "TEST_SERVICENAME")

        self.assertIsNotNone(output_int)
        self.assertIsNotNone(output_list)
        self.assertIsNotNone(output_list_string)
        self.assertIsNotNone(output_dict)
        self.assertIsNotNone(output_dict_string)
        self.assertIsInstance(output_int, dict)
        self.assertIsInstance(output_list, dict)
        self.assertIsInstance(output_list_string, dict)
        self.assertIsInstance(output_dict, dict)
        self.assertIsInstance(output_dict_string, dict)
        self.assertTrue(len(output_int) == 0)
        self.assertTrue(len(output_list) == 0)
        self.assertTrue(len(output_list_string) == 0)
        self.assertTrue(len(output_dict) == 0)
        self.assertTrue(len(output_dict_string) == 0)

    def test_get_cve_information_returns_empty_dict_when_None_as_the_response(self):
        '''
        Test to check if the function returns an
        empty dict when the response is None.
        '''

        mock_get_patcher = patch('requests.get')

        test_list = ["INVALID_CVEEE"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = None

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 0)

    def test_get_cve_information_returns_empty_dict_when_None_as_the_response_status_code(self):
        '''
        Test to check if the function returns an
        empty dict when the response status code is None.
        '''

        mock_get_patcher = patch('requests.get')

        test_text = "null"
        test_list = ["INVALID_CVEEE"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=None, text=test_text)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 0)


    def test_get_cve_information_returns_empty_dict_when_None_as_the_response_text(self):
        '''
        Test to check if the function returns an
        empty dict when the response text is None.
        '''

        mock_get_patcher = patch('requests.get')

        test_list = ["INVALID_CVEEE"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=200, text=None)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 0)

    def test_get_cve_information_returns_None_as_dict_values_when_getting_400_response(self):
        '''
        Test to check if the function returns None
        as the return dict values when the response
        has a 400 as the status code.
        '''

        mock_get_patcher = patch('requests.get')

        test_text = "null"
        test_list = ["INVALID_CVEEE"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=400, text=test_text)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["INVALID_CVEEE"], dict)
        self.assertTrue(len(output["INVALID_CVEEE"]) == 5)
        self.assertIsNone(output["INVALID_CVEEE"]["CVS-Score"])
        self.assertIsNone(output["INVALID_CVEEE"]["Complexity"])
        self.assertIsNone(output["INVALID_CVEEE"]["Vektor"])
        self.assertIsNone(output["INVALID_CVEEE"]["Summary"])
        self.assertIsNone(output["INVALID_CVEEE"]["Exploit-DB"])

    def test_get_cve_information_returns_None_as_dict_values_when_getting_500_response(self):
        '''
        Test to check if the function returns None
        as the return dict values when the response
        has a 500 as the status code.
        '''

        mock_get_patcher = patch('requests.get')

        test_text = "null"
        test_list = ["INVALID_CVEEE"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=500, text=test_text)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["INVALID_CVEEE"], dict)
        self.assertTrue(len(output["INVALID_CVEEE"]) == 5)
        self.assertIsNone(output["INVALID_CVEEE"]["CVS-Score"])
        self.assertIsNone(output["INVALID_CVEEE"]["Complexity"])
        self.assertIsNone(output["INVALID_CVEEE"]["Vektor"])
        self.assertIsNone(output["INVALID_CVEEE"]["Summary"])
        self.assertIsNone(output["INVALID_CVEEE"]["Exploit-DB"])

    def test_get_cve_information_returns_None_as_dict_values_when_given_invalid_cve_as_parameter(self):
        '''
        Test to check if the function returns None
        as the return dict values when an invalid
        cve has not been given as a parameter.
        '''

        mock_get_patcher = patch('requests.get')

        test_text = "null"
        test_list = ["INVALID_CVEEE"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=200, text=test_text)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["INVALID_CVEEE"], dict)
        self.assertTrue(len(output["INVALID_CVEEE"]) == 5)
        self.assertIsNone(output["INVALID_CVEEE"]["CVS-Score"])
        self.assertIsNone(output["INVALID_CVEEE"]["Complexity"])
        self.assertIsNone(output["INVALID_CVEEE"]["Vektor"])
        self.assertIsNone(output["INVALID_CVEEE"]["Summary"])
        self.assertIsNone(output["INVALID_CVEEE"]["Exploit-DB"])

    def test_get_cve_information_returns_None_as_cvescore_when_cvss_key_missing(self):
        '''
        Test to check if the function returns None
        as the cvescore value when the cvss key is
        missing in the response.
        '''

        mock_get_patcher = patch('requests.get')

        path = get_path(__file__, 'resources/cve_response_missing_cvss.json')

        with open(str(path)) as test_json_file:
            test_text = json.load(test_json_file)
            test_text = json.dumps(test_text)
            test_list = ["CVE-2020-0601"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=200, text=test_text)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["CVE-2020-0601"], dict)
        self.assertTrue(len(output["CVE-2020-0601"]) == 5)
        self.assertIsNone(output["CVE-2020-0601"]["CVS-Score"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Complexity"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Vektor"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Summary"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Exploit-DB"])

    def test_get_cve_information_returns_None_as_complexity_and_None_as_vector_when_access_key_missing(self):
        '''
        Test to check if the function returns None
        as the complexity value and as the vector
        value when the access key is missing
        in the response.
        '''

        mock_get_patcher = patch('requests.get')

        path = get_path(__file__, 'resources/cve_response_missing_access.json')

        with open(str(path)) as test_json_file:
            test_text = json.load(test_json_file)
            test_text = json.dumps(test_text)
            test_list = ["CVE-2020-0601"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=200, text=test_text)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["CVE-2020-0601"], dict)
        self.assertTrue(len(output["CVE-2020-0601"]) == 5)
        self.assertIsNotNone(output["CVE-2020-0601"]["CVS-Score"])
        self.assertIsNone(output["CVE-2020-0601"]["Complexity"])
        self.assertIsNone(output["CVE-2020-0601"]["Vektor"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Summary"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Exploit-DB"])

    def test_get_cve_information_returns_None_as_complexity_when_complexity_key_missing(self):
        '''
        Test to check if the function returns None
        as the complexity value when the complexity
        key is missing in the response.
        '''

        mock_get_patcher = patch('requests.get')

        path = get_path(__file__, 'resources/cve_response_missing_complexity.json')

        with open(str(path)) as test_json_file:
            test_text = json.load(test_json_file)
            test_text = json.dumps(test_text)
            test_list = ["CVE-2020-0601"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=200, text=test_text)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["CVE-2020-0601"], dict)
        self.assertTrue(len(output["CVE-2020-0601"]) == 5)
        self.assertIsNotNone(output["CVE-2020-0601"]["CVS-Score"])
        self.assertIsNone(output["CVE-2020-0601"]["Complexity"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Vektor"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Summary"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Exploit-DB"])

    def test_get_cve_information_returns_None_as_vector_when_vector_key_missing(self):
        '''
        Test to check if the function returns None
        as the vector value when the vector key is
        missing in the response.
        '''

        mock_get_patcher = patch('requests.get')

        path = get_path(__file__, 'resources/cve_response_missing_vector.json')

        with open(str(path)) as test_json_file:
            test_text = json.load(test_json_file)
            test_text = json.dumps(test_text)
            test_list = ["CVE-2020-0601"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=200, text=test_text)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["CVE-2020-0601"], dict)
        self.assertTrue(len(output["CVE-2020-0601"]) == 5)
        self.assertIsNotNone(output["CVE-2020-0601"]["CVS-Score"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Complexity"])
        self.assertIsNone(output["CVE-2020-0601"]["Vektor"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Summary"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Exploit-DB"])

    def test_get_cve_information_returns_None_as_summary_when_summary_key_missing(self):
        '''
        Test to check if the function returns None
        as the summary value when the summary key is
        missing in the response.
        '''

        mock_get_patcher = patch('requests.get')

        path = get_path(__file__, 'resources/cve_response_missing_summary.json')

        with open(str(path)) as test_json_file:
            test_text = json.load(test_json_file)
            test_text = json.dumps(test_text)
            test_list = ["CVE-2020-0601"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=200, text=test_text)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["CVE-2020-0601"], dict)
        self.assertTrue(len(output["CVE-2020-0601"]) == 5)
        self.assertIsNotNone(output["CVE-2020-0601"]["CVS-Score"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Complexity"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Vektor"])
        self.assertIsNone(output["CVE-2020-0601"]["Summary"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Exploit-DB"])

    def test_get_cve_information_returns_None_as_exploit_db_when_refmap_key_missing(self):
        '''
        Test to check if the function returns None
        as the exploit db value when the refmap key
        is missing in the response.
        '''

        mock_get_patcher = patch('requests.get')

        path = get_path(__file__, 'resources/cve_response_missing_refmap.json')

        with open(str(path)) as test_json_file:
            test_text = json.load(test_json_file)
            test_text = json.dumps(test_text)
            test_list = ["CVE-2020-0601"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=200, text=test_text)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["CVE-2020-0601"], dict)
        self.assertTrue(len(output["CVE-2020-0601"]) == 5)
        self.assertIsNotNone(output["CVE-2020-0601"]["CVS-Score"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Complexity"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Vektor"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Summary"])
        self.assertIsNone(output["CVE-2020-0601"]["Exploit-DB"])

    def test_get_cve_information_returns_None_as_exploit_db_when_exploit_db_key_missing(self):
        '''
        Test to check if the function returns None
        as the exploit db value when the exploit db
        key is missing in the response.
        '''

        mock_get_patcher = patch('requests.get')

        path = get_path(__file__, 'resources/cve_response_missing_exploit_db.json')

        with open(str(path)) as test_json_file:
            test_text = json.load(test_json_file)
            test_text = json.dumps(test_text)
            test_list = ["CVE-2020-0601"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=200, text=test_text)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["CVE-2020-0601"], dict)
        self.assertTrue(len(output["CVE-2020-0601"]) == 5)
        self.assertIsNotNone(output["CVE-2020-0601"]["CVS-Score"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Complexity"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Vektor"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Summary"])
        self.assertIsNone(output["CVE-2020-0601"]["Exploit-DB"])

    def test_get_cve_information_returns_valid_dict_when_given_valid_response_with_all_keys(self):
        '''
        Test to check if the function returns a
        valid dict when the response is valid
        and contains all keys.
        '''

        mock_get_patcher = patch('requests.get')

        path = get_path(__file__, 'resources/cve_response_valid.json')

        with open(str(path)) as test_json_file:
            test_text = json.load(test_json_file)
            test_text = json.dumps(test_text)
            test_list = ["CVE-2020-0601"]

        mock_get = mock_get_patcher.start()

        mock_get.return_value = Mock(status_code=200, text=test_text)

        output = get_cve_information(test_list, "TEST_SERVICENAME")

        mock_get_patcher.stop()

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["CVE-2020-0601"], dict)
        self.assertTrue(len(output["CVE-2020-0601"]) == 5)
        self.assertIsNotNone(output["CVE-2020-0601"]["CVS-Score"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Complexity"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Vektor"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Summary"])
        self.assertIsNotNone(output["CVE-2020-0601"]["Exploit-DB"])