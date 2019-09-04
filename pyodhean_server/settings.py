"""Default application settings"""


class DefaultConfig:
    """Default configuration"""
    API_VERSION = 0.1
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_REDOC_PATH = '/'
    OPENAPI_REDOC_VERSION = 'next'
    LOGGER_ENABLED = False
    LOGGER_LEVEL = 'WARNING'
    LOGGER_BACKUP = 30
    LOGGER_FORMAT = (
        '%(asctime)s | %(levelname)-8s | '
        '%(remote_addr)-15s | %(method)-7s | %(url)s | %(message)s'
    )


class DefaultCeleryConfig:
    """Default Celery configuration"""
    broker_url = 'redis://'
    result_backend = 'redis://'
    task_track_started = True
