'''
Kafka related funtions for the entire system.
'''

from kafka.consumer import KafkaConsumer

from kafka.admin import KafkaAdminClient
from kafka.admin import NewTopic

from libs.kafka.logging import LogMessage


def create_topic_if_not_exists(kafkaserver, topicname, servicename):
    '''
    create_topic_if_not_exists will create a given topic incase it does not already exists.
    @param kafkaserver will be the ip:port where the server is running.
    @param topicname will be the name of the topic.
    '''
    try:
        consumer = KafkaConsumer(bootstrap_servers=kafkaserver, group_id='libary')
        if topicname is not None:
            if (topics := consumer.topics()) is not None and not topicname in topics:
                admin_client = KafkaAdminClient(bootstrap_servers=kafkaserver, client_id='lib', api_version=(2, 7, 0))
                topic_list = [NewTopic(name=topicname, num_partitions=1, replication_factor=1)]
                admin_client.create_topics(new_topics=topic_list, validate_only=False)
                print("[+] Created a new topic. Name: {}".format(topicname))
    except Exception as error:
        LogMessage(str(error), LogMessage.LogTyp.ERROR, servicename).log()
