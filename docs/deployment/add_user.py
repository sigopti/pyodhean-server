"""Add a user to users database"""
# pylint: disable=invalid-name

import argparse

from werkzeug.security import generate_password_hash

parser = argparse.ArgumentParser(description='Add user to users database')
parser.add_argument(
    'users_db',
    type=argparse.FileType('a', encoding='UTF-8'),
    help='Users DB file',
)
parser.add_argument('user', help='Username')
parser.add_argument('password', help='Password')

args = parser.parse_args()

args.users_db.write(
    ','.join((args.user, generate_password_hash(args.password))))
args.users_db.write('\n')
