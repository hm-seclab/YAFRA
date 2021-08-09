'''
Tests for logging.py
'''
from unittest import TestCase, mock
from unittest.mock import patch

from kafka import KafkaProducer

from libs.kafka.logging import LogMessage, send_health_message


class LoggingTests(TestCase):
    '''
    Tests for the logging script.
    '''

    def test_send_health_message_throws_an_exception_when_given_None_as_kafkaserver_parameter(self):
        '''
        Test to check, if the function throws an exception,
        when None has been given as the kafkaserver parameter.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, send_health_message(None, "TEST_TOPICNAME", "TEST_SERVICENAME"))

    def test_send_health_message_creates_a_new_topic_when_given_None_as_topicname_parameter(self):
        '''
        Test to check, if the function calls the
        create_topic_if_not_exists, when None has
        been given as the topicname parameter.
        '''
        with patch('libs.kafka.logging.create_topic_if_not_exists') as mock_create_topic_if_not_exists, patch.object(KafkaProducer, "send") as mock_kafka_producer_send:
            send_health_message("TEST_KAFKASERVER", None, "TEST_SERVICENAME")
            mock_create_topic_if_not_exists.assert_called_once()
            mock_kafka_producer_send.assert_called_once()

    @mock.patch('libs.kafka.logging.KafkaProducer')
    def test_send_health_message_creates_a_new_topic_when_given_valid_parameters(self, mock_kafka_producer):
        '''
        Test to check, if the function sends a health
        message, when given valid parameters.
        '''
        with patch('libs.kafka.logging.create_topic_if_not_exists') as mock_create_topic_if_not_exists:
            mock_kafka_producer_instance = mock_kafka_producer.return_value
            mock_kafka_producer_instance.send.side_effect = "TEST"
            send_health_message("TEST_KAFKASERVER", "TEST_TOPICNAME", "TEST_SERVICENAME")
            mock_create_topic_if_not_exists.assert_called_once()
            mock_kafka_producer.assert_called_once()
