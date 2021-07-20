'''
Tests for filter.py
'''

from unittest import TestCase
from unittest.mock import patch

from libs.core.filter import filter_dict_values, replace_item, filter_by_blacklist
from libs.kafka.logging import LogMessage


class FilterTests(TestCase):
    '''
    Tests for the filters.
    '''

    def test_filter_dict_values_returns_empty_dict_when_given_empty_dict(self):
        '''
        Test to check if the function returns an empty dict,
        when an empty dict has been given as a parameter.
        '''
        test_dict = {}
        output = filter_dict_values(test_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 0)

    def test_filter_dict_values_throws_exception_when_given_None_as_dict(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a dict parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, filter_dict_values(None, "TEST_SERVICENAME"))

    def test_filter_dict_values_returns_a_dict_with_lists_when_given_a_dict_with_lists_only(self):
        '''
        Test to check if the function returns a dict with lists,
        when a dict with lists only has been given as a parameter.
        '''
        test_dict = {}
        test_dict["key1"] = [1, 2]
        test_dict["key2"] = ["a", "b", "c"]

        output = filter_dict_values(test_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertTrue(len(output["key1"]) == 2)
        self.assertTrue(len(output["key2"]) == 3)

    def test_filter_dict_values_returns_a_dict_with_lists_and_other_types_when_given_a_dict_with_lists_and_other_types(
            self):
        '''
        Test to check if the function returns a dict with lists and other types,
        when a dict with lists and other types has been given as a parameter.
        '''
        test_dict = {}
        test_dict2 = {}
        test_dict["key1"] = [1, 2]
        test_dict["key2"] = ["a", "b", "c"]
        test_dict["key3"] = "a"
        test_dict["key4"] = 1
        test_dict["key5"] = test_dict2

        output = filter_dict_values(test_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 5)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertIsInstance(output["key3"], str)
        self.assertIsInstance(output["key4"], int)
        self.assertIsInstance(output["key5"], dict)
        self.assertTrue(len(output["key1"]) == 2)
        self.assertTrue(len(output["key2"]) == 3)

    def test_filter_dict_values_returns_a_dict_with_lists_in_which_every_element_occurs_only_one_time(self):
        '''
        Test to check if the function returns a dict with lists, in which
        every element occurs only one time.
        '''
        test_dict = {}
        test_dict["key1"] = [1, 2, 1, 2, 1, 2]
        test_dict["key2"] = ["a", "b", "c", "a", "b", "c"]
        test_dict["key3"] = ["a", "b", "c"]

        output = filter_dict_values(test_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 3)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertIsInstance(output["key3"], list)
        self.assertTrue(len(output["key1"]) == 2)
        self.assertTrue(len(output["key2"]) == 3)
        self.assertTrue(len(output["key3"]) == 3)

    def test_replace_item_returns_empty_dict_when_given_empty_findings_dict(self):
        '''
        Test to check if the function returns an empty dict,
        when an empty findings dict has been given as a parameter.
        '''
        test_findings_dict = {}

        output = replace_item(test_findings_dict, "key1", "finding_to_be_blocked_1", "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 0)

    def test_replace_item_throws_exception_when_given_None_as_dict(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a dict parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, replace_item(None, "key1", "finding_to_be_blocked_1", "TEST_SERVICENAME"))

    def test_replace_items_returns_unchanged_dict_if_the_block_key_is_empty(self):
        '''
        Test to check if the function returns the dict
        unchanged, if the block key is empty.
        '''
        test_findings_dict = {}
        test_findings_dict["key1"] = ["finding1a", "finding1b", "finding1c", "finding_to_be_blocked_1"]
        test_findings_dict["key2"] = ["finding2a", "finding2b", "finding2c", "finding_to_be_blocked_1",
                                      "finding_to_be_blocked_2"]

        output = replace_item(test_findings_dict, "", "finding_to_be_blocked_1", "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)

    def test_replace_items_returns_unchanged_dict_if_the_block_value_is_empty(self):
        '''
        Test to check if the function returns the dict
        unchanged, if the block value is empty.
        '''
        test_findings_dict = {}
        test_findings_dict["key1"] = ["finding1a", "finding1b", "finding1c", "finding_to_be_blocked_1"]
        test_findings_dict["key2"] = ["finding2a", "finding2b", "finding2c", "finding_to_be_blocked_1",
                                      "finding_to_be_blocked_2"]

        output = replace_item(test_findings_dict, "key1", "", "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)

    def test_replace_items_returns_unchanged_dict_if_the_block_key_is_None(self):
        '''
        Test to check if the function returns the dict
        unchanged, if the block key is None.
        '''
        test_findings_dict = {}
        test_findings_dict["key1"] = ["finding1a", "finding1b", "finding1c", "finding_to_be_blocked_1"]
        test_findings_dict["key2"] = ["finding2a", "finding2b", "finding2c", "finding_to_be_blocked_1",
                                      "finding_to_be_blocked_2"]

        output = replace_item(test_findings_dict, None, "finding_to_be_blocked_1", "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)

    def test_replace_items_returns_unchanged_dict_if_the_block_value_is_None(self):
        '''
        Test to check if the function returns the dict
        unchanged, if the block value is None.
        '''
        test_findings_dict = {}
        test_findings_dict["key1"] = ["finding1a", "finding1b", "finding1c", "finding_to_be_blocked_1"]
        test_findings_dict["key2"] = ["finding2a", "finding2b", "finding2c", "finding_to_be_blocked_1",
                                      "finding_to_be_blocked_2"]

        output = replace_item(test_findings_dict, "key1", None, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)

    def test_replace_item_removes_given_value_for_given_key_and_returns_a_dict(self):
        '''
        Test to check if the function removes a given value for a given key
        and returns a dict, without this value.
        '''
        test_findings_dict = {}
        test_findings_dict["key1"] = ["finding1a", "finding1b", "finding1c", "finding_to_be_blocked_1"]
        test_findings_dict["key2"] = ["finding2a", "finding2b", "finding2c", "finding_to_be_blocked_1",
                                      "finding_to_be_blocked_2"]

        output = replace_item(test_findings_dict, "key1", "finding_to_be_blocked_1", "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertTrue(len(output["key1"]) == 3)
        self.assertTrue(len(output["key2"]) == 5)

    def test_replace_item_removes_multiple_given_value_for_given_key_and_returns_a_dicts(self):
        '''
        Test to check if the function removes multiple given value for a given key
        and returns a dict, without this value.
        '''
        test_findings_dict = {}
        test_findings_dict["key1"] = ["finding1a", "finding1b", "finding1c", "finding_to_be_blocked_1"]
        test_findings_dict["key2"] = ["finding2a", "finding2b", "finding2c", "finding_to_be_blocked_1",
                                      "finding_to_be_blocked_2"]

        output = replace_item(test_findings_dict, "key1", "finding_to_be_blocked_1", "TEST_SERVICENAME")
        output = replace_item(test_findings_dict, "key2", "finding_to_be_blocked_1", "TEST_SERVICENAME")
        output = replace_item(test_findings_dict, "key2", "finding_to_be_blocked_2", "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertTrue(len(output["key1"]) == 3)
        self.assertTrue(len(output["key2"]) == 3)

    def test_filter_by_blacklist_returns_empty_dict_when_given_empty_findings_dict(self):
        '''
        Test to check if the function returns an empty dict,
        when an empty dict has been given as the findings parameter.
        '''
        test_findings_dict = {}

        test_blacklist_dict = {}
        test_blacklist_dict["key1"] = ["finding_to_be_blocked_1"]
        test_blacklist_dict["key2"] = ["finding_to_be_blocked_2"]

        output = filter_by_blacklist(test_findings_dict, test_blacklist_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 0)

    def test_filter_by_blacklist_throws_exception_when_findings_dict_is_None(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a finding dict parameter.
        '''

        test_blacklist_dict = {}
        test_blacklist_dict["key1"] = ["finding_to_be_blocked_1"]
        test_blacklist_dict["key2"] = ["finding_to_be_blocked_2"]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, filter_by_blacklist(None, test_blacklist_dict, "TEST_SERVICENAME"))

    def test_filter_by_blacklist_returns_unchanged_dict_when_given_empty_blacklist_dict(self):
        '''
        Test to check if the function returns an unchanged dict,
        when an empty dict has been given as the blacklist parameter.
        '''

        test_findings_dict = {}
        test_findings_dict["key1"] = ["finding1a", "finding1b", "finding1c", "finding_to_be_blocked_1"]
        test_findings_dict["key2"] = ["finding2a", "finding2b", "finding2c", "finding_to_be_blocked_1",
                                      "finding_to_be_blocked_2"]

        test_blacklist_dict = {}

        output = filter_by_blacklist(test_findings_dict, test_blacklist_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)

    def test_filter_by_blacklist_returns_unchanged_dict_when_given_None_as_blacklist_dict(self):
        '''
        Test to check if the function returns an unchanged dict,
        when an None has been given as the blacklist parameter.
        '''

        test_findings_dict = {}
        test_findings_dict["key1"] = ["finding1a", "finding1b", "finding1c", "finding_to_be_blocked_1"]
        test_findings_dict["key2"] = ["finding2a", "finding2b", "finding2c", "finding_to_be_blocked_1",
                                      "finding_to_be_blocked_2"]

        output = filter_by_blacklist(test_findings_dict, None, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)

    def test_filter_by_blacklist_returns_findings_without_blocked_values_for_given_keys(self):
        '''
        Test to check if the function returns a dict of findings,
        without values which got stored inside the blacklist.
        Note -> finding_to_be_blocked_1 is only allowed to be blocked,
        inside the key1, because it is declared like this also inside
        the given blacklist.
        '''
        test_findings_dict = {}
        test_findings_dict["key1"] = ["finding1a", "finding1b", "finding1c", "finding_to_be_blocked_1"]
        test_findings_dict["key2"] = ["finding2a", "finding2b", "finding2c", "finding_to_be_blocked_1",
                                      "finding_to_be_blocked_2"]

        test_blacklist_dict = {}
        test_blacklist_dict["key1"] = ["finding_to_be_blocked_1"]
        test_blacklist_dict["key2"] = ["finding_to_be_blocked_2"]

        output = filter_by_blacklist(test_findings_dict, test_blacklist_dict, "TEST_SERVICENAME")

        print(output)

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertTrue(len(output["key1"]) == 3)
        self.assertTrue(len(output["key2"]) == 4)

    def test_filter_by_blacklist_returns_findings_without_blocked_values_for_multiple_keys(self):
        '''
        Test to check if the function removes multiple given value for a given key
        and returns a dict, without this value.
        '''
        test_findings_dict = {}
        test_findings_dict["key1"] = ["finding1a", "finding1b", "finding1c", "finding_to_be_blocked_1"]
        test_findings_dict["key2"] = ["finding2a", "finding2b", "finding2c", "finding_to_be_blocked_1",
                                      "finding_to_be_blocked_2"]

        test_blacklist_dict = {}
        test_blacklist_dict["key1"] = ["finding_to_be_blocked_1"]
        test_blacklist_dict["key2"] = ["finding_to_be_blocked_2"]

        output = filter_by_blacklist(test_findings_dict, test_blacklist_dict, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)
        self.assertIsInstance(output["key1"], list)
        self.assertIsInstance(output["key2"], list)
        self.assertTrue(len(output["key1"]) == 3)
        self.assertTrue(len(output["key2"]) == 4)
        self.assertFalse("finding_to_be_blocked_1" in output["key1"])
        self.assertTrue("finding_to_be_blocked_1" in output["key2"])
        self.assertFalse("finding_to_be_blocked_2" in output["key2"])
