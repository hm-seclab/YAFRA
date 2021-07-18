'''
This class will represent the iocpusher-server.
'''

# pylint: disable=C0413, C0411

import sys
import time
import json
import datetime
import random
import pytz
import gitlab
sys.path.append('..')

from threading import Thread

from libs.core.environment import envvar
from libs.kafka.logging import LogMessage
from libs.kafka.logging import send_health_message
from libs.gitlabl.repository import create_repository_if_not_exists
from libs.gitlabl.repository import create_monthly_if_not_exists
from libs.gitlabl.repository import get_branch_name
from libs.gitlabl.repository import get_projectid_by_name
from libs.gitlabl.issues import create_issues
from libs.cve.cve_information import get_cve_information
from libs.virustotal.domains import get_vt_information_domains
from libs.virustotal.ips import get_vt_information_ipv4
from libs.mitre.enterprise import get_mitre_information_tactics_enterpise
from libs.mitre.enterprise import get_mitre_information_techniques_enterpise
from libs.markdown.generator import generate_markdown_file
from libs.extensions.loader import load_extensions
from libs.extensions.loader import generate_dict_with_jsonfield_and_reportfield
from libs.misp.search import get_appearance_in_misp

from pyattck import Attck

from pymisp import PyMISP

from kafka.consumer import KafkaConsumer

from flask import Flask
from flask_script import Server
from flask_apscheduler import APScheduler

# ENVIRONMENT-VARS
SERVICENAME = envvar("SERVICENAME", "Pusher")
IOC_TOPIC_NAME = envvar("IOC_TOPIC", "ioc")
KAFKA_SERVER = envvar("KAFKA_SERVER", "0.0.0.0:9092")
HEALTHTOPIC = envvar("HEALTH_TOPIC", "health_report")
GITLAB_SERVER = envvar("GITLAB_SERVER", "http://0.0.0.0:10082")
GITLAB_TOKEN = envvar("GITLAB_TOKEN", "NOTWORKING")
GITLAB_REPO_NAME = envvar("GITLAB_REPO_NAME", "IOCFindings")
VT_API_KEY = envvar("VIRUS_TOTAL", "None")
MISP_SERVER = envvar("MISP_SERVER", "0.0.0.0")
MISP_TOKEN = envvar("MISP_TOKEN", None)
MISP_CERT_VERIFY = True if envvar("MISP_VERIF", True) == "True" else False
GITLAB_CERT_VERIFY = True if envvar("GITLAB_VERIF", str(True)).lower() in ("yes", "y", "true", "1", "t") else False

class Config:
    '''
    Config class with configs for flask.
    '''
    SCHEDULER_API_ENABLED = True

app = Flask(SERVICENAME)
app.config.from_object(Config())

scheduler = APScheduler()
scheduler.init_app(app)

def flaskapp():
    '''
    flaskapp will return the FLASK_APP.
    @return a flask_app
    '''
    return app

