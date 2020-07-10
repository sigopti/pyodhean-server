"""Default application settings"""


class DefaultConfig:
    """Default configuration"""

    API_TITLE = 'PyODHeaN server'

    # Authentication
    AUTH_ENABLED = False

    # Logging
    LOGGER_ENABLED = False
    LOGGER_LEVEL = 'WARNING'
    LOGGER_FORMAT = (
        '%(asctime)s | %(levelname)-8s | '
        '%(remote_addr)-15s | %(method)-7s | %(url)s | %(message)s'
    )

    # Celery settings
    CELERY_BROKER_URL = 'redis://'
    CELERY_RESULT_BACKEND = 'redis://'
    CELERY_DEFAULT_QUEUE = 'pyodhean'

    # OpenAPI settings
    # These settings are used by the automatic swagger API documentation.
    # They may be overidden to disable it or configure it differently.
    # In production, it is a good idea to pin the ReDoc version number rather
    # than use "next".
    # See flask-smorest documentation:
    # https://flask-smorest.readthedocs.io/en/latest/openapi.html
    OPENAPI_VERSION = '3.0.2'
    OPENAPI_URL_PREFIX = '/'
    OPENAPI_REDOC_PATH = '/'
    OPENAPI_REDOC_URL = (
        "https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"
    )


class DefaultCeleryConfig:
    """Default Celery configuration"""
    broker_url = 'redis://'
    result_backend = 'redis://'
    task_default_queue = 'pyodhean'
    task_track_started = True
