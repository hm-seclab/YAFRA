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

SERVICENAME = envvar("SERVICENAME", "Scraper")
KAFKA_SERVER = envvar("KAFKA_SERVER", "0.0.0.0:9092")
HEALTHTOPIC = envvar("HEALTH_TOPIC", "health_report")
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
    def some_methods():
        #TODO write some code here.
        pass

    def __call__(self, app, *args, **kwargs):
        '''
        __call__ override __call__ function from server-class.
        '''
        scheduler.start()
        #Thread(target=Reporter.consume_reports, daemon=True).start()
        return Server.__call__(self, app, *args, **kwargs)