class Pusher(Server):
    '''
    Pusher will be the server/microservice which will take data
        from KAFKA, enrich the data, generate a markdown report
        and push it to gitlab.
    '''

    @staticmethod
    def get_repository_handle(): #TODO move to lib
        '''

        '''
        try:
            gitlab_instance = gitlab.Gitlab(GITLAB_SERVER, GITLAB_TOKEN, ssl_verify=GITLAB_CERT_VERIFY)
            projectid = get_projectid_by_name(gitlab_instance, GITLAB_REPO_NAME, SERVICENAME)
            gprojects = gitlab_instance.projects.get(projectid)
            return gprojects
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
            return None

    EXTENSIONS = list(filter(lambda ext: ext.in_report(), load_extensions(SERVICENAME)))
    PUSHER_THREAD = None
    BACKOFF_TIMER = 5
    TIME_SINCE_EXCEPTION = None
    GPROJECT = None

    @staticmethod
    def add_misp_appearance(findings, improved_findings):
        '''
        enrich the found iocs with misp information, atleast some of them.
        @param findings will a be an object with all findings.
        @param improved_findings will be all allready enriched findings by
            things like virus_total or circl.lu
        @return dict with merged findings.
        '''
        enriched = improved_findings
        try:
            misp_handle = PyMISP(MISP_SERVER, MISP_TOKEN, MISP_CERT_VERIFY, 'json')
            key_type = {
                "urls": "url",
                "md5s": "md5",
                "sha256s": "SHA-256",
                "sha1s": "SHA-1",
                "sha512s": "SHA-512",
                "email_addresses": "email"
            }
            for find_key, k_type in key_type.items():
                if (elements := findings[str(find_key)]) is not None and len(elements) > 0:
                    enriched[find_key] = [{str(k_type): element, "misp": get_appearance_in_misp(misp_handle, element, SERVICENAME)} for element in elements]
            if (domains_details := improved_findings['domains']) is not None and len(domains_details) > 0:
                for key, value in domains_details.items(): improved_findings['domains'][key] = {**value, "misp": get_appearance_in_misp(misp_handle, key, SERVICENAME)}
            if (ipv4_details := improved_findings['ipv4']) is not None and len(ipv4_details) > 0:
                for key, value in ipv4_details.items(): improved_findings['ipv4'][key] = {**value, "misp": get_appearance_in_misp(misp_handle, key, SERVICENAME)}
            if (cve_details := improved_findings['cve']) is not None and len(cve_details) > 0:   
                for key, value in cve_details.items(): improved_findings['cve'][key] = {**value, "misp": get_appearance_in_misp(misp_handle, key, SERVICENAME)}
            enriched = {
                **improved_findings,
                **enriched
            }
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
        return enriched

    @staticmethod
    def generate_improved_findings(findings):
        '''
        generate_improved_findings will generate more data about cve\'s,
            ipv4\'s, domain\'s and mitre tactic\'s and technique\'s.
        @param findings will be a set of findings in dict format.
        @return a dict with more data about the finding.s
        '''
        improved_findings = {}
        finding_keys = findings.keys() if findings is not None else {}
        try:
            cve_details, ipv4_details, domains_details, m_e_tactics, m_e_techniques = {}, {}, {}, {}, {}
            if 'cves' in finding_keys and (cves := findings['cves']) is not None and len(cves) > 0:
                cve_details = get_cve_information(cves, SERVICENAME)
            if 'ipv4s' in finding_keys and (ipv4s := findings['ipv4s']) is not None and len(ipv4s) > 0:
                ipv4_details = get_vt_information_ipv4(VT_API_KEY, ipv4s, SERVICENAME)
            if 'domains' in finding_keys and (domains := findings['domains']) is not None and len(domains) > 0:
                domains_details = get_vt_information_domains(VT_API_KEY, domains, SERVICENAME)
            if 'attack_tactics' in finding_keys and (mitre_attack_tac_ent := findings['attack_tactics']['enterprise']) is not None and len(mitre_attack_tac_ent) > 0:
                m_e_tactics = get_mitre_information_tactics_enterpise(mitre_attack_tac_ent, SERVICENAME)
            if 'attack_techniques' in finding_keys and (mitre_attack_tech_ent := findings['attack_techniques']['enterprise']) is not None and len(mitre_attack_tech_ent) > 0:
                m_e_techniques = get_mitre_information_techniques_enterpise(mitre_attack_tech_ent, SERVICENAME)
            improved_findings = {
                "cve": cve_details,
                "ipv4": ipv4_details,
                "domains": domains_details,
                "Enterprice_tactics": m_e_tactics,
                "Enterprice_techniques": m_e_techniques,
            }
            improved_findings = Pusher.add_misp_appearance(findings, improved_findings)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
        return improved_findings

    @scheduler.task("interval", id="health_push", seconds=5, timezone=pytz.UTC)
    def healthpush():
        '''
        healthpush will send a health message to KAFKA.
        '''
        try:
            send_health_message(KAFKA_SERVER, HEALTHTOPIC, SERVICENAME)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def generate_markdown(findings):
        '''
        generate_markdown will generate improved findings by calling
            generate_improved_findings and combine the improved data
            with parts of the inital data. After all a markdown-file
            will be generated from the data.
        @param findings will should be all findings in json/dict-format.
        @return a markdown-file as string.
        '''
        try:
            improved_findings = Pusher.generate_improved_findings(findings)
            forbidden_keys = ['ipv4s', 'domains', 'attack_techniques', 'attack_tactics', 'cves', 'phone_numbers', 'registry_key_paths', "email_addresses", 'urls', 'sha256s', 'sha512s', 'sha1s', 'md5s']
            for key, value in findings.items():
                if key not in forbidden_keys:
                    improved_findings[key] = value
            dict_for_extensions = generate_dict_with_jsonfield_and_reportfield(Pusher.EXTENSIONS, SERVICENAME)
            markdown, mitre_files = generate_markdown_file(improved_findings, dict_for_extensions, SERVICENAME)
            return markdown, mitre_files, improved_findings
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
            return findings

    @staticmethod
    def create_markdown(findings, report_name):
        '''
        create_markdown will generate from findings a markdownfile and
            put it in gitlab as a report.
        @param findings will be all findings in json/dict-format.
        @return a dict as json for gitlab.
        '''
        data = {}
        try:
            markdown, mitre_files, _ = Pusher.generate_markdown(findings)
            data = {
                'branch': report_name,
                'commit_message': 'Commited a report: {}'.format(report_name),
                'actions': [
                        {
                            'action': 'create',
                            'file_path': '{}/report.md'.format(report_name),
                            'content': str(markdown)
                        }
                    ]
                }
            if 'yara_rules' in findings.keys() and len(findings['yara_rules']) > 0:
                for rule, index in zip(findings['yara_rules'], range(len(findings['yara_rules']))):
                    data['actions'].append({
                        'action': 'create',
                        'file_path': '{0}/Yara_rules/{0}_rule_{1}.yar'.format(report_name, index+1),
                        'content': str(rule)
                    })
            if mitre_files is not None and len(mitre_files) > 0:
                for filename, content in mitre_files.items():
                    if content is not None:
                        data['actions'].append({
                            'action': 'create',
                            'file_path': '{0}/Mitre/{1}.md'.format(report_name, filename),
                            'content': str(content)
                        })
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
        return data

    @scheduler.task("cron", id="execute", year='*', month='*', timezone=pytz.UTC)
    def create_monthly_branch():
        '''
        create_monthly_branch will create everyday a new branch
            in the format IoC-[CurrentMonth]-[CurrentYear].
        '''
        try:
            create_monthly_if_not_exists(gitlabserver=GITLAB_SERVER, token=GITLAB_TOKEN, repository=GITLAB_REPO_NAME, servicename=SERVICENAME)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def submit_report(findings):
        '''
        submit_report will submit the pull-request into the
            IoC-[CurrentDate]-Branch.
        @param findings will be all findings in json/dict formtat.
        '''
        try:
            findings = json.loads(findings.value.decode("utf-8"))
            report_name = findings['input_filename'] if 'input_filename' in findings.keys() else random.randint(4, 10000)
            Pusher.GPROJECT.branches.create({'branch': report_name, 'ref': get_branch_name()})
            data = Pusher.create_markdown(findings, report_name)
            _ = Pusher.GPROJECT.commits.create(data)
            create_issues(  gitlabserver=GITLAB_SERVER,
                            token=GITLAB_TOKEN,
                            repository=GITLAB_REPO_NAME,
                            servicename=SERVICENAME,
                            title=report_name,
                            description="A report has been submitted. The name of the branch is: {}.".format(report_name))
        except gitlab.gitlab.GitlabCreateError as gc_error:
            LogMessage(str(gc_error), LogMessage.LogTyp.INFO, SERVICENAME).log()
        except Exception as error:
            if 'response_code' in dir(error) and (error.response_code == 500 or error.response_code == 502):
                Pusher.BACKOFF_TIMER += 15
                Pusher.TIME_SINCE_EXCEPTION = datetime.datetime.now()
                Pusher.GPROJECT = Pusher.get_repository_handle()
                Pusher.submit_report(findings)
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def consume_findings():
        '''
        consume_findings will consume all findings from KAFKA and
            push them into the gitlab repository.
        '''
        try:
            consumer = KafkaConsumer(IOC_TOPIC_NAME, bootstrap_servers=KAFKA_SERVER, client_id='ioc_pusher', api_version=(2, 7, 0),)
            for report in consumer:
                Thread(target=Pusher.submit_report, args=(report,), daemon=True).start()
                time.sleep(Pusher.BACKOFF_TIMER)
        except Exception as error:
            if 'response_code' in dir(error) and (error.response_code == 500 or error.response_code == 502):
                Pusher.GPROJECT = Pusher.get_repository_handle()
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    @scheduler.task("interval", id="clear_timer", minutes=2, timezone=pytz.UTC)
    def clear_backoff_timer():
        '''
        clear_backoff_timer will check the last time a exception occurred.
            In case it is more than 5 minutes it will clear the timer and
            set it back to 5 seconds.
        '''
        difference = 0
        try:
            current_time = datetime.datetime.now()
            if Pusher.TIME_SINCE_EXCEPTION is not None:
                difference = current_time - Pusher.TIME_SINCE_EXCEPTION
                difference = difference.seconds // 60 % 60
            if Pusher.BACKOFF_TIMER > 5 and difference >= 5:
                LogMessage("Reseting the backoff time for the pusher", LogMessage.LogTyp.ERROR, SERVICENAME).log()
                Pusher.BACKOFF_TIMER = 5
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    @scheduler.task("interval", id="health_push", minutes=2, timezone=pytz.UTC)
    def recover_pusher_thread():
        '''
        recover_pusher_thread will check every 2 minutes whether the pusher thread is still alive or not.
            In Case it is not a new thread will be created and started.
        '''
        try:
            if Pusher.PUSHER_THREAD is None or not Pusher.PUSHER_THREAD.is_alive():
                Pusher.PUSHER_THREAD = Thread(target=Pusher.consume_findings, daemon=True).start()
                LogMessage("Recovering the pusher thread", LogMessage.LogTyp.INFO, SERVICENAME).log()
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    def __call__(self, app, *args, **kwargs):
        '''
        __call__ override __call__ function from server-class.
        '''
        attack = Attck(nested_subtechniques=False)
        attack.update()
        create_repository_if_not_exists(gitlabserver=GITLAB_SERVER, token=GITLAB_TOKEN, repository=GITLAB_REPO_NAME, servicename=SERVICENAME)
        Pusher.PUSHER_THREAD = Thread(target=Pusher.consume_findings, daemon=True).start()
        Pusher.GPROJECT = Pusher.get_repository_handle()
        Pusher.create_monthly_branch()
        scheduler.start()
        return Server.__call__(self, app, *args, **kwargs)
