'''
Tests for topichandler.py
'''
from unittest import TestCase, mock
from unittest.mock import patch

from libs.kafka.logging import LogMessage
from libs.kafka.topichandler import create_topic_if_not_exists


class TopicHandlerTests(TestCase):
    '''
    Tests for the topic handler script.
    '''

    def test_create_topic_if_not_exists_throws_an_exception_when_given_None_as_kafkaserver_parameter(self):
        '''
        Test to check, if the function throws an exception,
        when None has been given as the kafkaserver parameter.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, create_topic_if_not_exists(None, "TEST_TOPICNAME", "TEST_SERVICENAME"))

    def test_create_topic_if_not_exists_throws_an_exception_when_given_None_as_topicname_parameter(self):
        '''
        Test to check, if the function throws an exception,
        when None has been given as the topicname parameter.
        '''
        with patch.object(LogMessage, "log", return_value="ERROR"):
            self.assertRaises(Exception, create_topic_if_not_exists("TEST_KAFKASERVER", None, "TEST_SERVICENAME"))

    @mock.patch('libs.kafka.topichandler.KafkaConsumer')
    @mock.patch('libs.kafka.topichandler.KafkaAdminClient')
    def test_create_topic_if_not_exists_creates_a_new_topic_when_given_valid_parameters(self, mock_kafka_consumer, mock_kafka_admin_client):
        '''
        Test to check, if the function creates a new
        topic, when given valid parameters.
        '''
        mock_kafka_admin_client_instance = mock_kafka_admin_client.return_value
        mock_kafka_admin_client_instance.create_topics.side_effect = "TEST"
        create_topic_if_not_exists("TEST_KAFKASERVER", "TEST_TOPICNAME", "TEST_SERVICENAME")
        mock_kafka_admin_client.assert_called_once()
