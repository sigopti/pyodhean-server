"""PyODHeaN server application"""

import json
from flask import Flask
from webargs.flaskparser import use_args

from pyodhean_server.task import solve
from pyodhean_server.schemas import InputSchema


app = Flask('PyODHeaN server')


@app.route('/enqueue', methods=['POST'])
@use_args(InputSchema)
def enqueue(json_input):
    """Enqueue solver task"""
    return solve.delay(json_input).id


@app.route('/status/<uuid:task_id>')
def status(task_id):
    """Get solver task status"""
    return solve.AsyncResult(str(task_id)).status


@app.route('/result/<uuid:task_id>')
def result(task_id):
    """Get solver task result"""
    return json.dumps(solve.AsyncResult(str(task_id)).result)
