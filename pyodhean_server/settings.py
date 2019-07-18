"""Default application settings"""


class DefaultConfig:
    """Default configuration"""
    API_VERSION = 0.1
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_REDOC_PATH = '/'
    OPENAPI_REDOC_VERSION = 'next'


class DefaultCeleryConfig:
    """Default Celery configuration"""
    broker_url = 'redis://'
    result_backend = 'redis://'
    task_track_started = True
