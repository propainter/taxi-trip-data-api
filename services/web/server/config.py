# services/web/server/config.py

import os



class BaseConfig(object):
    '''Base configuration.'''
    DEBUG = False
    WTF_CSRF_ENABLED = True
    REDIS_URL = 'redis://redis:6379/0'
    QUEUES = ['default']
    INPUT_DATA_FILE = '/Users/himanshugautam/Downloads/chicago_taxi_trips_2020.parquet'
    SPARK_MASTER = "local[1]"
    KM_IN_UNIT_MILE=1.609344
    CONFIG_NAME='GOJEK'
    API_CACHE_TIMEOUT=60


class DevelopmentConfig(BaseConfig):
    '''Development configuration.'''
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SPARK_MASTER = "local[1]"
    INPUT_DATA_FILE = '/Users/himanshugautam/Downloads/chicago_taxi_trips_2020.parquet'


class TestingConfig(BaseConfig):
    '''Testing configuration.'''
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(BaseConfig):
    '''Production configuration.'''
    DEBUG = False