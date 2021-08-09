'''
Server-Class for the extractions of IoC's.
'''

# pylint: disable=C0413, C0411

import os
import sys
import json
import pytz
import re
import iocextract as ioce

sys.path.append('..')

from io import StringIO
from threading import Thread

from kafka.producer import KafkaProducer
from kafka.consumer import KafkaConsumer

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from ioc_finder import find_iocs

from flask import Flask
from flask import request
from flask import render_template
from flask_script import Server
from flask_apscheduler import APScheduler
from flask_dropzone import Dropzone

from libs.core.filter import filter_dict_values
from libs.core.filter import filter_by_blacklist
from libs.core.merge_dicts import merge_dicts
from libs.core.environment import envvar
from libs.kafka.topichandler import create_topic_if_not_exists
from libs.kafka.logging import LogMessage
from libs.kafka.logging import send_health_message
from libs.extensions.loader import load_extensions
from libs.gitlabl.files import read_file_from_gitlab
from libs.gitlabl.sanitize_title import sanitize_title
import traceback
# ENVIRONMENT-VARS
SERVICENAME = envvar("SERVICENAME", "Extractor")
IOC_TOPIC_NAME = envvar("IOC_TOPIC", "ioc")
SCRAPER_TOPIC_NAME = envvar("SCRAPER_TOPIC", "datascraper")
KAFKA_SERVER = envvar("KAFKA_SERVER", "0.0.0.0:9092")
HEALTHTOPIC = envvar("HEALTH_TOPIC", "health_report")
GITLAB_SERVER = envvar("GITLAB_SERVER", "0.0.0.0:10082")
GITLAB_TOKEN = envvar("GITLAB_TOKEN", "NOTWORKING")
GITLAB_REPO_NAME = envvar("GITLAB_REPO_NAME", "IOCFindings")

DOCKER_REPORTS_PATH = "/app/iocextractor/reports"


class Config:
    '''
    Config class with configs for flask.
    '''
    SCHEDULER_API_ENABLED = True


app = Flask(SERVICENAME, template_folder='templates', static_folder="static/", static_url_path='/static')
app.config.from_object(Config())
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = '.pdf'
app.config['DROPZONE_MAX_FILE_SIZE'] = 10
app.config['DROPZONE_MAX_FILES'] = 100
app.config['UPLOADED_PATH'] = os.path.join(DOCKER_REPORTS_PATH, 'uploads')

dropzone = Dropzone(app)

scheduler = APScheduler()
scheduler.init_app(app)


def flaskapp():
    '''
    flaskapp will return the FLASK_APP.
    @return a flask_app
    '''
    return app


