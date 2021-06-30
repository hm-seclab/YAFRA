'''
Generate a markdown file from json/dict input.
'''

from libs.markdown.cleaner import remove_tabs_and_spaces_front
import os
import json

from collections import Counter

from mdutils.mdutils import MdUtils

from libs.kafka.logging import LogMessage
from libs.countrycodes.iso_hanlder import convert_alpha_2_to_alpha_3
from libs.countrycodes.iso_hanlder import convert_alpha_2_to_qualified_name

from .gl_structure import BAR_WEBSITE_TYPES_SCHEMA
from .gl_structure import CVE_HEATMAP
from .gl_structure import PIEC_SCHEMA


def generate_adsense_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the adsense-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'google_adsense_publisher_ids' in findings.keys() and len(findings['google_adsense_publisher_ids']) > 0:
            markdownfile.new_header(level=2, title='Adsense publisher-ids')
            markdownfile.new_list(items=findings['google_adsense_publisher_ids'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_ganalytics_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the google analystics-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'google_analytics_tracker_ids' in findings.keys() and len(findings['google_analytics_tracker_ids']) > 0:
            markdownfile.new_header(level=2, title='Analytics-tracker-ids')
            markdownfile.new_list(items=findings['google_analytics_tracker_ids'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_google_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the google-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        section_keys = ['google_analytics_tracker_ids', 'google_adsense_publisher_ids']
        if any([(element in section_keys and len(findings[str(element)]) > 0) for element in findings.keys()]):
            markdownfile.new_header(level=1, title='Google')
            generate_ganalytics_section(markdownfile, findings, servicename)
            generate_adsense_section(markdownfile, findings, servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_useragents_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the useragents-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'user_agents' in findings.keys() and len(findings['user_agents']) > 0:
            markdownfile.new_header(level=2, title='User-agents')
            markdownfile.new_list(items=findings['user_agents'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_registry_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the registery-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'registry_key_paths' in findings.keys() and len(findings['registry_key_paths']) > 0:
            markdownfile.new_header(level=2, title='Registry Keys')
            markdownfile.new_list(items=findings['registry_key_paths'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_filepaths_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the filepaths-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'file_paths' in findings.keys() and len(findings['file_paths']) > 0:
            markdownfile.new_header(level=2, title='Filepaths')
            markdownfile.new_list(items=remove_tabs_and_spaces_front(findings['file_paths']))
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_misc_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the misc-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        section_keys = ['file_paths', 'registry_key_paths', 'user_agents']
        if any([(element in section_keys and len(findings[str(element)]) > 0) for element in findings.keys()]):
            markdownfile.new_header(level=1, title='Misc')
            generate_filepaths_section(markdownfile, findings, servicename)
            generate_registry_section(markdownfile, findings, servicename)
            generate_useragents_section(markdownfile, findings, servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_monero_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the monero-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'monero_addresses' in findings.keys() and len(findings['monero_addresses']) > 0:
            markdownfile.new_header(level=2, title='Monero')
            markdownfile.new_list(items=findings['monero_addresses'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_bitcoin_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the authentihashes-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'bitcoin_addresses' in findings.keys() and len(findings['bitcoin_addresses']) > 0:
            markdownfile.new_header(level=2, title='Bitcoin')
            markdownfile.new_list(items=findings['bitcoin_addresses'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_wallets_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the wallets-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        section_keys = ['bitcoin_addresses', 'monero_addresses']
        if any([(element in section_keys and len(findings[str(element)]) > 0) for element in findings.keys()]):
            markdownfile.new_header(level=1, title='Crypto-Wallets')
            generate_bitcoin_section(markdownfile, findings, servicename)
            generate_monero_section(markdownfile, findings, servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_imphashes_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the imphashes-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'imphashes' in findings.keys() and len(findings['imphashes']) > 0:
            markdownfile.new_header(level=2, title='Imphashes')
            markdownfile.new_list(items=findings['imphashes'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_authentihashes_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the authentihashes-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'authentihashes' in findings.keys() and len(findings['authentihashes']) > 0:
            markdownfile.new_header(level=2, title='Auth hashes')
            markdownfile.new_list(items=findings['authentihashes'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_md5_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the md5-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'md5s' in findings.keys() and len(findings['md5s']) > 0:
            markdownfile.new_header(level=2, title='MD5')
            generate_simple_table(markdownfile, findings, 'md5s', 'md5', 'MD5', servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_sha512_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the sha512-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'sha512s' in findings.keys() and len(findings['sha512s']) > 0:
            markdownfile.new_header(level=2, title='SHA-512')
            generate_simple_table(markdownfile, findings, 'sha512s', 'SHA-512', 'SHA512', servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_ssdeeps_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the ssdeeps-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'ssdeeps' in findings.keys() and len(findings['ssdeeps']) > 0:
            markdownfile.new_header(level=2, title='SSDeeps')
            markdownfile.new_list(items=findings['ssdeeps'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_sha256_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the sha256-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'sha256s' in findings.keys() and len(findings['sha256s']) > 0:
            markdownfile.new_header(level=2, title='SHA-256')
            generate_simple_table(markdownfile, findings, 'sha256s', 'SHA-256', 'SHA256', servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_sha1_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the sha1-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'sha1s' in findings.keys() and len(findings['sha1s']) > 0:
            markdownfile.new_header(level=2, title='SHA-1')
            generate_simple_table(markdownfile, findings, 'sha1s', 'SHA-1', 'SHA1', servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_hashes_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the hashes-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        section_keys = ['sha1s', 'sha256s', 'sha512s', 'md5s', 'ssdeeps', 'authentihashes', 'imphashes']
        if any([(element in section_keys and len(findings[str(element)]) > 0) for element in findings.keys()]):
            markdownfile.new_header(level=1, title='File hashes')
            generate_sha1_section(markdownfile, findings, servicename)
            generate_sha256_section(markdownfile, findings, servicename)
            generate_sha512_section(markdownfile, findings, servicename)
            generate_ssdeeps_section(markdownfile, findings, servicename)
            generate_authentihashes_section(markdownfile, findings, servicename)
            generate_md5_section(markdownfile, findings, servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_n_mac_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the mac-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'mac_addresses' in findings.keys() and len(findings['mac_addresses']) > 0:
            markdownfile.new_header(level=2, title='MAC address')
            markdownfile.new_list(items=findings['mac_addresses'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_n_ipv6_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the ipv6-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'ipv6s' in findings.keys() and len(findings['ipv6s']) > 0:
            markdownfile.new_header(level=3, title='IPv6-Address')
            markdownfile.new_list(items=findings['ipv6s'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_n_cidrs_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the cidrs-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'ipv4_cidrs' in findings.keys() and len(findings['ipv4_cidrs']) > 0:
            markdownfile.new_header(level=3, title='IPv4-CIDRS')
            markdownfile.new_list(items=findings['ipv4_cidrs'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_n_ipv4_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the ipv4-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'ipv4' in findings.keys() and len(findings['ipv4']) > 0:
            markdownfile.new_header(level=3, title='IPv4-Address')
            fields = ["IP", "Country", "ASN", "Detected files", "Undetected files", "Related Events"]
            n_colums = len(fields)
            n_rows = len(findings['ipv4']) + 1
            for entry in findings['ipv4']:
                fields.extend([
                    str(entry),
                    convert_alpha_2_to_alpha_3(str(findings['ipv4'][entry]['Country']), servicename),
                    str(findings['ipv4'][entry]['ASN']) if findings['ipv4'][entry]['ASN'] is not None else "#",
                    str(findings['ipv4'][entry]['Detected_files']),
                    str(findings['ipv4'][entry]['Undetected_files']),
                    str(findings['ipv4'][entry]['misp']) if len(findings['ipv4'][entry]['misp']) > 0 else "#",
                ])
            markdownfile.new_line()
            markdownfile.new_table(columns=n_colums, rows=n_rows, text=fields, text_align='center')
            markdownfile.new_paragraph()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_n_ips_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the ip-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        section_keys = ['ipv4', 'ipv4_cidrs', 'ipv6s', 'mac_addresses']
        if any([(element in section_keys and len(findings[str(element)]) > 0) for element in findings.keys()]):
            markdownfile.new_header(level=2, title='IPv4 and IPv6')
            generate_n_ipv4_section(markdownfile, findings, servicename)
            generate_n_cidrs_section(markdownfile, findings, servicename)
            generate_n_ipv6_section(markdownfile, findings, servicename)
            generate_n_mac_section(markdownfile, findings, servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()


def generate_n_domains_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the domains-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'domains' in findings.keys() and len(findings['domains']) > 0:
            markdownfile.new_header(level=2, title='Domains')
            fields = ["Domain", "Categories", "Vendor", "Detected files", "Undetected files", "Related Events"]
            n_colums = len(fields)
            n_rows = len(findings['domains']) + 1
            for entry in findings['domains']:
                fields.extend([
                    str(entry),
                    str(findings['domains'][entry]['Categories']),
                    str(findings['domains'][entry]['Vendor']),
                    str(findings['domains'][entry]['Detected_files']),
                    str(findings['domains'][entry]['Undetected_files']),
                    str(findings['domains'][entry]['misp']) if len(findings['domains'][entry]['misp']) > 0 else "#",
                ])
            markdownfile.new_line()
            markdownfile.new_table(columns=n_colums, rows=n_rows, text=fields, text_align='center')
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_n_email_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the email-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'email_addresses' in findings.keys() and len(findings['email_addresses']) > 0:
            markdownfile.new_header(level=2, title='Emails')
            generate_simple_table(markdownfile, findings, 'email_addresses', 'email', 'Emails', servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_n_url_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the url-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'urls' in findings.keys() and len(findings['urls']) > 0:
            markdownfile.new_header(level=2, title='URLs')
            fields = ["URL", "Related Events"]
            n_colums = len(fields)
            n_rows = len(findings['urls']) + 1
            for entry in findings['urls']:
                fields.extend([
                    str(entry['url']),
                    str(entry['misp']) if entry['misp'] != "" else "#",
                ])
            markdownfile.new_line()
            markdownfile.new_table(columns=n_colums, rows=n_rows, text=fields, text_align='center')
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_n_ans_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the ans-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'asns' in findings.keys() and len(findings['asns']) > 0:
            markdownfile.new_header(level=2, title='Autonomous system')
            markdownfile.new_list(items=findings['asns'])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_network_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the tlp-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        section_keys = ['asns', 'urls', 'email_addresses', 'domains', 'ipv4_cidrs', 'ipv6s', 'ipv4', 'mac_addresses']
        if any([(element in section_keys and len(findings[str(element)]) > 0) for element in findings.keys()]):
            markdownfile.new_header(level=1, title='Network')
            generate_n_ans_section(markdownfile, findings, servicename)
            generate_n_url_section(markdownfile, findings, servicename)
            generate_n_email_section(markdownfile, findings, servicename)
            generate_n_domains_section(markdownfile, findings, servicename)
            generate_n_ips_section(markdownfile, findings, servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_cve_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the cve-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'cve' in findings.keys() and len(findings['cve']) > 0:
            markdownfile.new_header(level=1, title='CVEs')
            for entry in findings['cve']:
                markdownfile.new_header(level=2, title="{}".format(str(entry)))
                fields = ['CVE', 'CVS-Score', 'Complexity', 'Vektor', "Related Events"]
                fields.extend([
                        str(entry),
                        str(findings['cve'][entry]['CVS-Score']),
                        str(findings['cve'][entry]['Complexity']),
                        str(findings['cve'][entry]['Vektor']),
                        str(findings['cve'][entry]['misp']) if len(findings['cve'][entry]['misp']) > 0 else "#",
                    ])
                markdownfile.new_table(columns=5, rows=2, text=fields, text_align='center')
                markdownfile.new_line()
                markdownfile.new_paragraph("**Summary**: {}".format(findings['cve'][entry]['Summary']))
                markdownfile.new_paragraph("**Mitre-CVE**: https://cve.mitre.org/cgi-bin/cvename.cgi?name={}".format(entry))
                markdownfile.new_paragraph("**ExploitDB**: {}".format(findings['cve'][entry]['Exploit-DB']))
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_mitre_ent_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the mitre-enterprise-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try: #TODO Split
        if 'Enterprice_tactics' in findings.keys() and len(findings['Enterprice_tactics']) > 0:
            markdownfile.new_header(level=3, title='Mitre tactics')
            markdownfile.new_paragraph("For more information about Mitre Att&ck Tactics. Link: https://attack.mitre.org/tactics/enterprise/")
            fields = ['Tactic-ID', 'Title', 'Mitre link', 'More Info']
            for entry in findings['Enterprice_tactics']:
                lower_link_title = (str(findings['Enterprice_tactics'][entry]['Title']).replace(" ", "-")).lower()
                fields.extend([
                    str(entry),
                    str(findings['Enterprice_tactics'][entry]['Title']),
                    str(findings['Enterprice_tactics'][entry]['Mitre_Link']),
                    str('''<a target="_blank" href="Mitre/enterprise_tactics.md#{}-{}">More</a>'''.format(str(entry).replace(".", "").lower(), lower_link_title))
                ])
            markdownfile.new_table(columns=4, rows=len(findings['Enterprice_tactics'])+1, text=fields, text_align='center')
            markdownfile.new_paragraph()
        if 'Enterprice_techniques' in findings.keys() and len(findings['Enterprice_techniques']) > 0:
            markdownfile.new_header(level=3, title='Mitre techniques')
            markdownfile.new_paragraph("For more information about Mitre Att&ck Techniques. Link: https://attack.mitre.org/techniques/enterprise/")
            fields = ['Technique-ID', 'Title', 'Mitre link', 'More Info']
            for entry in findings['Enterprice_techniques']:
                lower_link_title = (str(findings['Enterprice_techniques'][entry]['Title']).replace(" ", "-")).lower()
                fields.extend([
                    str(entry),
                    str(findings['Enterprice_techniques'][entry]['Title']),
                    str(findings['Enterprice_techniques'][entry]['Mitre_Link']),
                    str('''<a target="_blank" href="Mitre/enterprise_techniques.md#{}-{}">More</a>'''.format(str(entry).replace(".", "").lower(), lower_link_title))
                ])
            markdownfile.new_table(columns=4, rows=len(findings['Enterprice_techniques'])+1, text=fields, text_align='center')
            markdownfile.new_paragraph()  
            markdownfile.new_paragraph()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_mitre_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the mirte-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        section_keys = ['Enterprice_tactics', 'Enterprice_techniques']
        if any([(element in section_keys and len(findings[str(element)]) > 0) for element in findings.keys()]):
            markdownfile.new_header(level=1, title='Mitre Att&ck')
            markdownfile.new_header(level=2, title='Enterprise tactics and techniques')
            generate_mitre_ent_section(markdownfile, findings, servicename)
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_tlp_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the tlp-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'tlp_labels' in findings.keys() and len(findings['tlp_labels']) > 0:
            markdownfile.new_header(level=1, title='Traffic Light Protocol')
            markdownfile.new_paragraph("Information in this report is considered to be **{}**, regarding to the TLP.".format(findings['tlp_labels'][0]))
            markdownfile.new_paragraph("For more information: https://www.cisa.gov/tlp")
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_overview_table(markdownfile, findings, extensionnames, servicename):
    try:
        fields = ['TLP', 'IPv4s', 'Domains', 'Emails', 'URLs', 'CVEs', 'YARA', 'Extensions', 'Tactics (ENTP)', 'Techniques (ENTP)']
        f_keys = findings.keys()
        ext = list(filter(lambda x: x != False, [(k in findings.keys() and len(findings[k]) > 0) for k in extensionnames.keys()]))
        table = [
            str(findings['tlp_labels'][0]) if 'tlp_labels' in f_keys and len(findings['tlp_labels']) > 0 else "#",
            str(len(findings['ipv4'])) if 'ipv4' in f_keys and len(findings['ipv4']) > 0 else "0",
            str(len(findings['domains'])) if 'domains' in f_keys and len(findings['domains']) > 0 else "0",
            str(len(findings['email_addresses'])) if 'email_addresses' in f_keys and len(findings['email_addresses']) > 0 else "0",
            str(len(findings['urls'])) if 'urls' in f_keys and len(findings['urls']) > 0 else "0",
            str(len(findings['cve'])) if 'cve' in f_keys and len(findings['cve']) > 0 else "0",
            "Yes" if 'yara_rules' in f_keys and len(findings['yara_rules']) > 0 else "No",
            str(len(ext)) if ext is not None and len(ext) > 0 else "0",
            str(len(findings['Enterprice_tactics'])) if 'Enterprice_tactics' in f_keys and len(findings['Enterprice_tactics']) > 0 else "0",
            str(len(findings['Enterprice_techniques'])) if 'Enterprice_techniques' in f_keys and len(findings['Enterprice_techniques']) > 0 else "0",
        ]
        fields.extend(table)
        markdownfile.new_table(columns=10, rows=2, text=fields, text_align='center')
        markdownfile.new_line()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_overview_section(markdownfile, findings, filename, extensionnames, servicename):
    '''
    generate_overview_section will generate the overview-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try: #TODO split
        markdownfile.new_header(level=1, title='Overview')
        markdownfile.new_paragraph(
            "This report contain the information about the warning from **{}**.".format(filename)
        )
        generate_overview_table(markdownfile, findings, extensionnames, servicename)
        if 'ipv4' in findings.keys() and (ipv4adds := findings['ipv4']) is not None and len(ipv4adds) > 0:
            markdownfile.new_header(level=2, title='Involved states')
            markdownfile.new_paragraph("The graph below shows all countrys involved in the incident (Based on the active ips).")
            local_schema = PIEC_SCHEMA
            counts = Counter(findings['ipv4'][elem]['Country'] for elem in findings['ipv4'])
            state_apperence = [{"State": convert_alpha_2_to_qualified_name(state, servicename) if state is not None else "Unknown", "value": amount} for state, amount in dict(counts).items()]
            local_schema['data']['values'] = state_apperence
            markdownfile.insert_code(json.dumps(local_schema), language="vegalite")
        if 'domains' in findings.keys() and (domains := findings['domains']) is not None and len(domains) > 0:
            markdownfile.new_header(level=2, title='Hosttypes')
            markdownfile.new_paragraph("The graph below displays all categories of host interacting in this incident.")
            local_schema = BAR_WEBSITE_TYPES_SCHEMA
            counts = Counter(findings['domains'][elem]['Categories'] for elem in findings['domains'])
            web_apperence = [{"Websitetypes": wtype[:20] if wtype is not None else "Unknown", "Amount": amount} for wtype, amount in dict(counts).items()]
            local_schema['data']['values'] = web_apperence
            markdownfile.insert_code(json.dumps(local_schema), language="vegalite")
        if 'cve' in findings.keys() and (domains := findings['cve']) is not None and len(domains) > 0:
            markdownfile.new_header(level=2, title='CVSS-Heatmap')
            markdownfile.new_paragraph("The graph below illustrates a CVE-Score-Complexity heatmap for a visuell riskassessment.")
            local_schema = CVE_HEATMAP
            counts = Counter((findings['cve'][elem]['CVS-Score'], findings['cve'][elem]['Complexity']) for elem in findings['cve'])
            cve_heat = [{"SCORE": score[0] if score is not None and len(score) == 2 else 0, "APPEAR": appear, "COMPLX": score[1]} for score, appear in dict(counts).items()]
            local_schema['data']['values'] = cve_heat
            markdownfile.insert_code(json.dumps(local_schema), language="vegalite")
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_extensions_section(markdownfile, findings, extensionnames, servicename):
    '''
    generate_extensions_section will generate the extensions section.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param extensionnames will be a list with the names of the extensions.
    @param servicename will be the name of the service.
    '''
    try:
        if any([(k in findings.keys() and len(findings[k]) > 0) for k in extensionnames.keys()]):
            markdownfile.new_header(level=1, title='Extensions')
            for json_name, report_name in extensionnames.items():
                if isinstance(findings[json_name], list) and len(findings[json_name]) > 0:
                    markdownfile.new_header(level=2, title=report_name)
                    markdownfile.new_list(items=findings[json_name])
                if isinstance(findings[json_name], str):
                    markdownfile.new_paragraph(findings[json_name])
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_yara_section(markdownfile, findings, servicename):
    '''
    generate_overview_section will generate the tlp-section of a report.
    @param markdownfile will be a handle to the makedown-object.
    @param findings will be all ico's and data as json/dict.
    @param filename will be the name of the input file
    @param servicename will be the name of the service.
    '''
    try:
        if 'yara_rules' in findings.keys() and len(findings['yara_rules']) > 0:
            markdownfile.new_header(level=1, title='YARA Rules')
            for rule, rule_index in zip(findings['yara_rules'], range(len(findings['yara_rules']))):
                markdownfile.new_header(level=2, title='Rule-{}'.format(rule_index+1))
                markdownfile.insert_code(rule, language="php")
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_mitre_enterprise_tac_files(filename, findings, servicename):
    try:
        filename = "mitre_enter_tac_"+filename
        if 'Enterprice_tactics' in findings.keys() and len(findings['Enterprice_tactics']) > 0:
            markdownfile = MdUtils(file_name=filename, title='{}'.format(filename))
            markdownfile.new_header(level=1, title='Mitre tactics (Enterprise)')
            markdownfile.new_paragraph("For more information about Mitre Att&ck Tactics. Link: https://attack.mitre.org/tactics/enterprise/")
            for entry in findings['Enterprice_tactics']:
                markdownfile.new_header(level=2, title="{}-{}".format(entry, findings['Enterprice_tactics'][entry]['Title']))
                markdownfile.new_paragraph("**Summary**: {}".format(findings['Enterprice_tactics'][entry]['Summary']))
                markdownfile.new_paragraph("**Mitre**: {}".format(findings['Enterprice_tactics'][entry]['Mitre_Link']))
                markdownfile.new_paragraph()
            markdownfile.new_table_of_contents(table_title='Table of tactics', depth=2)
            in_memory_markdown_file = markdownfile.create_md_file()

            tac_f_markdown_file = in_memory_markdown_file.read_file(filename)
            os.remove(filename + ".md")
            return tac_f_markdown_file
        return None
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_enterprise_apt_section(entry, findings, markdownfile, servicename):
    try:
        rows = len(findings['Enterprice_techniques'][entry]['APTs']) + 1
        fields = ['APT', 'Name', 'Mitre-Link']
        for apt in findings['Enterprice_techniques'][entry]['APTs']:
            fields.extend([
                str(apt['ID']),
                str(apt['Name']),
                str(apt['Link']),
            ])
        markdownfile.new_table(columns=3, rows=rows, text=fields, text_align='center')
        markdownfile.new_line()
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_mitre_enterprise_tech_files(filename, findings, servicename):
    try:
        filename = "mitre_enter_tech_"+filename
        if 'Enterprice_techniques' in findings.keys() and len(findings['Enterprice_techniques']) > 0:
            markdownfile = MdUtils(file_name=filename, title='{}'.format(filename))
            markdownfile.new_header(level=1, title='Mitre techniques (Enterprise)')
            markdownfile.new_paragraph("For more information about Mitre Att&ck Techniques. Link: https://attack.mitre.org/techniques/enterprise/")
            for entry in findings['Enterprice_techniques']:
                markdownfile.new_header(level=2, title="{}-{}".format(entry, findings['Enterprice_techniques'][entry]['Title']))
                markdownfile.new_paragraph("**Summary**: {}".format(findings['Enterprice_techniques'][entry]['Summary']))
                markdownfile.new_paragraph()
                markdownfile.new_paragraph("**Detection**: {}".format(findings['Enterprice_techniques'][entry]['Detections']))
                markdownfile.new_paragraph()
                markdownfile.new_paragraph("**Mitre**: {}".format(findings['Enterprice_techniques'][entry]['Mitre_Link']))
                if len(findings['Enterprice_techniques'][entry]['APTs']) > 0:
                    generate_enterprise_apt_section(entry, findings, markdownfile, servicename)
            markdownfile.new_table_of_contents(table_title='Table of tactics', depth=2)
            in_memory_markdown_file = markdownfile.create_md_file()

            tech_f_markdown_file = in_memory_markdown_file.read_file(filename)
            os.remove(filename + ".md")
            return tech_f_markdown_file
        return None
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

def generate_simple_table(markdownfile, findings, findings_key, object_key, table_title,  servicename):
    '''
    generate_simple_table will generate a simple table with 2 by x elements for tables with just one
        element and a related_event field, like md5.
    @param markdownfile will be the file to append
    @param findings will be the findingsobject
    @param findings_key will be the key of the findings-section
    @param object_key will be the name of the field in the object
    @param table_title will be the name of the table column
    @param servicename will be the name of the calling service.
    '''
    try:
        fields = [table_title, "Related Events"]
        n_colums = len(fields)
        n_rows = len(findings[findings_key]) + 1
        for entry in findings[findings_key]:
            fields.extend([
                        str(entry[object_key]),
                        str(entry['misp']) if len(entry['misp']) > 0 else "#"
                    ])
        markdownfile.new_line()
        markdownfile.new_table(columns=n_colums, rows=n_rows, text=fields, text_align='center')
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()

# List of functionpointers.
generators = [
    generate_mitre_section,
    generate_cve_section,
    generate_network_section,
    generate_hashes_section,
    generate_misc_section,
    generate_wallets_section,
    generate_google_section,
    generate_yara_section
]

def generate_markdown_file(findings, extensionnames, servicename):
    '''
    generate_markdown_file will generate a markdown file from
        given findings in json/dict format.
    @param findings will be a json/dict with findings.
    @param servicename will be the name of the calling-service.
    @param extensionnames will be a dict in the format {'json_field_name': 'report_heading'}
    @return a markdown-file as string.
    '''
    try:
        filename = findings['input_filename']
        markdownfile = MdUtils(file_name=filename, title='{}'.format(filename))
        generate_overview_section(markdownfile, findings, filename, extensionnames, servicename)
        for entry in generators:
            entry(markdownfile, findings, servicename)
        if extensionnames is not None and isinstance(extensionnames, dict) and len(extensionnames) > 0:
            generate_extensions_section(markdownfile, findings, extensionnames, servicename)

        markdownfile.new_table_of_contents(table_title='Table of content', depth=4)
        in_memory_markdown_file = markdownfile.create_md_file()

        f_markdown_file = in_memory_markdown_file.read_file(filename)
        os.remove(filename + ".md")

        enter_tac_file = generate_mitre_enterprise_tac_files(filename, findings, servicename)
        enter_tech_file = generate_mitre_enterprise_tech_files(filename, findings, servicename)

        return f_markdown_file, {"enterprise_tactics": enter_tac_file, "enterprise_techniques": enter_tech_file}
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
        return "Cannot generate a report for file. {}".format(filename)
