"""Authentication"""

import csv
from pathlib import Path

from werkzeug.security import check_password_hash
from flask_httpauth import HTTPBasicAuth
from flask_smorest import abort

from .exceptions import PyodheanServerConfigError


auth = HTTPBasicAuth()  # pylint: disable=invalid-name


def init_app(app):
    """Initialize application authentication"""

    # Check config on startup
    if app.config["AUTH_ENABLED"]:
        if "AUTH_USERS" not in app.config:
            raise PyodheanServerConfigError("Missing AUTH_USERS parameter.")
        users_db_file = app.config["AUTH_USERS"]
        if not Path(users_db_file).exists():
            raise PyodheanServerConfigError("Missing users DB file.")

    @auth.verify_password
    def verify_password(username, password):  # pylint: disable=unused-variable
        if not app.config["AUTH_ENABLED"]:
            return True
        users = {}
        with open(app.config["AUTH_USERS"]) as users_db:
            for row in csv.reader(users_db):
                # Skip empty rows
                if row:
                    users[row[0]] = row[1]
        if username in users:
            return check_password_hash(users.get(username), password)
        return False

    @auth.error_handler
    def auth_error(status):  # pylint: disable=unused-variable
        # Call abort to trigger error handler and get consistent JSON output
        abort(status, message="Authentication error")
