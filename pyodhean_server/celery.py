"""Celery application

Runs PyODHeaN model solver task asynchronously
"""
import os

from celery import Celery
from pyodhean_server.settings import DefaultCeleryConfig


app = Celery(
    'PyODHeaN Solver',
    include=['pyodhean_server.solver.task'],
)
app.config_from_object(DefaultCeleryConfig)

if 'CELERY_BROKER_URL' in os.environ:
    app.conf.update(broker_url=os.environ['CELERY_BROKER_URL'])
if 'CELERY_RESULT_BACKEND' in os.environ:
    app.conf.update(result_backend=os.environ['CELERY_RESULT_BACKEND'])
