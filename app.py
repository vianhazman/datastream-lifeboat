import time
import argparse
from client.CustomInfluxDBClient import CustomInfluxDBCLient
from client.CustomKafkaProducer import CustomKafkaProducer
from client.PostgresClient import PostgresClient
from util.dynamic import __getclass__
from util.getMissingDuplicateId import list_decrement
import util.constant as constant
from util.logging import get_logger
from util.parser import parse_config


def run():
    logger.info("Start execution for job {} with {} mode".format(args.job_name, args.mode))
    InfluxConfig = config['InfluxDB']

    if args.mode.lower() == 'daily':
        client = CustomInfluxDBCLient(InfluxConfig['host'], InfluxConfig['port'], InfluxConfig['username'],
                                      InfluxConfig['password'], InfluxConfig['database'])
        result = client.query(InfluxConfig['idField'], InfluxConfig['measurement'], args.start_time, args.end_time)
        result_list = list(result.get_points())

        ids = list(map(lambda x: x[InfluxConfig['idField']], result_list))

        ids.sort()

        missing_ids, duplicate_ids = list_decrement(ids)
        id_range = int(ids[-1]) - int(ids[0])
        logger.info("Missing data count: {}".format(len(missing_ids)))
        missing_data_percentage = (len(missing_ids) / id_range) * 100
        duplicate_data_percentage = (len(duplicate_ids) / id_range) * 100
        logger.info("Percentage of missing data: {:.2f}%".format(missing_data_percentage))
        logger.info("Percentage of duplicate data: {:.2f}%".format(duplicate_data_percentage))

    PostgresConfig = config['Postgres']

    pg = PostgresClient(PostgresConfig['username'], PostgresConfig['password'], PostgresConfig['host'],
                        PostgresConfig['port'], PostgresConfig['database'])

    logger.info(pg)

    if args.mode.lower() == 'daily':
        missing_data_list = pg.queryMissingData(PostgresConfig['table'], PostgresConfig['idField'], missing_ids)
    else:
        missing_data_list = pg.queryTimeRange(PostgresConfig['table'],
                                              args.start_time, args.end_time)

    KafkaConfig = config['Kafka']

    avroProducer = CustomKafkaProducer({
        'bootstrap.servers': KafkaConfig['bootstrap.servers'],
        'schema.registry.url': KafkaConfig['schema.registry.url']
    }, KafkaConfig['topic'])

    logger.info(avroProducer)

    logger.info(
        __getclass__(constant.TRANSFORMATION_PACKAGE, config['Job']['TransformationClass']).produce(avroProducer,
                                                                                                    missing_data_list))


def get_args():
    parser = argparse.ArgumentParser(description="specify job")
    parser.add_argument('--job_name', help="Job Name", required=True)
    parser.add_argument('--mode', help="Job Type - manual / daily", required=True)
    parser.add_argument('--start_time', help="Date start", required=True)
    parser.add_argument('--end_time', help="Date end")
    return parser.parse_args()


if __name__ == "__main__":
    logger = get_logger(__name__)
    start_time = time.time()
    args = get_args()
    config = parse_config(args.job_name)
    run()
    logger.info("--- Job execution finished in %s seconds ---" % (time.time() - start_time))
