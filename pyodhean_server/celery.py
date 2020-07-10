"""Celery application

Runs PyODHeaN model solver task asynchronously
"""
import os

from celery import Celery, signals
from pyodhean_server.settings import DefaultCeleryConfig


celery = Celery(
    'PyODHeaN Solver',
    include=['pyodhean_server.solver.task'],
)
celery.config_from_object(DefaultCeleryConfig)

# https://stackoverflow.com/questions/52372117/how-to-call-a-celery-shared-task
# This seems to work around the issue of the task being owned by the Celery
# default app rather than this Celery app.
celery.set_default()

if 'CELERY_BROKER_URL' in os.environ:
    celery.conf.update(broker_url=os.environ['CELERY_BROKER_URL'])
if 'CELERY_RESULT_BACKEND' in os.environ:
    celery.conf.update(result_backend=os.environ['CELERY_RESULT_BACKEND'])
if 'CELERY_DEFAULT_QUEUE' in os.environ:
    celery.conf.update(task_default_queue=os.environ['CELERY_DEFAULT_QUEUE'])
if 'IO_FILES_DIR' in os.environ:
    celery.conf.update(io_files_dir=os.environ['IO_FILES_DIR'])


# https://stackoverflow.com/questions/9824172/find-out-whether-celery-task-exists
@signals.before_task_publish.connect
def cb_set_sent_state(sender=None, headers=None, **kwargs):
    """Set SENT custom status when the task is enqueued"""
    task = celery.tasks.get(sender)
    backend = task.backend
    backend.store_result(headers['id'], None, 'SENT')


def init_app(app):
    """Set Celery config from application"""
    celery.conf['broker_url'] = app.config['CELERY_BROKER_URL']
    celery.conf['result_backend'] = app.config['CELERY_RESULT_BACKEND']
    celery.conf['task_default_queue'] = app.config['CELERY_DEFAULT_QUEUE']
