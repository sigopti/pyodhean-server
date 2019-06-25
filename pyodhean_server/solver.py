"""Solver API Blueprint"""

import json
from flask_rest_api import Blueprint

from pyodhean_server.task import solve
from pyodhean_server.schemas import InputSchema


blp = Blueprint(
    'Solver', __name__, url_prefix='/solver', description="Solver resources")


@blp.route('/tasks/', methods=['POST'])
@blp.arguments(InputSchema)
def enqueue(json_input):
    """Enqueue solver task"""
    return solve.delay(json_input).id


@blp.route('/tasks/<uuid:task_id>/status')
def status(task_id):
    """Get solver task status"""
    return solve.AsyncResult(str(task_id)).status


@blp.route('/tasks/<uuid:task_id>/result')
def result(task_id):
    """Get solver task result"""
    return json.dumps(solve.AsyncResult(str(task_id)).result)
