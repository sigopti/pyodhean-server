"""Solver API Blueprint"""
import pathlib
import json

from flask import current_app
from kombu.exceptions import OperationalError

from flask_smorest import Blueprint, abort

from pyodhean_server.auth import auth
from .task import solve, CELERY_STATUSES_MAPPING
from .schemas import (
    SolverInputSchema, SolverOutputSchema, TaskIdSchema, StatusSchema)


blp = Blueprint(
    'Solver', __name__, url_prefix='/solver', description="Solver resources")


@blp.route('/tasks/', methods=['POST'])
@auth.login_required
@blp.arguments(SolverInputSchema)
@blp.response(TaskIdSchema)
def enqueue(json_input):
    """Enqueue solver task"""
    try:
        task = solve.delay(json_input)
    except OperationalError:
        current_app.logger.error("Can't queue task. Check Redis is running.")
        abort(503)
    current_app.logger.info("Task %(task_id)s enqueued.", {'task_id': task.id})
    current_app.logger.debug(json.dumps(json_input))
    # Log request to file
    io_files_dir = current_app.config.get('IO_FILES_DIR')
    if io_files_dir is not None:
        with (
            pathlib.Path(io_files_dir) / f"{task.id}-request.json"
        ).open("w") as json_file:
            json_file.write(json.dumps(json_input, indent=2))
    return task


@blp.route('/tasks/<uuid:task_id>/status')
@auth.login_required
@blp.response(StatusSchema)
def status(task_id):
    """Get solver task status"""
    task_state = solve.backend.get_state(str(task_id))
    if task_state == 'PENDING':
        abort(
            404,
            message=(
                'Unknown task ID: {}. '
                'Either the task ID is wrong or the task was deleted.'
                ''.format(task_id)
            )
        )
    return {'status': CELERY_STATUSES_MAPPING[task_state]}


@blp.route('/tasks/<uuid:task_id>/result')
@auth.login_required
@blp.response(SolverOutputSchema)
def result(task_id):
    """Get solver task result"""
    task_state = solve.backend.get_state(str(task_id))
    if task_state != 'SUCCESS':
        abort(
            404,
            message=(
                'Task result unavailable because status is not "success". '
                'Please check status first: /tasks/{}/status'.format(task_id)
            )
        )
    return solve.AsyncResult(str(task_id)).result
