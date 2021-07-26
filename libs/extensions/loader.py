'''
Extentionloader will load all active extentions
'''

import os
import re
import yaml

from libs.kafka.logging import LogMessage

class Extension():
    '''
    Extension will be a class representing a YAFRA-Extension.
    '''

    def __init__(self, name, field, pattern, reportfield, misptype, pattern_args=0, group=0, not_in_report=False):
        '''
        CTor of the Extensions-class.
        '''
        self.name = name
        self.field = field
        self.pattern = pattern
        self.misptype = misptype
        self.reportfield = reportfield
        self.pattern_args = pattern_args
        self.group = group
        self.hidden =  not_in_report

    def get_pattern(self):
        '''
        get_pattern will return a compiled regex with flags.
        '''
        try:
            return re.compile(self.pattern, self.pattern_args)
        except Exception:
            return self.pattern

    def get_group(self):
        '''
        get_group will return an int value which contains the group for the regex.
        '''
        try:
            return self.group
        except Exception:
            return 0   

    def in_report(self):
        '''
        return a boolean if the extension should be in the report or not.
        '''
        try:
            return not self.hidden
        except Exception:
            return True           

def generate_dict_with_jsonfield_and_reportfield(extensions, servicename):
    '''
    generate_dict_with_jsonfield_and_reportfield will return a dict with
        json_field_names and report_field_names.
    @param extensions will be a list of extensions.
    @return a dict with {json_field_names, report_field_names}.
    '''
    dict_j_r = {}
    try:
        for ext in extensions:
            if type(ext) is not Extension:
                continue
            dict_j_r[ext.field] = ext.reportfield
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return dict_j_r

def load_extensions(servicename):
    '''
    load_extentions will load all extensions for the extensions-folder.
    @param servicename will be the name of the calling service.
    @return a list of extension-objects.
    '''
    extensions = []
    try:
        for ext in list(filter(lambda x: x.endswith("yafex"), os.listdir("../extensions"))):
            try:
                docker_filep = os.path.abspath(os.path.join("../extensions", ext))
                with open(docker_filep) as file:
                    data = yaml.load(file, Loader=yaml.FullLoader)
                    if data is None:
                        continue
                    if 'Status' not in data or data['Status'] is None or type(data['Status']) is not str:
                        continue
                    if data['Status'] == "enabled":
                        if 'Name' not in data or data['Name'] is None or type(data['Name']) is not str:
                            continue
                        if 'Field' not in data or data['Field'] is None or type(data['Field']) is not str:
                            continue
                        if 'Pattern' not in data or data['Pattern'] is None or type(data['Pattern']) is not str:
                            continue
                        if 'Reportfield' not in data or data['Reportfield'] is None or type(data['Reportfield']) is not str:
                            continue
                        if 'MISPType' not in data or data['MISPType'] is None or type(data['MISPType']) is not str:
                            continue
                        if 'PatternArgs' not in data or data['PatternArgs'] is None or type(data['PatternArgs']) is not int:
                            continue
                        group = int(data['Group']) if 'Group' in data and data['Group'] is not None and type(data['Group']) is int else 0
                        hidden = bool(data['Hidden']) if 'Hidden' in data and data['Hidden'] is not None and type(data['Hidden']) is bool else False
                        extensions.append(Extension(str(data['Name']), str(data['Field']), str(data['Pattern']), str(data['Reportfield']), str(data['MISPType']), data['PatternArgs'], group, hidden))
            except Exception as error:
                LogMessage(str("Extension {} can not be loaded properly.".format(ext)), LogMessage.LogTyp.WARNING, servicename).log()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return extensions


def append_extensions_misp_types(ctypes, lextensions, servicename):
    '''
    append_extensions_misp_types will add all misp-types from the
        extensions into the currentlist of types.
    @param ctypes will be a dict with all currently available types.
    @param lextensions will be a list of extensions.
    @return a dict with all reportnames (K) and misp types (V).
    '''
    try:
        for extension in lextensions:
            if extension.reportfield not in ctypes.keys():
                ctypes[extension.reportfield] = extension.misptype
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
    return ctypes
