"""PyODHeaN solver API example"""
# pylint: disable=invalid-name

import time
import json
from pprint import pprint

from pyodhean_server.app import create_app


DUMMY_TASK_ID = '00000000-0000-0000-0000-000000000000'


app = create_app()

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
    ],
    'parameters': {
        'diameter_int_min': 0.10,
        'speed_max': 2,
    },
}

client = app.test_client()

# Send task to solver
response = client.post('/solver/tasks/', data=json.dumps(json_input))
task_id = response.json['task_id']

# Check status until it's over
while client.get(
        '/solver/tasks/{}/status'.format(task_id)
).json['status'] in ('waiting', 'ongoing'):
    time.sleep(1)

# Result now available
response = client.get('/solver/tasks/{}/result'.format(task_id))
result = response.json

# Display result
pprint(result)
