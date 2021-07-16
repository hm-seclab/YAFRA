'''
This script contains functions and classes related to logging.
'''

import json

from datetime import datetime

from enum import Enum
from kafka.producer import KafkaProducer

from libs.core.environment import envvar
from .topichandler import create_topic_if_not_exists

def send_health_message(kafkaserver, topicname, servicename):
    '''
    send_health_message will send a fine to the KAFKA server
        with the name of the service.
    @param kafkaserver will be the address of the KAFKA server.
    @param topicname will be the name of the KAFKA topic.
    @param serivcename will be the name of the calling service.
    '''
    try:
        create_topic_if_not_exists(kafkaserver, topicname)
        producer = KafkaProducer(bootstrap_servers=kafkaserver, client_id=str(servicename), api_version=(2,7,0))
        message = json.dumps({
            "Sender": servicename,
            "Message": "Fine",
            "Time": datetime.now().strftime("%H:%M:%S")
        })
        producer.send(topicname, message.encode('UTF-8'))
    except Exception as error:
        print(error)

class LogMessage():
    '''
    LogMessage will repesent a Warning, Info or Error-Log.
    '''

    class LogTyp(Enum):
        '''
        LogTyp will repesent all types of LogMessages, their symbol and name.
        @Types ERROR, INFO, WARNING
        '''
        ERROR = ("red", "[-]", "ERROR")
        INFO = ("blue", "[i]", "INFO")
        WARNING = ("yellow", "[!]", "WARNING")

    def __init__(self, message, typ, servicename, mute=False):
        '''
        __init__ is the CTor for the LogMessage object.
        @param message is the message to log.
        @param typ will be a object from LogMessage.LogTyp
        @param servicename is the name of the service who logged
            the message.
        @param mute is a boolean indicating whether a LogMessages
            should print a message.
        '''
        self.message = message
        self.typ = typ
        self.servicename = servicename
        self.mute = mute
        self.kafkaserver = envvar("KAFKA_SERVER", "0.0.0.0:9092")
        self.logging_topic = envvar("LOGGER_TOPIC", "logging")
        create_topic_if_not_exists(self.kafkaserver, self.logging_topic)

    def __json(self):
        '''
        __json will turn an LogMessage object into json.
        @param self is the LogMessage object.
        @return json-formatted-str
        '''
        return json.dumps({
            "typ": self.typ.value[2],
            "message": self.message,
            "service": self.servicename
        })

    def log(self):
        '''
        log will print a message given to the object and also stream it to the kafka logging topic.
        @param self is the LogMessage object.
        '''
        try:
            if not self.mute:
                print("{} {}: {} - ({})".format(self.typ.value[1], self.typ.value[2], self.message, self.servicename))
            producer = KafkaProducer(bootstrap_servers=self.kafkaserver, client_id='logging', api_version=(2, 7, 0))
            message = str(self.__json()).encode('UTF-8')
            producer.send(self.logging_topic, message)
        except Exception as error:
            print(error)
