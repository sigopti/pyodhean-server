"""Tesk PyODHeaN solver task"""
# pylint: disable=invalid-name

import time

from pprint import pprint

from pyodhean_server.task import solve


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
                'kW': 80, 'Tin': 80, 'Tout': 60,
            },
            # C2
            {
                'id': [30.0, 50.0], 'kWh': 0, 'tot_kWh': 10085800,
                'kW': 80, 'Tin': 80, 'Tout': 60,
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


# Sync
json_output = solve(json_input)
pprint(json_output)

# Async
task_id = solve.delay(json_input).id
while not solve.AsyncResult(task_id).ready():
    time.sleep(1)
json_output = solve.AsyncResult(task_id).result
pprint(json_output)
