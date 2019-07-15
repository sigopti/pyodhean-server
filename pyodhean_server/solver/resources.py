"""Solver API Blueprint"""

from flask_rest_api import Blueprint, abort

from .task import solve
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
    return {'status': solve.AsyncResult(str(task_id)).status.lower()}


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
