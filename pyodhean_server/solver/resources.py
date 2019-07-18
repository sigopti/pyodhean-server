"""Solver API Blueprint"""

from flask_rest_api import Blueprint, abort

from .task import solve, CELERY_STATUSES_MAPPING
from .schemas import (
    SolverInputSchema, SolverOutputSchema, TaskIdSchema, StatusSchema)


blp = Blueprint(
    'Solver', __name__, url_prefix='/solver', description="Solver resources")


@blp.route('/tasks/', methods=['POST'])
@blp.arguments(SolverInputSchema)
@blp.response(TaskIdSchema)
def enqueue(json_input):
    """Enqueue solver task"""
    return solve.delay(json_input)


@blp.route('/tasks/<uuid:task_id>/status')
@blp.response(StatusSchema)
def status(task_id):
    """Get solver task status"""
    task_status = solve.AsyncResult(str(task_id)).status
    if task_status == 'PENDING':
        abort(
            404,
            message=(
                'Unknown task ID: {}. '
                'Either the task ID is wrong or the task was deleted.'
                ''.format(task_id)
            )
        )
    return {'status': CELERY_STATUSES_MAPPING[task_status]}


@blp.route('/tasks/<uuid:task_id>/result')
@blp.response(SolverOutputSchema)
def result(task_id):
    """Get solver task result"""
    if solve.AsyncResult(str(task_id)).status != 'SUCCESS':
        abort(
            404,
            message=(
                'Task result unavailable because status is not "success". '
                'Please check status first: /tasks/{}/status'.format(task_id)
            )
        )
    return solve.AsyncResult(str(task_id)).result
