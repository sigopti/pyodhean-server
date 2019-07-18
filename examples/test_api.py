"""Test PyODHeaN solver API"""
# pylint: disable=invalid-name

import time
import json
from pprint import pprint

from werkzeug.utils import cached_property
from flask import Response

from pyodhean_server.app import app


class JSONResponse(Response):
    # pylint: disable=too-many-ancestors
    """
    A Response class with extra useful helpers, i.e. ``.json`` property.

    Taken from https://github.com/frol/flask-restplus-server-example/
    """
    @cached_property
    def json(self):
        return json.loads(self.get_data(as_text=True))


app.response_class = JSONResponse

json_input = {
    'nodes': {
        'production': [
            # P1
            {
                'id': [0.0, 0.0],
                'technologies': {
                    'k1': {
                        'efficiency': 0.9,
                        't_out_max': 100,
                        't_in_min': 30,
                        'production_unitary_cost': 800,
                        'energy_unitary_cost': 0.08,
                        'energy_cost_inflation_rate': 0.04,
                    },
                },
            },
        ],
        'consumption': [
            # C1
            {
                'id': [2.0, 5.0],
                'kW': 80, 't_in': 80, 't_out': 60,
            },
            # C2
            {
                'id': [30.0, 50.0],
                'kW': 80, 't_in': 80, 't_out': 60,
            },
        ],
    },
    'links': [
        # P1 -> C1
        {'length': 10.0, 'source': [0.0, 0.0], 'target': [2.0, 5.0]},
        # C1 -> C2
        {'length': 100.0, 'source': [2.0, 5.0], 'target': [30.0, 50.0]},
    ]
}

client = app.test_client()

response = client.post('/solver/tasks/', data=json.dumps(json_input))
assert response.status_code == 200

task_id = response.json['task_id']

# Result not available yet
response = client.get('/solver/tasks/{}/result'.format(task_id))
assert response.status_code == 404
assert '/tasks/{}/status'.format(task_id) in response.json['message']

# Check status until it's over
# Note: In real life, one would need to catch failures
while client.get(
        '/solver/tasks/{}/status'.format(task_id)).json['status'] != 'success':
    time.sleep(1)

# When using RabbitMQ as result backend (RPC backend), results are meant to be
# consumed only once (https://github.com/celery/celery/issues/5414).
# In practice, the result may be lost if queried several times.
# A reproducible case is when another task ID is queried. Then querying for
# original task ID will fail on a second attempt.
dummy_task_id = '00000000-0000-0000-0000-000000000000'
response = client.get('/solver/tasks/{}/result'.format(dummy_task_id))
assert response.status_code == 404

# Result now available
response = client.get('/solver/tasks/{}/result'.format(task_id))
assert response.status_code == 200
result = response.json
assert result['status'] == 'ok'
assert 'solution' in result

response = client.get('/solver/tasks/{}/result'.format(task_id))
assert response.status_code == 200
assert response.json == result

# Display result
pprint(result)
