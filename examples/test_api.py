"""Tesk PyODHeaN solver API"""
# pylint: disable=invalid-name

import time
import json
from pprint import pprint

from pyodhean_server.app import app


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

client = app.test_client()

task_id = client.post(
    'enqueue',
    data=json.dumps(json_input)
).get_data(as_text=True)


while client.get(
        'status/{}'.format(task_id)
        ).get_data(as_text=True) == 'PENDING':
    time.sleep(1)

# When using RabbitMQ as result backend (RPC backend), results are meant to be
# consumed only once (https://github.com/celery/celery/issues/5414).
# In practice, the result may be lost if queried several times.
# A reproducible case is when another task ID is queried. Then querying for
# original task ID will fail on a second attempt.
dummy_task_id = '00000000-0000-0000-0000-000000000000'
result = client.get('result/{}'.format(dummy_task_id)).get_data(as_text=True)
assert json.loads(result) is None
result = client.get('result/{}'.format(task_id)).get_data(as_text=True)
assert json.loads(result) is not None
result = client.get('result/{}'.format(task_id)).get_data(as_text=True)
assert json.loads(result) is not None
pprint(json.loads(result))
