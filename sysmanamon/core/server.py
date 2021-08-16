'''
The actual server-class for systemmanagement and -monitoring service.
'''

import sys
import json
sys.path.append('..')

from threading import Thread

from flask import Flask
from flask import jsonify
from flask import make_response
from flask import render_template

from flask_script import Server

from kafka.consumer import KafkaConsumer

from libs.kafka.logging import LogMessage
from libs.kafka.topichandler import create_topic_if_not_exists
from libs.core.environment import envvar

SERVICENAME = envvar("SERVICENAME", "Systemmanagement and monitoring")
LOGGING_TOPIC_NAME = envvar("LOGGER_TOPIC", "logging")
# nosec
KAFKA_SERVER = envvar("KAFKA_SERVER", "0.0.0.0:9092")
HEALTHTOPIC = envvar("HEALTH_TOPIC", "health")

app = Flask(SERVICENAME, template_folder='core/templates', static_folder="core/static", static_url_path='/static')
app.config['TEMPLATES_AUTO_RELOAD'] = True #TODO raus in production

def flaskapp():
    return app

class Sysmonserver(Server):

    LOGMESSAGES = []
    HEALTHMESSAGES = []

    @app.route('/ping')
    def ping_test():
        '''
        ping_test will send a ping in case a request comes in.
        '''
        return make_response(jsonify({"Message": "Ping"}), 200)

    @app.route('/')
    def index():
        '''
        index will return the root page.
        '''
        try:
            return render_template("index.html")
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
            return make_response(jsonify({"Message": "Cannot render index.html"}), 200)

    @staticmethod
    def consume_logging_messages():
        '''
        consume_logging_messages will consume the log messages from the kafka topic.
        '''
        try:
            consumer = KafkaConsumer(LOGGING_TOPIC_NAME, bootstrap_servers=KAFKA_SERVER, client_id='sysmon', api_version=(2, 7, 0),)
            for report in consumer:
                value = report.value.decode("utf-8")
                value = json.loads(value)
                Sysmonserver.LOGMESSAGES.append(value)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @app.route('/logs')
    def log_message_endpoint():
        '''
        log_message_endpoint will serve the log message endpoint.
        '''
        try:
            reports = Sysmonserver.LOGMESSAGES
            Sysmonserver.LOGMESSAGES = []
            return make_response(jsonify(reports), 200 if len(reports) > 0 else 204)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
            return make_response(jsonify({"Message": "Unknown error on the client side"}), 400)

    @staticmethod
    def consume_health_messages():
        '''
        consume_health_messages will consume the health messages from the kafka topic.
        '''
        try:
            consumer = KafkaConsumer(HEALTHTOPIC, bootstrap_servers=KAFKA_SERVER, client_id='sysmon', api_version=(2, 7, 0),)
            for report in consumer:
                value = report.value.decode("utf-8")
                value = json.loads(value)
                Sysmonserver.HEALTHMESSAGES.append(value)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()

    @app.route('/health')
    def health_status_endpoint():
        '''
        health_status_endpoint will serve the health status endpoint.
        '''
        try:
            reports = Sysmonserver.HEALTHMESSAGES
            if len(reports) > 0: reports = reports[:8]
            Sysmonserver.HEALTHMESSAGES = []
            return make_response(jsonify(reports), 200 if len(reports) > 0 else 204)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
            return make_response(jsonify({"Message": "Unknown error on the client side"}), 400)

    def application_setup(self):
        '''
        application_setup will initat all needed things for the server.
        @param self will be Sysmonserver-object. 
        '''
        try:
            create_topic_if_not_exists(KAFKA_SERVER, LOGGING_TOPIC_NAME)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
    
    def __call__(self, app, *args, **kwargs):
        self.application_setup()
        Thread(target=Sysmonserver.consume_logging_messages, daemon=True).start()
        Thread(target=Sysmonserver.consume_health_messages, daemon=True).start()
        return Server.__call__(self, app, *args, **kwargs)