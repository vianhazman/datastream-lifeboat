from confluent_kafka.avro import AvroProducer
from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient

from util import constant


class CustomKafkaProducer(AvroProducer):

    def __init__(self, config, topicName):
        self.topicName = topicName
        config['on_delivery'] = self.delivery_report
        config['message.max.bytes'] = 1000000000

        sr = CachedSchemaRegistryClient({
            'url': config['schema.registry.url']
        })

        value_schema = sr.get_latest_schema("{}-value".format(topicName))[1]
        key_schema = sr.get_latest_schema("{}-key".format(topicName))[1]

        super().__init__(config, default_key_schema=key_schema, default_value_schema=value_schema)

    def produce(self, msg):
        key = {constant.ID_FIELD: msg[constant.AFTER_FIELD][constant.ID_FIELD]}
        super().produce(topic=self.topicName, value=msg, key=key)

    def delivery_report(self, err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
