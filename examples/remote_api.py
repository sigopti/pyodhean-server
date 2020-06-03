"""Remote PyODHeaN solver API example"""
# pylint: disable=invalid-name

import time
import argparse
import base64
from pprint import pprint

import requests


parser = argparse.ArgumentParser(description='Test PyODHeaN API.')
parser.add_argument('--url', dest='host', required=True, help='API host URL')
parser.add_argument('--user', dest='user', help='Username')
parser.add_argument('--password', dest='password', help='Password')

args = parser.parse_args()

headers = {}

if args.user:
    if args.password is None:
        parser.error('"password" is required when "user" is specified')
    creds = base64.b64encode(
        '{user}:{password}'.format(user=args.user, password=args.password)
        .encode()
    ).decode()
    headers['Authorization'] = 'Basic ' + creds


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
                        'coverage_rate': 0.80,
                    },
                    'k2': {
                        'efficiency': 0.9,
                        't_out_max': 100,
                        't_in_min': 30,
                        'production_unitary_cost': 1000,
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
                'kW': 80, 't_in': 60, 't_out': 80,
            },
            # C2
            {
                'id': [30.0, 50.0],
                'kW': 80, 't_in': 60, 't_out': 80,
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
        'diameter_int_max': 0.20,
        'speed_max': 2.5,
    },
}


# Send task to solver
response = requests.post(
    args.host + '/solver/tasks/',
    json=json_input,
    headers=headers,
)
task_id = response.json()['task_id']

# Check status until it's over
while requests.get(
        args.host + '/solver/tasks/{}/status'.format(task_id),
        headers=headers,
).json()['status'] in ('waiting', 'ongoing'):
    time.sleep(1)

# Result now available
response = requests.get(
    args.host + '/solver/tasks/{}/result'.format(task_id),
    headers=headers,
)
result = response.json()

# Display result
pprint(result)
