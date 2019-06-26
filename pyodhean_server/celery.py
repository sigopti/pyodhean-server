"""Celery application

Runs PyODHeaN model solver task asynchronously
"""
from celery import Celery
from pyodhean_server.settings import DefaultCeleryConfig


app = Celery(
    'PyODHeaN Solver',
    include=['pyodhean_server.task'],
)
app.config_from_object(DefaultCeleryConfig)
