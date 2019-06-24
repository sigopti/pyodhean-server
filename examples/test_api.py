"""Tesk PyODHeaN solver API"""
# pylint: disable=invalid-name

import time
import json
from pprint import pprint

from pyodhean_server.app import app


json_input = {
    'nodes': {
        'production': [
            # P1
            {
                'id': [0.0, 0.0], 'kWh': 0, 'tot_kWh': 15467900,
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
                'id': [2.0, 5.0], 'kWh': 5382100.0, 'tot_kWh': 15467900,
                'kW': 80, 't_in': 80, 't_out': 60,
            },
            # C2
            {
                'id': [30.0, 50.0], 'kWh': 0, 'tot_kWh': 10085800,
                'kW': 80, 't_in': 80, 't_out': 60,
            },
        ],
    },
    'links': [
        # P1 -> C1
        {'Length': 10.0, 'source': [0.0, 0.0], 'target': [2.0, 5.0]},
        # C1 -> C2
        {'Length': 100.0, 'source': [2.0, 5.0], 'target': [30.0, 50.0]},
    ]
}

client = app.test_client()

response = client.post('/tasks/', data=json.dumps(json_input))
assert response.status_code == 200

task_id = response.get_data(as_text=True)

while client.get(
        '/tasks/{}/status'.format(task_id)
        ).get_data(as_text=True) == 'PENDING':
    time.sleep(1)

# When using RabbitMQ as result backend (RPC backend), results are meant to be
# consumed only once (https://github.com/celery/celery/issues/5414).
# In practice, the result may be lost if queried several times.
# A reproducible case is when another task ID is queried. Then querying for
# original task ID will fail on a second attempt.
dummy_task_id = '00000000-0000-0000-0000-000000000000'
response = client.get('/tasks/{}/result'.format(dummy_task_id))
assert response.status_code == 200
assert json.loads(response.get_data(as_text=True)) is None

response = client.get('/tasks/{}/result'.format(task_id))
assert response.status_code == 200
assert json.loads(response.get_data(as_text=True)) is not None

response = client.get('/tasks/{}/result'.format(task_id))
assert response.status_code == 200
result = json.loads(response.get_data(as_text=True))
assert result is not None

# Display result
pprint(result)
