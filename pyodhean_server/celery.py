"""Celery application

Runs PyODHeaN model solver task asynchronously
"""
from celery import Celery


app = Celery(
    'PyODHeaN Solver',
    backend='redis://',
    broker='redis://',
    include=['pyodhean_server.task'],
)
