"""Test a remote PyODHeaN solver API"""
# pylint: disable=invalid-name

import time
import json
import argparse
from pprint import pprint

import requests


parser = argparse.ArgumentParser(description='Test PyODHeaN API.')
parser.add_argument('--url', dest='host', required=True, help='API host URL')

args = parser.parse_args()

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


response = requests.post(
    args.host + '/solver/tasks/', data=json.dumps(json_input))
assert response.status_code == 200

task_id = response.json()['task_id']

while requests.get(
        args.host + '/solver/tasks/{}/status'.format(task_id)
).json()['status'] in ('waiting', 'ongoing'):
    time.sleep(1)

response = requests.get(args.host + '/solver/tasks/{}/result'.format(task_id))
assert response.status_code == 200
result = response.json()
assert result['status'] == 'ok'
assert 'solution' in result

# Display result
pprint(result)
