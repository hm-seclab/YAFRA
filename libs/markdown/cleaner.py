'''
This script contains function to clean findings.
'''

def remove_tabs_and_spaces_front(strings):
    '''
    remove_tabs_and_spaces_front will remove spaces and tabs at
        the start and end of string.
    @return a list of strings.
    '''
    try:
        strings = list(map(lambda string: str(string).strip("\t"), strings))
        strings = list(map(lambda string: str(string).strip(" "), strings))
        return strings
    except Exception as error:
        print(error)
        return strings

def clear_yara_start_and_end(strings):
    '''
    remove chars from gitlab at the start and end of the yara rule.
    @return a list of strings with yara rules.
    '''
    try:
        strings = list(map(lambda string: str(string).strip("```php"), strings))
        strings = list(map(lambda string: str(string).rstrip("```"), strings))
        return strings
    except Exception as error:
        print(error)
        return strings
