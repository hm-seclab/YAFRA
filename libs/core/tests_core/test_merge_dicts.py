'''
Tests for merge_dicts.py
'''
from unittest import TestCase
from unittest.mock import patch

from libs.core.merge_dicts import merge_dicts
from libs.kafka.logging import LogMessage


class FilterTests(TestCase):
    '''
    Tests for merge_dicts.
    '''

    def test_merge_dicts_returns_empty_dict_when_given_empty_target_dict_and_empty_source_dict(self):
        '''
        Test to check if the function returns an empty dict,
        when an empty dict has been given as the target and the source parameter.
        '''
        test_target_dict = {}
        test_source_dict = {}

        output = merge_dicts(test_target_dict, test_source_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 0)

    def test_merge_dicts_returns_source_dict_when_given_empty_target_dict(self):
        '''
        Test to check if the function returns the given source dict,
        when an empty dict has been given as the target parameter.
        '''
        test_target_dict = {}
        test_source_dict = {}
        test_source_dict["key1"] = [1, 2]
        test_source_dict["key2"] = ["a", "b", "c"]

        output = merge_dicts(test_target_dict, test_source_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertTrue(len(output["key1"]) == 2)
        self.assertTrue(len(output["key2"]) == 3)

    def test_merge_dicts_returns_target_dict_when_given_empty_source_dict(self):
        '''
        Test to check if the function returns the given target dict,
        when an empty dict has been given as the source parameter.
        '''
        test_target_dict = {}
        test_target_dict["key1"] = [1, 2]
        test_target_dict["key2"] = ["a", "b", "c"]
        test_source_dict = {}

        output = merge_dicts(test_target_dict, test_source_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertTrue(len(output["key1"]) == 2)
        self.assertTrue(len(output["key2"]) == 3)

    def test_merge_dicts_throws_exception_when_given_None_as_target_dict_and_None_as_source_dict(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as the target and the source parameter.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, merge_dicts(None, None, "TEST_SERVICENAME"))

    def test_merge_dicts_throws_exception_when_given_None_as_target_dict(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as the target parameter.
        '''
        test_source_dict = {}
        test_source_dict["key1"] = [1, 2]
        test_source_dict["key2"] = ["a", "b", "c"]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, merge_dicts(None, test_source_dict, "TEST_SERVICENAME"))

    def test_merge_dicts_throws_exception_when_given_None_as_source_dict(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as the target parameter.
        '''

        test_target_dict = {}
        test_target_dict["key1"] = [1, 2]
        test_target_dict["key2"] = ["a", "b", "c"]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, merge_dicts(test_target_dict, None, "TEST_SERVICENAME"))

    def test_merge_dicts_returns_merged_dict_from_two_dicts_with_different_keys_and_different_values(self):
        '''
        Test to check if the function returns a merged
        dict, when two dicts with different keys and different
        values have been given as the parameters.
        '''
        test_target_dict = {}
        test_target_dict["key1"] = [1, 2]
        test_target_dict["key2"] = ["a", "b", "c"]
        test_source_dict = {}
        test_source_dict["key3"] = "a"
        test_source_dict["key4"] = 1

        output = merge_dicts(test_target_dict, test_source_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 4)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertIsInstance(output["key3"], str)
        self.assertIsInstance(output["key4"], int)
        self.assertTrue(len(output["key1"]) == 2)
        self.assertTrue(len(output["key2"]) == 3)

    def test_merge_dicts_returns_merged_dict_from_two_dicts_with_different_keys_and_same_values(self):
        '''
        Test to check if the function returns a merged
        dict, when two dicts with different keys and same
        values have been given as the parameters.
        '''
        test_target_dict = {}
        test_target_dict["key1"] = [1, 2]
        test_target_dict["key2"] = ["a", "b", "c"]
        test_source_dict = {}
        test_source_dict["key3"] = [1, 2]
        test_source_dict["key4"] = ["a", "b", "c"]

        output = merge_dicts(test_target_dict, test_source_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 4)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertIsInstance(output["key3"], list)
        self.assertIsInstance(output["key4"], list)
        self.assertTrue(len(output["key1"]) == 2)
        self.assertTrue(len(output["key2"]) == 3)
        self.assertTrue(len(output["key3"]) == 2)
        self.assertTrue(len(output["key4"]) == 3)

    def test_merge_dicts_returns_merged_dict_from_two_dicts_with_same_keys_and_same_values(self):
        '''
        Test to check if the function returns a merged
        dict, when two dicts with same keys and same
        values have been given as the parameters.
        '''
        test_target_dict = {}
        test_target_dict["key1"] = [1, 2]
        test_target_dict["key2"] = ["a", "b", "c"]
        test_source_dict = {}
        test_source_dict["key1"] = [1, 2]
        test_source_dict["key2"] = ["a", "b", "c"]

        output = merge_dicts(test_target_dict, test_source_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertTrue(len(output["key1"]) == 4)
        self.assertTrue(len(output["key2"]) == 6)

    def test_merge_dicts_returns_merged_dict_from_two_dicts_with_same_keys_and_different_values_but_same_type(self):
        '''
        Test to check if the function returns a merged
        dict, when two dicts with same keys and different
        values with the same type have been given as the parameters.
        '''
        test_target_dict = {}
        test_target_dict["key1"] = [1, 2]
        test_target_dict["key2"] = ["a", "b", "c"]
        test_source_dict = {}
        test_source_dict["key1"] = [3, 4]
        test_source_dict["key2"] = ["d", "e", "f"]

        output = merge_dicts(test_target_dict, test_source_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertTrue(len(output["key1"]) == 4)
        self.assertTrue(len(output["key2"]) == 6)

    def test_merge_dicts_throws_exception_when_given_two_dicts_with_same_keys_and_different_values_with_different_type(self):
        '''
        Test to check if the function returns a merged
        dict, when two dicts with same keys and different
        values with the same type have been given as the parameters.
        '''
        test_target_dict = {}
        test_target_dict["key1"] = [1, 2]
        test_target_dict["key2"] = ["a", "b", "c"]
        test_source_dict = {}
        test_source_dict["key1"] = "a"
        test_source_dict["key2"] = 1

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, merge_dicts(test_target_dict, test_source_dict, "TEST_SERVICENAME"))
