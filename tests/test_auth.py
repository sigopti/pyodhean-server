"""Authentication extension tests"""
import base64
from pathlib import Path

from werkzeug.security import generate_password_hash

import pytest

from pyodhean_server.app import create_app
from pyodhean_server.exceptions import PyodheanServerConfigError
from .common import TestingConfig

DUMMY_TASK_ID = '00000000-0000-0000-0000-000000000000'


class TestAuth:

    def test_auth_resource(self, tmpdir):
        """Test authentication feature

        Only "status" route is tested. The point is only to test the feature.
        """

        # Create users database file
        users_db_file = Path(tmpdir) / 'users.db'
        with open(users_db_file, 'w') as users_db:
            users_db.write(','.join(('test', generate_password_hash('test'))))

        class AuthTestingConfig(TestingConfig):
            AUTH_ENABLED = True
            AUTH_USERS = str(users_db_file)

        app = create_app(AuthTestingConfig)
        client = app.test_client()

        # Missing credentials
        response = client.get(
            '/solver/tasks/{}/status'.format(DUMMY_TASK_ID))
        assert response.status_code == 401

        # Wrong credentials
        creds = base64.b64encode('test:wrong'.encode()).decode()
        response = client.get(
            '/solver/tasks/{}/status'.format(DUMMY_TASK_ID),
            headers={'Authorization': 'Basic ' + creds},
        )
        assert response.status_code == 401

        # Right credentials
        creds = base64.b64encode('test:test'.encode()).decode()
        response = client.get(
            '/solver/tasks/{}/status'.format(DUMMY_TASK_ID),
            headers={'Authorization': 'Basic ' + creds},
        )
        assert response.status_code == 404

    def test_auth_missing_auth_users_parameter(self):
        class AuthTestingConfig(TestingConfig):
            AUTH_ENABLED = True

        with pytest.raises(
                PyodheanServerConfigError,
                match="Missing AUTH_USERS parameter."
        ):
            create_app(AuthTestingConfig)

    def test_auth_missing_auth_users_db_file(self, tmpdir):
        users_db_file = Path(tmpdir) / 'users.db'

        class AuthTestingConfig(TestingConfig):
            AUTH_ENABLED = True
            AUTH_USERS = str(users_db_file)

        with pytest.raises(
                PyodheanServerConfigError,
                match="Missing users DB file."
        ):
            create_app(AuthTestingConfig)
