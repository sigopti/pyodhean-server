"""Solver API Blueprint"""

from flask_rest_api import Blueprint

from pyodhean_server.task import solve
from pyodhean_server.schemas import (
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
    return solve.AsyncResult(str(task_id))


@blp.route('/tasks/<uuid:task_id>/result')
@blp.response(SolverOutputSchema)
def result(task_id):
    """Get solver task result"""
    return solve.AsyncResult(str(task_id)).result