class Extractor(Server):
    '''
    Extractor will be the class for the extractor-server.
    '''

    EXTENSIONS = load_extensions(SERVICENAME)
    BLACKLIST = {}

    @app.route('/', methods=['GET', 'POST'])
    def file_dropzone():
        '''
        file_dropzone will render a drag and drop view for the reports.
        @return a rendered template.
        '''
        if request.method == 'POST':
            files = request.files.get('file')
            file_path = os.path.join(DOCKER_REPORTS_PATH, files.filename)
            files.save(file_path)
        return render_template('index.html')

    @staticmethod
    @scheduler.task("interval", id="refetch", seconds=30, timezone=pytz.UTC)
    def refetch_blacklist():
        '''
        refetch_blacklist will fetch the blacklist from the master every 30 minutes.
        '''
        content = {}
        try:
            if Extractor.BLACKLIST is None or len(Extractor.BLACKLIST) <= 0:
                LogMessage("Using local blacklist.", LogMessage.LogTyp.INFO, SERVICENAME).log()
                with open(os.path.abspath("../datasets/blacklist.json")) as content:
                    content = json.load(content)
            else:
                LogMessage("Using blacklist from gitlab.", LogMessage.LogTyp.INFO, SERVICENAME).log()
                content = read_file_from_gitlab(gitlabserver=GITLAB_SERVER, token=GITLAB_TOKEN, repository=GITLAB_REPO_NAME, file="blacklist.json", servicename=SERVICENAME, branch_name="master")
                content = json.loads(content)
            if content is not None:
                Extractor.BLACKLIST = content
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def pushfindings(findings):
        '''
        pushfindings will push all findings to KAFKA.
        @param findings will be the findings.
        '''
        try:
            producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, client_id='ioc_extractor', api_version=(2, 7, 0))
            message = str(json.dumps(findings)).encode('UTF-8')
            producer.send(IOC_TOPIC_NAME, message)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def extensions(string):
        '''
        extensions will execute extensions for this server.
        @param string will be the string to check against.
        @return findings in the string machting the extensions-rules.
        '''
        findings = {}
        try:
            for i in Extractor.EXTENSIONS:
                try:
                    l_findings = re.findall(i.get_pattern(), string)
                    if len(l_findings) > 0 and isinstance(l_findings[0], tuple):
                        findings[str(i.field)] = [
                            element[i.get_group()] if len(element) - 1 >= i.get_group() else element.group(0) for
                            element in l_findings]
                    else:
                        findings[str(i.field)] = l_findings
                except Exception as error:
                    LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
        return findings

    def extract_ioc(pdftext):
        '''
        extract_ioc will extract ioc from a given text all ioc.
        @param pdftext will be the text to search trough.
        @return will return a dictonary with all icos or an empty
            dict incase of no ioc or an error.
        '''
        iocs = {}
        try:
            iocs = find_iocs(pdftext)
            yara_rules = [rule for rule in ioce.extract_yara_rules(pdftext)]
            iocs['yara_rules'] = yara_rules
            ex_ioc = Extractor.extensions(pdftext)
            iocs = merge_dicts(iocs, filter_dict_values(ex_ioc, SERVICENAME), SERVICENAME)
            iocs = filter_by_blacklist(iocs, Extractor.BLACKLIST, SERVICENAME)
        except Exception as error:
            LogMessage(f"{str(error)} {''.join(traceback.format_tb(error.__traceback__))}", LogMessage.LogTyp.ERROR, SERVICENAME).log()
        return iocs

    @staticmethod
    def extract(reportpath):
        '''
        extract will take a PDF-File as path and try to extract all IoC's. After the
            Extraction, the file will be removed. The IoC's will be pushed to KAFKA
            by calling the pushfindings-Function.
        @param reportpath will be the path to the PDF-File.
        '''
        try:
            pdf_content = StringIO()
            LogMessage(f"Extract ioc's from file: {reportpath}", LogMessage.LogTyp.INFO, SERVICENAME).log()
            with open(reportpath, 'rb') as file:
                resource_manager = PDFResourceManager()
                device = TextConverter(resource_manager, pdf_content, laparams=LAParams())
                interpreter = PDFPageInterpreter(resource_manager, device)
                for page in PDFPage.create_pages(PDFDocument(PDFParser(file))):
                    interpreter.process_page(page)
            pdftext = pdf_content.getvalue()
            iocs = Extractor.extract_ioc(pdftext)
            input_filename = sanitize_title(unsanitized_title=str((os.path.basename(reportpath))), servicename=SERVICENAME)
            iocs['input_filename'] = input_filename
            Extractor.pushfindings(iocs)
            os.remove(reportpath)
            LogMessage(f"The ioc's had been extracted from the file and the file has been removed: {reportpath}", LogMessage.LogTyp.INFO, SERVICENAME).log()
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

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
    def handle_scraper_feed(data):
        '''
        handle_scraper_feed take the data from scraper
            and extract all ioc and push the result to
            KAFKA for the ioc pusher.
        @param data will be the data from KAFKA.
        '''
        try:
            if (json_data := json.loads(data.value.decode("utf-8"))) is not None:
                iocs = Extractor.extract_ioc(json_data.get('content'))
                input_filename = sanitize_title(unsanitized_title=str(json_data.get('title')), servicename=SERVICENAME)
                iocs['input_filename'] = input_filename
                Extractor.pushfindings(iocs)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def consume_findings_from_scraper():
        '''
        consume_findings_from_scraper will consume all findings from KAFKA and
            push them into the gitlab repository.
        '''
        try:
            consumer = KafkaConsumer(SCRAPER_TOPIC_NAME, bootstrap_servers=KAFKA_SERVER, client_id='ioc_extractor',
                                     api_version=(2, 7, 0), )
            for report in consumer:
                Thread(target=Extractor.handle_scraper_feed, args=(report,), daemon=True).start()
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @scheduler.task("interval", id="execute", seconds=10, timezone=pytz.UTC, misfire_grace_time=900)
    def execute():
        '''
        execute will run the service and search for PDF's and start for every file a
            thread. The thread will execute the extract-Function and extract all IoC's
            in a file.
        '''
        try:
            if (reports := os.listdir(DOCKER_REPORTS_PATH)) is not None and len(reports) > 0:
                threads = []
                for report in reports:
                    if report.endswith(".pdf"):
                        threads.append(
                            Thread(target=Extractor.extract, args=(os.path.join(DOCKER_REPORTS_PATH, report),)))
                for instance in threads:
                    instance.start()
                for instance in threads:
                    instance.join()
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    def __call__(self, app, *args, **kwargs):
        '''
        __call__ will be executed befor the server creation and run some functions
            on startup. So a Topic will be create for the IoC's and the scheduler
            will be started for the cron-jobs.
        @param self is the Server-Object.
        @param app will be the app passed to the __call__ function of the server-class
        @param *args and **kwargs will be the vargs passed to the __call__ function
            of the server-class
        '''
        create_topic_if_not_exists(KAFKA_SERVER, IOC_TOPIC_NAME, SERVICENAME)
        Extractor.BLACKLIST = Extractor.refetch_blacklist()
        scheduler.start()
        Thread(target=Extractor.consume_findings_from_scraper, daemon=True).start()
        return Server.__call__(self, app, *args, **kwargs)
