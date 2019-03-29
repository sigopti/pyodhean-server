"""Celery application

Runs PyODHeaN model solver task asynchronously
"""
from celery import Celery


app = Celery(  # pylint: disable=invalid-name
    'PyODHeaN Solver',
    backend='rpc://',
    broker='pyamqp://',
    include=['pyodhean_server.task'],
)
