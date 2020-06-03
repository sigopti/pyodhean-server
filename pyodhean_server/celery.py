"""Celery application

Runs PyODHeaN model solver task asynchronously
"""
import os

from celery import Celery, signals
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
if 'IO_FILES_DIR' in os.environ:
    app.conf.update(io_files_dir=os.environ['IO_FILES_DIR'])


# https://stackoverflow.com/questions/9824172/find-out-whether-celery-task-exists
@signals.before_task_publish.connect
def cb_set_sent_state(sender=None, headers=None, **kwargs):
    """Set SENT custom status when the task is enqueued"""
    task = app.tasks.get(sender)
    backend = task.backend
    backend.store_result(headers['id'], None, 'SENT')
