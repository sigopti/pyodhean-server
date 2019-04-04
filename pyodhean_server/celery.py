"""Celery application

Runs PyODHeaN model solver task asynchronously
"""
from celery import Celery


app = Celery(
    'PyODHeaN Solver',
    backend='rpc://',
    broker='pyamqp://',
    include=['pyodhean_server.task'],
)
