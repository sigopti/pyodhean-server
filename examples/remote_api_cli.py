"""Remote PyODHeaN solver API example with problem defined in a .json file"""
# pylint: disable=invalid-name

import time
import json
import argparse
import base64
from pprint import pprint

import requests


parser = argparse.ArgumentParser(description='Test PyODHeaN API.')
parser.add_argument(
    '--url', dest='host', required=True, help='API host URL')
parser.add_argument(
    '-i',
    dest='input_file',
    required=True,
    type=argparse.FileType('r'),
    help='Input JSON file',
)
parser.add_argument('--user', dest='user', help='Username')
parser.add_argument('--password', dest='password', help='Password')

args = parser.parse_args()

json_input = json.load(args.input_file)

headers = {}

if args.user:
    if args.password is None:
        parser.error('"password" is required when "user" is specified')
    creds = base64.b64encode(
        '{user}:{password}'.format(user=args.user, password=args.password)
        .encode()
    ).decode()
    headers['Authorization'] = 'Basic ' + creds


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
