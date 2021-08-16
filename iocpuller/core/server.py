'''
This class will represent the puller-server.
'''

# pylint: disable=C0413, C0411

import sys
import json
import pytz

sys.path.append('..')

from datetime import datetime

from kafka.consumer import KafkaConsumer
from kafka.producer import KafkaProducer

from libs.core.environment import envvar
from libs.gitlabl.files import read_file_from_gitlab
from libs.gitlabl.commit import get_filename_since_last_timestamp
from libs.gitlabl.commit import get_latest_commit_hash_by_branch
from libs.gitlabl.pull_requests import get_list_of_relevant_prs
from libs.gitlabl.pull_requests import merge_pull_request
from libs.gitlabl.repository import get_branch_name
from libs.kafka.topichandler import create_topic_if_not_exists
from libs.kafka.logging import LogMessage
from libs.kafka.logging import send_health_message
from libs.markdown.converter import convert_markdown_to_json

from flask import Flask
from flask_script import Server
from flask_apscheduler import APScheduler

SERVICENAME = envvar("SERVICENAME", "Puller")
# nosec
KAFKA_SERVER = envvar("KAFKA_SERVER", "0.0.0.0:9092")
KAFKA_REPORT_TOPIC = envvar("REPORT_TOPIC", "rfreport")
KAFKA_TIMESTAMP_TOPIC = envvar("TIMESTAMP_TOPIC", "committstamps")
HEALTHTOPIC = envvar("HEALTH_TOPIC", "health_report")
# nosec
GITLAB_SERVER = envvar("GITLAB_SERVER", "0.0.0.0:10082")
GITLAB_TOKEN = envvar("GITLAB_TOKEN", "NOTWORKING")
GITLAB_REPO_NAME = envvar("GITLAB_REPO_NAME", "IOCFindings")

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

class Puller(Server):
    '''
    Class for the Puller-Server.
    '''

    @staticmethod
    def commit_timestamp(commit_hash, time, branch_name):
        '''
        commit_timestamp will send a timestamp to KAFKA so it can be accessed
            at any time.
        @param commit_hash will be the hash value of the commit.
        @param time will be a datetime object with the timestamp
        @param branch_name will be the branch_name of the last timestamp.
        @return will return a timestamp-object.
        '''
        timestamp = None
        try:
            timestamp = json.dumps({"commit_hash": commit_hash, "time": time, "branch_name": branch_name}).encode("UTF-8")
            producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, client_id='ioc_puller', api_version=(2,7,0))
            producer.send(KAFKA_TIMESTAMP_TOPIC, timestamp)
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
        return timestamp

    @staticmethod
    def latest_timestamp():
        '''
        latest_timestamp will return the latest timestamp from the KAFKA
            topic.
        @return a timestamp as a dict with the fields: branch_name,
            commit_hash, time.
        '''
        v_last_timestamp = None
        try:
            consumer = KafkaConsumer(KAFKA_TIMESTAMP_TOPIC,
                bootstrap_servers=KAFKA_SERVER,
                client_id='ioc_puller',
                api_version=(2, 7, 0),
                auto_offset_reset='earliest',
                enable_auto_commit=False,
                consumer_timeout_ms=5000)
            if (messages := [message for message in consumer]) is not None and len(messages) > 0: #TODO R1721
                v_last_timestamp = (messages[-1]).value.decode('UTF-8')
        except Exception as error:
            LogMessage(str(error), LogMessage.LogTyp.ERROR, SERVICENAME).log()
        return v_last_timestamp

    @scheduler.task("interval", id="execute", seconds=30, timezone=pytz.UTC, misfire_grace_time=900)
    def execute():
        '''
        execute will merge all pull-request an fetch the new data in order to send it into the
            KAFKA for the reporter-service.
        '''
        branch_name = get_branch_name()
        latest_timestamp = None
        try:
            if (latest_timestamp := Puller.latest_timestamp()) is None:
                latest_timestamp = Puller.commit_timestamp(
                    get_latest_commit_hash_by_branch(gitlabserver=GITLAB_SERVER, token=GITLAB_TOKEN, repository=GITLAB_REPO_NAME, branch=branch_name, servicename=SERVICENAME),
                    datetime.now().isoformat(), get_branch_name()
                )
            prs = get_list_of_relevant_prs(GITLAB_SERVER, GITLAB_TOKEN, GITLAB_REPO_NAME, SERVICENAME)
            merge_pull_request(prs, SERVICENAME)
            if (files := get_filename_since_last_timestamp(gitlabserver=GITLAB_SERVER, token=GITLAB_TOKEN, repository=GITLAB_REPO_NAME, timestamp=latest_timestamp, servicename=SERVICENAME)) is not None and len(files) > 0:
                producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER, client_id='ioc_puller', api_version=(2,7,0))
                for file in files:
                    content = read_file_from_gitlab(gitlabserver=GITLAB_SERVER, token=GITLAB_TOKEN, repository=GITLAB_REPO_NAME, file=file, servicename=SERVICENAME)
                    filename = str(file).replace("/report.md", "")
                    message = convert_markdown_to_json(content, filename, SERVICENAME).encode('UTF-8')
                    producer.send(KAFKA_REPORT_TOPIC, message)
            latest_timestamp = Puller.commit_timestamp(
                    get_latest_commit_hash_by_branch(gitlabserver=GITLAB_SERVER, token=GITLAB_TOKEN, repository=GITLAB_REPO_NAME, branch=branch_name, servicename=SERVICENAME),
                    datetime.now().isoformat(), get_branch_name()
                )
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

    def __call__(self, app, *args, **kwargs):
        '''
        __call__
        '''
        for topic in [KAFKA_REPORT_TOPIC, KAFKA_TIMESTAMP_TOPIC]:
            create_topic_if_not_exists(KAFKA_SERVER, topic)
        scheduler.start()
        return Server.__call__(self, app, *args, **kwargs)
