"""Tesk PyODHeaN solver task"""
# pylint: disable=invalid-name

import time

from pprint import pprint

from pyodhean_server.task import solve


json_input = {
    'nodes': [
        # P1
        {'id': [0, 0], 'kWh': 0, 'tot_kWh': 15467900, 'Type': 'Source'},
        # C1
        {'id': [2, 5], 'kWh': 5382100.0, 'tot_kWh': 15467900},
        # C2
        {'id': [30, 50], 'kWh': 0, 'tot_kWh': 10085800}
    ],
    'links': [
        # P1 -> C1
        {'Length': 10, 'source': [0, 0], 'target': [2, 5]},
        # C1 -> C2
        {'Length': 100, 'source': [2, 5], 'target': [30, 50]},
    ]
}


# Sync
json_output = solve(json_input)
pprint(json_output)

# Async
task_id = solve.delay(json_input)
while not solve.AsyncResult(task_id).ready():
    time.sleep(1)
json_output = solve.AsyncResult(task_id).result
pprint(json_output)
