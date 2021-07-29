'''
Tests for loader.py
'''
import re
from unittest import TestCase
from unittest.mock import patch

from libs.core.get_path import get_path
from libs.extensions.loader import Extension, generate_dict_with_jsonfield_and_reportfield, load_extensions, \
    append_extensions_misp_types
from libs.kafka.logging import LogMessage


class ExtensionsLoaderTests(TestCase):
    '''
    Tests for the extensions class.
    '''

    def test_generate_dict_with_jsonfield_and_reportfield_returns_empty_dict_when_given_empty_list_as_parameter(self):
        '''
        Test to check if the function returns an empty dict
        when an empty list has been given as a parameter.
        '''
        test_list = []

        output = generate_dict_with_jsonfield_and_reportfield(test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 0)

    def test_generate_dict_with_jsonfield_and_reportfield_throws_exception_when_given_None_as_parameter(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, generate_dict_with_jsonfield_and_reportfield(None, "TEST_SERVICENAME"))

    def test_generate_dict_with_jsonfield_and_reportfield_throws_exception_when_given_None_as_list_element(self):
        '''
        Test to check if the function throws an exception,
        when None has been given as a list element.
        '''
        test_list = [None]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, generate_dict_with_jsonfield_and_reportfield(test_list, "TEST_SERVICENAME"))

    def test_generate_dict_with_jsonfield_and_reportfield_returns_empty_dict_when_not_given_extension_as_list_element(self):
        '''
        Test to check if the function returns an empty dict
        when an extension has not been given as list element.
        '''
        test_list_int = [1, 2]
        test_list_list = [[], []]
        test_list_list_string = [["a"], ["b"]]
        test_list_dict = [{}]
        dict_string = {}
        dict_string["key1"] = [1, 2]
        test_list_dict_string = [dict_string]

        output_int = generate_dict_with_jsonfield_and_reportfield(test_list_int, "TEST_SERVICENAME")
        output_list = generate_dict_with_jsonfield_and_reportfield(test_list_list, "TEST_SERVICENAME")
        output_list_string = generate_dict_with_jsonfield_and_reportfield(test_list_list_string, "TEST_SERVICENAME")
        output_dict = generate_dict_with_jsonfield_and_reportfield(test_list_dict, "TEST_SERVICENAME")
        output_dict_string = generate_dict_with_jsonfield_and_reportfield(test_list_dict_string, "TEST_SERVICENAME")

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

    def test_generate_dict_with_jsonfield_and_reportfield_throws_exception_when_None_as_json_field(self):
        '''
        Test to check if the function throws an exception
        when the json field is None.
        '''
        test_extension = Extension("TEST_NAME", None, "TEST_PATTERN", "TEST_REPORTFIELD", "TEST_MISPTYPE", 0, 0,
                                   False)
        test_list = [test_extension]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, generate_dict_with_jsonfield_and_reportfield(test_list, "TEST_SERVICENAME"))

    def test_generate_dict_with_jsonfield_and_reportfield_throws_exception_when_None_as_report_field(self):
        '''
        Test to check if the function throws an exception
        when the report field is None.
        '''
        test_extension = Extension("TEST_NAME", "TEST_FIELD", "TEST_PATTERN", None, "TEST_MISPTYPE", 0, 0,
                                   False)
        test_list = [test_extension]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, generate_dict_with_jsonfield_and_reportfield(test_list, "TEST_SERVICENAME"))

    def test_generate_dict_with_jsonfield_and_reportfield_throws_exception_when_None_as_json_field_and_None_as_report_field(self):
        '''
        Test to check if the function throws an exception
        when the json field and the report field is None.
        '''
        test_extension = Extension("TEST_NAME", None, "TEST_PATTERN", None, "TEST_MISPTYPE", 0, 0,
                                   False)
        test_list = [test_extension]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, generate_dict_with_jsonfield_and_reportfield(test_list, "TEST_SERVICENAME"))

    def test_generate_dict_with_jsonfield_and_reportfield_returns_valid_dict_when_given_valid_extension_with_valid_json_field_and_valid_report_field_as_parameter(self):
        '''
        Test to check if the function returns a valid dict
        when a valid extension with valid json field and
        valid report field has been given as a paramter.
        '''
        test_extension = Extension("TEST_NAME", "TEST_FIELD", "TEST_PATTERN", "TEST_REPORTFIELD", "TEST_MISPTYPE", 0, 0,
                                   False)
        test_list = [test_extension]

        output = generate_dict_with_jsonfield_and_reportfield(test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["TEST_FIELD"], str)
        self.assertIsNotNone(output["TEST_FIELD"])
        self.assertEqual(output["TEST_FIELD"], "TEST_REPORTFIELD")

    def test_load_extensions_returns_empty_list_when_status_is_missing(self):
        '''
        Test to check if the function returns
        an empty list, when the status inside
        the yafex file is missing.
        '''
        test_yafex_file_path = get_path(__file__, 'resources/test_extension_status_missing.yafex')

        with patch('os.listdir') as mock_listdir, patch('os.path.abspath') as mock_abspath:
            mock_listdir.return_value = ['test_extension_status_missing.yafex']
            mock_abspath.return_value = str(test_yafex_file_path)

            output = load_extensions("TEST_SERVICENAME")

            self.assertIsNotNone(output)
            self.assertIsInstance(output, list)
            self.assertTrue(len(output) == 0)

    def test_load_extensions_returns_empty_list_when_status_is_None(self):
        '''
        Test to check if the function returns
        an empty list, when the status inside
        the yafex file is None.
        '''
        test_yafex_file_path = get_path(__file__, 'resources/test_extension_status_None.yafex')

        with patch('os.listdir') as mock_listdir, patch('os.path.abspath') as mock_abspath:
            mock_listdir.return_value = ['test_extension_status_None.yafex']
            mock_abspath.return_value = str(test_yafex_file_path)

            output = load_extensions("TEST_SERVICENAME")

            self.assertIsNotNone(output)
            self.assertIsInstance(output, list)
            self.assertTrue(len(output) == 0)


    def test_load_extensions_returns_empty_list_when_status_is_disabled_in_yafex(self):
        '''
        Test to check if the function returns
        an empty list, when the status inside
        the yafex file is disabled.
        '''
        test_yafex_file_path = get_path(__file__, 'resources/test_extension_status_disabled.yafex')

        with patch('os.listdir') as mock_listdir, patch('os.path.abspath') as mock_abspath:
            mock_listdir.return_value = ['test_extension_status_disabled.yafex']
            mock_abspath.return_value = str(test_yafex_file_path)

            output = load_extensions("TEST_SERVICENAME")

            self.assertIsNotNone(output)
            self.assertIsInstance(output, list)
            self.assertTrue(len(output) == 0)

    def test_load_extensions_returns_empty_list_when_yafex_is_empty(self):
        '''
        Test to check if the function returns
        an empty list, when the yafex file
        is empty.
        '''
        test_yafex_file_path = get_path(__file__, 'resources/test_extension_empty.yafex')

        with patch('os.listdir') as mock_listdir, patch('os.path.abspath') as mock_abspath:
            mock_listdir.return_value = ['test_extension_empty.yafex']
            mock_abspath.return_value = str(test_yafex_file_path)

            output = load_extensions("TEST_SERVICENAME")

            self.assertIsNotNone(output)
            self.assertIsInstance(output, list)
            self.assertTrue(len(output) == 0)

    def test_load_extensions_returns_empty_list_when_name_in_yafex_is_empty(self):
        '''
        Test to check if the function returns
        an empty list, when the name in the
        yafex file is empty.
        '''
        test_yafex_file_path = get_path(__file__, 'resources/test_extension_empty_name.yafex')

        with patch('os.listdir') as mock_listdir, patch('os.path.abspath') as mock_abspath:
            mock_listdir.return_value = ['test_extension_empty_name.yafex']
            mock_abspath.return_value = str(test_yafex_file_path)

            output = load_extensions("TEST_SERVICENAME")

            self.assertIsNotNone(output)
            self.assertIsInstance(output, list)
            self.assertTrue(len(output) == 0)

    def test_load_extensions_returns_valid_extension_with_group_0_when_no_group_given(self):
        '''
        Test to check if the function returns
        a valid extension object, with 0 as
        the group value, when no group is
        given inside the yafex file.
        '''
        test_yafex_file_path = get_path(__file__, 'resources/test_extension_no_group.yafex')

        with patch('os.listdir') as mock_listdir, patch('os.path.abspath') as mock_abspath:
            mock_listdir.return_value = ['test_extension_no_group.yafex']
            mock_abspath.return_value = str(test_yafex_file_path)

            output = load_extensions("TEST_SERVICENAME")

            test_extension_object = output[0]
            test_name = test_extension_object.name
            test_field = test_extension_object.field
            test_report_field = test_extension_object.reportfield
            test_misp_type = test_extension_object.misptype
            test_pattern_args = test_extension_object.pattern_args
            test_group = test_extension_object.get_group()
            test_pattern = test_extension_object.get_pattern()
            test_hidden = test_extension_object.hidden

            self.assertIsNotNone(output)
            self.assertIsInstance(output, list)
            self.assertTrue(len(output) == 1)
            self.assertTrue(type(test_extension_object), 'Extension')
            self.assertIsNotNone(test_name)
            self.assertIsNotNone(test_field)
            self.assertIsNotNone(test_report_field)
            self.assertIsNotNone(test_misp_type)
            self.assertIsNotNone(test_pattern_args)
            self.assertIsNotNone(test_group)
            self.assertIsNotNone(test_pattern)
            self.assertIsNotNone(test_hidden)
            self.assertEqual(test_name, "TEST_NAME")
            self.assertEqual(test_field, "test_field")
            self.assertEqual(test_report_field, "Test Report Field")
            self.assertEqual(test_misp_type, "test_misp_type")
            self.assertEqual(test_pattern_args, 0)
            self.assertEqual(test_group, 0)
            self.assertEqual(test_pattern, re.compile('(AR[0-9]{2}-[0-9a-zA-Z]{4,5})'))
            self.assertEqual(test_hidden, True)

    def test_load_extensions_returns_valid_extension_with_group_0_when_no_group_is_not_int(self):
        '''
        Test to check if the function returns
        a valid extension object, with 0 as
        the group value, when the group type
        is not int.
        '''
        test_yafex_file_path = get_path(__file__, 'resources/test_extension_group_string.yafex')

        with patch('os.listdir') as mock_listdir, patch('os.path.abspath') as mock_abspath:
            mock_listdir.return_value = ['test_extension_group_string.yafex']
            mock_abspath.return_value = str(test_yafex_file_path)

            output = load_extensions("TEST_SERVICENAME")

            test_extension_object = output[0]
            test_name = test_extension_object.name
            test_field = test_extension_object.field
            test_report_field = test_extension_object.reportfield
            test_misp_type = test_extension_object.misptype
            test_pattern_args = test_extension_object.pattern_args
            test_group = test_extension_object.get_group()
            test_pattern = test_extension_object.get_pattern()
            test_hidden = test_extension_object.hidden

            self.assertIsNotNone(output)
            self.assertIsInstance(output, list)
            self.assertTrue(len(output) == 1)
            self.assertTrue(type(test_extension_object), 'Extension')
            self.assertIsNotNone(test_name)
            self.assertIsNotNone(test_field)
            self.assertIsNotNone(test_report_field)
            self.assertIsNotNone(test_misp_type)
            self.assertIsNotNone(test_pattern_args)
            self.assertIsNotNone(test_group)
            self.assertIsNotNone(test_pattern)
            self.assertIsNotNone(test_hidden)
            self.assertEqual(test_name, "TEST_NAME")
            self.assertEqual(test_field, "test_field")
            self.assertEqual(test_report_field, "Test Report Field")
            self.assertEqual(test_misp_type, "test_misp_type")
            self.assertEqual(test_pattern_args, 0)
            self.assertEqual(test_group, 0)
            self.assertEqual(test_pattern, re.compile('(AR[0-9]{2}-[0-9a-zA-Z]{4,5})'))
            self.assertEqual(test_hidden, True)

    def test_load_extensions_returns_valid_extension_with_hidden_False_when_no_hidden_given(self):
        '''
        Test to check if the function returns
        a valid extension object, with False
        as the hidden value, when no hidden
        is given inside the yafex file.
        '''
        test_yafex_file_path = get_path(__file__, 'resources/test_extension_no_hidden.yafex')

        with patch('os.listdir') as mock_listdir, patch('os.path.abspath') as mock_abspath:
            mock_listdir.return_value = ['test_extension_no_hidden.yafex']
            mock_abspath.return_value = str(test_yafex_file_path)

            output = load_extensions("TEST_SERVICENAME")

            test_extension_object = output[0]
            test_name = test_extension_object.name
            test_field = test_extension_object.field
            test_report_field = test_extension_object.reportfield
            test_misp_type = test_extension_object.misptype
            test_pattern_args = test_extension_object.pattern_args
            test_group = test_extension_object.get_group()
            test_pattern = test_extension_object.get_pattern()
            test_hidden = test_extension_object.hidden

            self.assertIsNotNone(output)
            self.assertIsInstance(output, list)
            self.assertTrue(len(output) == 1)
            self.assertTrue(type(test_extension_object), 'Extension')
            self.assertIsNotNone(test_name)
            self.assertIsNotNone(test_field)
            self.assertIsNotNone(test_report_field)
            self.assertIsNotNone(test_misp_type)
            self.assertIsNotNone(test_pattern_args)
            self.assertIsNotNone(test_group)
            self.assertIsNotNone(test_pattern)
            self.assertIsNotNone(test_hidden)
            self.assertEqual(test_name, "TEST_NAME")
            self.assertEqual(test_field, "test_field")
            self.assertEqual(test_report_field, "Test Report Field")
            self.assertEqual(test_misp_type, "test_misp_type")
            self.assertEqual(test_pattern_args, 0)
            self.assertEqual(test_group, 0)
            self.assertEqual(test_pattern, re.compile('(AR[0-9]{2}-[0-9a-zA-Z]{4,5})'))
            self.assertEqual(test_hidden, False)

    def test_load_extensions_returns_valid_extension_with_hidden_False_when_hidden_is_not_bool(self):
        '''
        Test to check if the function returns
        a valid extension object, with False as
        the hidden value, when the hidden type
        is not bool.
        '''
        test_yafex_file_path = get_path(__file__, 'resources/test_extension_hidden_string.yafex')

        with patch('os.listdir') as mock_listdir, patch('os.path.abspath') as mock_abspath:
            mock_listdir.return_value = ['test_extension_hidden_string.yafex']
            mock_abspath.return_value = str(test_yafex_file_path)

            output = load_extensions("TEST_SERVICENAME")

            test_extension_object = output[0]
            test_name = test_extension_object.name
            test_field = test_extension_object.field
            test_report_field = test_extension_object.reportfield
            test_misp_type = test_extension_object.misptype
            test_pattern_args = test_extension_object.pattern_args
            test_group = test_extension_object.get_group()
            test_pattern = test_extension_object.get_pattern()
            test_hidden = test_extension_object.hidden

            self.assertIsNotNone(output)
            self.assertIsInstance(output, list)
            self.assertTrue(len(output) == 1)
            self.assertTrue(type(test_extension_object), 'Extension')
            self.assertIsNotNone(test_name)
            self.assertIsNotNone(test_field)
            self.assertIsNotNone(test_report_field)
            self.assertIsNotNone(test_misp_type)
            self.assertIsNotNone(test_pattern_args)
            self.assertIsNotNone(test_group)
            self.assertIsNotNone(test_pattern)
            self.assertIsNotNone(test_hidden)
            self.assertEqual(test_name, "TEST_NAME")
            self.assertEqual(test_field, "test_field")
            self.assertEqual(test_report_field, "Test Report Field")
            self.assertEqual(test_misp_type, "test_misp_type")
            self.assertEqual(test_pattern_args, 0)
            self.assertEqual(test_group, 0)
            self.assertEqual(test_pattern, re.compile('(AR[0-9]{2}-[0-9a-zA-Z]{4,5})'))
            self.assertEqual(test_hidden, False)

    def test_load_extensions_returns_valid_extension_when_all_fields_are_set(self):
        '''
        Test to check if the function returns
        a valid extension object, when all
        fields are set properly.
        '''
        test_yafex_file_path = get_path(__file__, 'resources/test_extension_valid.yafex')

        with patch('os.listdir') as mock_listdir, patch('os.path.abspath') as mock_abspath:
            mock_listdir.return_value = ['test_extension_valid.yafex']
            mock_abspath.return_value = str(test_yafex_file_path)

            output = load_extensions("TEST_SERVICENAME")

            test_extension_object = output[0]
            test_name = test_extension_object.name
            test_field = test_extension_object.field
            test_report_field = test_extension_object.reportfield
            test_misp_type = test_extension_object.misptype
            test_pattern_args = test_extension_object.pattern_args
            test_group = test_extension_object.get_group()
            test_pattern = test_extension_object.get_pattern()
            test_hidden = test_extension_object.hidden

            self.assertIsNotNone(output)
            self.assertIsInstance(output, list)
            self.assertTrue(len(output) == 1)
            self.assertTrue(type(test_extension_object), 'Extension')
            self.assertIsNotNone(test_name)
            self.assertIsNotNone(test_field)
            self.assertIsNotNone(test_report_field)
            self.assertIsNotNone(test_misp_type)
            self.assertIsNotNone(test_pattern_args)
            self.assertIsNotNone(test_group)
            self.assertIsNotNone(test_pattern)
            self.assertIsNotNone(test_hidden)
            self.assertEqual(test_name, "TEST_NAME")
            self.assertEqual(test_field, "test_field")
            self.assertEqual(test_report_field, "Test Report Field")
            self.assertEqual(test_misp_type, "test_misp_type")
            self.assertEqual(test_pattern_args, 0)
            self.assertEqual(test_group, 0)
            self.assertEqual(test_pattern, re.compile('(AR[0-9]{2}-[0-9a-zA-Z]{4,5})'))
            self.assertEqual(test_hidden, True)

    def test_append_extensions_misp_types_returns_empty_dict_when_given_empty_dict_and_empty_list_as_parameter(self):
        '''
        Test to check if the function returns an empty dict
        when an empty dict and an empty list have been given
        as a parameter.
        '''
        test_dict = {}
        test_list = []

        output = append_extensions_misp_types(test_dict, test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 0)

    def test_append_extensions_misp_types_returns_valid_dict_when_given_empty_dict_as_parameter(self):
        '''
        Test to check if the function returns a valid dict
        when an empty dict has been given as a parameter.
        '''
        test_dict = {}
        test_extension = Extension("TEST_NAME", "TEST_FIELD", "TEST_PATTERN", "TEST_REPORTFIELD", "TEST_MISPTYPE", 0, 0, False)
        test_list = [test_extension]

        output = append_extensions_misp_types(test_dict, test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["TEST_REPORTFIELD"], str)
        self.assertIsNotNone(output["TEST_REPORTFIELD"])
        self.assertEqual(output["TEST_REPORTFIELD"], "TEST_MISPTYPE")

    def test_append_extensions_misp_types_returns_valid_dict_when_given_empty_list_as_parameter(self):
        '''
        Test to check if the function returns a valid dict
        when an empty list has been given as a parameter.
        '''
        test_dict = {
            "TEST_KEY": "TEST_VALUE",
        }
        test_list = []

        output = append_extensions_misp_types(test_dict, test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["TEST_KEY"], str)
        self.assertIsNotNone(output["TEST_KEY"])
        self.assertEqual(output["TEST_KEY"], "TEST_VALUE")

    def test_append_extensions_misp_types_throws_exception_when_None_as_dict_parameter(self):
        '''
        Test to check if the function throws an exception
        when None has been given as a dict parameter.
        '''
        test_extension = Extension("TEST_NAME", "TEST_FIELD", "TEST_PATTERN", "TEST_REPORTFIELD", "TEST_MISPTYPE", 0, 0, False)
        test_list = [test_extension]

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, append_extensions_misp_types(None, test_list, "TEST_SERVICENAME"))

    def test_append_extensions_misp_types_throws_exception_when_None_as_list_parameter(self):
        '''
        Test to check if the function throws an exception
        when None hass been given as a list parameter.
        '''
        test_dict = {
            "TEST_KEY": "TEST_VALUE",
        }

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, append_extensions_misp_types(test_dict, None, "TEST_SERVICENAME"))

    def test_append_extensions_misp_types_throws_exception_when_None_as_dict_and_list_parameter(self):
        '''
        Test to check if the function throws an exception
        when None hass been given as a dict and as a
        list parameter.
        '''

        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, append_extensions_misp_types(None, None, "TEST_SERVICENAME"))

    def test_append_extensions_misp_types_creates_new_key_value_pair_when_not_already_in_dict(self):
        '''
        Test to check if the function creates a new
        key value pair inside a dict, when the
        key value pair is not already in the given dict.
        '''
        test_dict = {
            "TEST_KEY": "TEST_VALUE",
        }
        test_extension = Extension("TEST_NAME", "TEST_FIELD", "TEST_PATTERN", "TEST_REPORTFIELD", "TEST_MISPTYPE", 0, 0, False)
        test_list = [test_extension]

        output = append_extensions_misp_types(test_dict, test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)
        self.assertIsInstance(output["TEST_KEY"], str)
        self.assertIsNotNone(output["TEST_KEY"])
        self.assertEqual(output["TEST_KEY"], "TEST_VALUE")
        self.assertIsInstance(output["TEST_REPORTFIELD"], str)
        self.assertIsNotNone(output["TEST_REPORTFIELD"])
        self.assertEqual(output["TEST_REPORTFIELD"], "TEST_MISPTYPE")

    def test_append_extensions_misp_types_creates_no_new_key_value_pair_when_already_in_dict(self):
        '''
        Test to check if the function does not
        create a new key value pair inside a dict,
        when the key value pair is already in the given dict.
        '''
        test_dict = {
            "TEST_KEY": "TEST_VALUE",
        }
        test_extension = Extension("TEST_NAME", "TEST_FIELD", "TEST_PATTERN", "TEST_KEY", "TEST_VALUE", 0, 0, False)
        test_list = [test_extension]

        output = append_extensions_misp_types(test_dict, test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["TEST_KEY"], str)
        self.assertIsNotNone(output["TEST_KEY"])
        self.assertEqual(output["TEST_KEY"], "TEST_VALUE")

    def test_append_extensions_misp_types_creates_no_new_value_for_existing_key(self):
        '''
        Test to check if the function does not
        create a new value for an already existing key.
        '''
        test_dict = {
            "TEST_KEY": "TEST_VALUE",
        }
        test_extension = Extension("TEST_NAME", "TEST_FIELD", "TEST_PATTERN", "TEST_KEY", "TEST_VALUE_NEW", 0, 0, False)
        test_list = [test_extension]

        output = append_extensions_misp_types(test_dict, test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 1)
        self.assertIsInstance(output["TEST_KEY"], str)
        self.assertIsNotNone(output["TEST_KEY"])
        self.assertEqual(output["TEST_KEY"], "TEST_VALUE")

    def test_append_extensions_misp_types_creates_new_key_value_pair_for_different_key_but_same_value(self):
        '''
        Test to check if the function creates
        a new key value pair for a different key,
        which has a already existing value.
        '''
        test_dict = {
            "TEST_KEY": "TEST_VALUE",
        }
        test_extension = Extension("TEST_NAME", "TEST_FIELD", "TEST_PATTERN", "TEST_KEY_NEW", "TEST_VALUE", 0, 0, False)
        test_list = [test_extension]

        output = append_extensions_misp_types(test_dict, test_list, "TEST_SERVICENAME")

        self.assertIsNotNone(output)
        self.assertIsInstance(output, dict)
        self.assertTrue(len(output) == 2)
        self.assertIsInstance(output["TEST_KEY"], str)
        self.assertIsNotNone(output["TEST_KEY"])
        self.assertEqual(output["TEST_KEY"], "TEST_VALUE")
        self.assertIsInstance(output["TEST_KEY_NEW"], str)
        self.assertIsNotNone(output["TEST_KEY_NEW"])
        self.assertEqual(output["TEST_KEY_NEW"], "TEST_VALUE")