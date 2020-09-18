AVRO_PAYLOAD_TEMPLATE = {
    'before': None,
    'after': None,
    'source': {
    'version': '1.0.1.Final' ,
    'connector': 'postgresql' ,
    'name': 'p-scele' ,
    'ts_ms': 1597838401785 ,
    'db': 'scele_s1' ,
    'schema': 'public' ,
    'table': 'mdl_logstore_standard_log'
  } ,
    'op': 'c',
    'ts_ms': 1597838416653
}

ID_FIELD = 'id'
AFTER_FIELD='after'
TIMESTAMP_FIELD='ts_ms'
SOURCE_FIELD='source'
TRANSFORMATION_PACKAGE='transformation'