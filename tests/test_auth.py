"""Authentication extension tests"""
import base64

from werkzeug.security import generate_password_hash, check_password_hash

import pytest

from pyodhean_server.app import create_app
from pyodhean_server.exceptions import PyodheanServerConfigError
from .common import TestingConfig

DUMMY_TASK_ID = '00000000-0000-0000-0000-000000000000'


class TestAuth:

    @pytest.mark.usefixtures('celery_worker')
    def test_auth_resource(self, tmp_path):
        """Test authentication feature

        Only "status" route is tested. The point is only to test the feature.
        """

        # Create users database file
        users_db_file = tmp_path / 'users.db'
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
        assert response.json["message"] == "Authentication error"

        # Wrong credentials
        creds = base64.b64encode('test:wrong'.encode()).decode()
        response = client.get(
            '/solver/tasks/{}/status'.format(DUMMY_TASK_ID),
            headers={'Authorization': 'Basic ' + creds},
        )
        assert response.status_code == 401
        assert response.json["message"] == "Authentication error"

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

    def test_auth_missing_auth_users_db_file(self, tmp_path):
        users_db_file = tmp_path / 'users.db'

        class AuthTestingConfig(TestingConfig):
            AUTH_ENABLED = True
            AUTH_USERS = str(users_db_file)

        with pytest.raises(
                PyodheanServerConfigError,
                match="Missing users DB file."
        ):
            create_app(AuthTestingConfig)

    @pytest.mark.usefixtures('init_app')
    def test_auth_add_user(self, tmp_path):
        users_db_file = tmp_path / 'users.db'
        result = self.app.test_cli_runner().invoke(
            args=('add-user', str(users_db_file), 'user_1', 'password_1')
        )
        assert result.exit_code == 0
        with open(users_db_file) as users_db:
            users = [line.split(',') for line in users_db.read().splitlines()]
        assert len(users) == 1
        assert check_password_hash(users[0][1], 'password_1')

        # Run twice to check line is appended
        result = self.app.test_cli_runner().invoke(
            args=('add-user', str(users_db_file), 'user_2', 'password_2')
        )
        assert result.exit_code == 0
        with open(users_db_file) as users_db:
            users = [line.split(',') for line in users_db.read().splitlines()]
        assert len(users) == 2
        assert check_password_hash(users[0][1], 'password_1')
        assert check_password_hash(users[1][1], 'password_2')
