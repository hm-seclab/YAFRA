'''
This script contains a transpiler from markdown to json.
'''

import re
import json

from markdown_tree_parser.parser import parse_string

from libs.kafka.logging import LogMessage

rules = [
    ("#", ""),
    ("*", ""),
    ("\n\n", " "),
    (" Summary: ", ""),
    ("\nSummary: ", ""),
]

rules_after = [
    ("\n", ""),
    ("- ", ""),
    (" - ", "")
]

re_rules = [
    ("list", re.compile("((\n){0,1}-\s{1,3}(.*)(\n){0,1})")),
    ("dict", re.compile("((\n){0,1}\|(.*)\|(\n){0,1})"))
]


def handle_objects_in_markdown(string, applied_rules, servicename):
    '''
    handle_objects_in_markdown will handle everything beyond a the
        string, int or list type.
    @param string will be the input data
    @param applied_rules will be all machting rules
    @return a list of objects.
    '''
    temp_string = string
    try:
        md_objects = ([((inst.replace("\n", "")).replace("|", ",")).split(",") for inst in applied_rules])
        for rep in applied_rules:
            temp_string = temp_string.replace(rep, "")
        keys = list(filter(lambda x: x != "" and not ":---:" in x, md_objects[0]))
        md_objects[0] = []
        md_objects = list(filter(lambda x: len(x) > 1, md_objects))
        md_objects = list(map(lambda y: list(filter(lambda x: x != "" and not ":---:" in x, y)), md_objects))
        string = [dict(zip(keys, instance)) for instance in md_objects] if len(md_objects) > 0 else None
        if temp_string is not None and temp_string != "" and re.search('[a-zA-Z]{3,}', temp_string) is not None:
            string.append({"text": temp_string})
        string = list(filter(lambda x: len(x) > 0, string))
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return string

def apply_post_rules(string, servicename):
    '''
    apply_post_rules will apply some rules to the string
        in order to make the result of previous processing
        steps better.
    @param string will be the input string to apply some
        rules on.
    @return will return a string.
    '''
    try:
        for i in rules_after:
            string = [element.replace(i[0], i[1]) for element in string]
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return string

def apply_prep_rules(string, servicename):
    '''
    apply_prep_rules will apply some rules to the string
        in order to provide a better processing in the
        next steps.
    @param string will be the input string to apply some
        rules on.
    @return will return a string.
    '''
    try:
        for i in rules:
            string = string.replace(i[0], i[1])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return string

def apply_transformation_rules(string, servicename):
    '''
    apply_transformation_rules will change a given string by
        predefinied rules.
    @param string will be the input string.
    @return will be the changed string.
    '''
    try:
        string = apply_prep_rules(string, servicename)
        for i in re_rules:
            if (temp := [x[0] for x in re.findall(i[1], str(string))]) is not None and len(temp) > 0:
                if i[0] == "list":
                    string = apply_post_rules(temp, servicename)
                elif i[0] == "dict":
                    string = handle_objects_in_markdown(string, temp, servicename)
                else:
                    continue
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return string

def traverse(inp, elements={}, servicename=""):
    '''
    traverse will traverse recursively over a given Markdown-AST
        and turn it into JSON.
    @param inp will be the AST.
    @param elements will be a list (empty) to put in the top level
        headers as dictionary.
    '''
    try:
        for element in inp:
            if element.children is not None and len(element.children):
                elements[str(element.text)] = traverse(element.children, {}, servicename)
            else:
                elements[str(element.text)] = apply_transformation_rules(str(element.source), servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return elements

def convert_markdown_to_json(filecontent, filename, servicename):
    '''
    convert_markdown_to_json will convert a given markdown-file into
        a JSON-Serialized-Object.
    @param filecontent will be the content of the file/markdown to
        parse and convert.
    @return will return a json-object.
    '''
    json_data = None
    try:
        disallowed_sections = ['Overview', 'Table of content', 'Mitre Att&ck']
        file_content = parse_string(filecontent)
        file_content = list(filter(lambda x: x.text not in disallowed_sections, file_content.children))
        data = {"data": traverse(file_content, {}, servicename), "Eventname": filename}
        if data is not None and len(data) > 0:
            json_data = json.dumps(data, indent=4, sort_keys=True)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return json_data
