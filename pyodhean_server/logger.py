"""Application logger"""

import time
import re
from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import request
from flask.logging import default_handler


class RequestFormatter(logging.Formatter):
    """Custom log Formatter injecting request information

    http://flask.pocoo.org/docs/1.0/logging/#injecting-request-information
    """
    def format(self, record):
        if request:
            record.url = request.url
            record.method = request.method
            record.remote_addr = request.remote_addr
        else:
            record.url = ''
            record.method = ''
            record.remote_addr = ''
        return super().format(record)


def init_app(app):
    """Initialize application logger"""

    # Use default config in DEBUG mode, configure logger otherwise
    if not app.debug:

        log_level = app.config['LOGGER_LEVEL']
        log_dir = Path(app.config['LOGGER_DIR'])
        log_backup_count = app.config['LOGGER_BACKUP']
        log_format = app.config['LOGGER_FORMAT']

        # Remove Flask default handler
        app.logger.removeHandler(default_handler)

        # Create a daily rotated log file handler
        file_handler = TimedRotatingFileHandler(
            str(log_dir / 'pyodhean.log'),
            when='midnight',
            backupCount=log_backup_count,
            utc=True)
        file_handler.suffix = '%Y-%m-%d'
        file_handler.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}$')

        # Create record formatter
        formatter = RequestFormatter(log_format)
        formatter.converter = time.gmtime
        file_handler.setFormatter(formatter)

        # Add our custom handler
        app.logger.addHandler(file_handler)

        # Set logging level
        app.logger.setLevel(log_level)
