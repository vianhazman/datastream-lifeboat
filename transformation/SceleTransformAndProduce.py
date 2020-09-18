import time

from util import constant

class SceleTransformAndProduce:
    def produce(avroProducer, missing_data_list):
        for i in missing_data_list:
            millis = int(round(time.time() * 1000))
            value = constant.AVRO_PAYLOAD_TEMPLATE
            value[constant.AFTER_FIELD] = i
            value[constant.TIMESTAMP_FIELD] = millis
            value[constant.SOURCE_FIELD][constant.TIMESTAMP_FIELD] = millis
            avroProducer.produce(value)
            avroProducer.poll(0)
        avroProducer.flush()

        return "Flushed {} rows of data from PG".format((len(missing_data_list)))
