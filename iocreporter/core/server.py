'''
This class will represent the reporter-server.
'''

# pylint: disable=C0413, C0411

import sys
import json
import pytz
sys.path.append('..')

from threading import Thread

from pymisp import PyMISP

from kafka.consumer import KafkaConsumer

from flask import Flask
from flask_script import Server
from flask_apscheduler import APScheduler

from libs.core.environment import envvar
from libs.kafka.logging import LogMessage
from libs.kafka.logging import send_health_message
from libs.misp.event import handle_misp_event

SERVICENAME = envvar("SERVICENAME", "Reporter")
KAFKA_SERVER = envvar("KAFKA_SERVER", "0.0.0.0:9092")
HEALTHTOPIC = envvar("HEALTH_TOPIC", "health_report")
REPORT_TOPIC = envvar("REPORT_TOPIC", "rfreport")
MISP_SERVER = envvar("MISP_SERVER", "0.0.0.0")
MISP_TOKEN = envvar("MISP_TOKEN", None)
MISP_CERT_VERIFY = True if envvar("MISP_VERIF", True) == "True" else False

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

class Reporter(Server):
    '''
    Reporter will be a class representing the reporter-service.
    '''

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
    def push_misp_report(report):
        '''
        push_misp_report will send the misp report to the misp-platfrom.
        '''
        try:
            report = json.loads(report.value.decode('UTF-8'))
            misp_connection = PyMISP(MISP_SERVER, MISP_TOKEN, MISP_CERT_VERIFY)
            handle_misp_event(misp_connection, report, SERVICENAME)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @staticmethod
    def consume_reports():
        '''
        consume_reports will consume all available reports from KAFKA
            and push the results to the MISP-Plattform.
        '''
        try:
            consumer = KafkaConsumer(REPORT_TOPIC, bootstrap_servers=KAFKA_SERVER, client_id='ioc_reporter', api_version=(2,7,0),)
            for report in consumer:
                Thread(target=Reporter.push_misp_report, args=(report,), daemon=True).start()
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    def __call__(self, app, *args, **kwargs):
        '''
        __call__ override __call__ function from server-class.
        '''
        scheduler.start()
        Thread(target=Reporter.consume_reports, daemon=True).start()
        return Server.__call__(self, app, *args, **kwargs)
