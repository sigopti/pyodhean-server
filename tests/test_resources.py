"""Resources tests"""
import json
from unittest import mock

import pytest

from kombu.exceptions import OperationalError

from pyodhean_server.solver.task import solve, CELERY_STATUSES_MAPPING


DUMMY_TASK_ID = '00000000-0000-0000-0000-000000000000'


class TestResources:

    @pytest.mark.usefixtures('init_app')
    def test_solve_redis_connection_error(self, json_input):
        with mock.patch.object(solve, 'delay', side_effect=OperationalError):
            response = self.client.post(
                '/solver/tasks/',
                data=json.dumps(json_input)
            )
        assert response.status_code == 503

    @pytest.mark.usefixtures('init_app')
    def test_status_unknown_task(self):
        response = self.client.get(
            '/solver/tasks/{}/status'.format(DUMMY_TASK_ID)
        )
        assert response.status_code == 404

    @pytest.mark.parametrize(
        'status',
        (s for s in CELERY_STATUSES_MAPPING if s != 'SUCCESS')
    )
    @pytest.mark.usefixtures('init_app')
    def test_result_status_not_success(self, status):
        with mock.patch.object(
                solve.backend, 'get_state', return_value=status
        ):
            response = self.client.get(
                '/solver/tasks/{}/result'.format(DUMMY_TASK_ID)
            )
        assert response.status_code == 404
