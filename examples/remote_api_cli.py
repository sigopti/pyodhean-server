"""Remote PyODHeaN solver API example with problem defined in a .json file"""
# pylint: disable=invalid-name

import sys
import time
import json
import argparse
from pprint import pprint

import requests


parser = argparse.ArgumentParser(description='Test PyODHeaN API.')
parser.add_argument(
    '--url', dest='host', required=True, help='API host URL')
parser.add_argument(
    '-i', dest='input_file', required=True, help='Input JSON file'
)

args = parser.parse_args()

try:
    with open(args.input_file) as f:
        json_input = json.load(f)
except IOError as e:
    print('Input file error: {}'.format(e))
    sys.exit()


# Send task to solver
response = requests.post(
    args.host + '/solver/tasks/', data=json.dumps(json_input))
task_id = response.json()['task_id']

# Check status until it's over
while requests.get(
        args.host + '/solver/tasks/{}/status'.format(task_id)
).json()['status'] in ('waiting', 'ongoing'):
    time.sleep(1)

# Result now available
response = requests.get(args.host + '/solver/tasks/{}/result'.format(task_id))
result = response.json()

# Display result
pprint(result)
