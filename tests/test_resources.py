"""Resources tests"""
import time
import json
from unittest import mock

import pytest

from kombu.exceptions import OperationalError

from pyodhean_server.solver.task import solve, CELERY_STATUSES_MAPPING

from .utils import celery_running, redis_running


DUMMY_TASK_ID = '00000000-0000-0000-0000-000000000000'


class TestResources:

    @pytest.mark.usefixtures('init_app')
    def test_solve_redis_connection_error(self, json_input):
        with mock.patch.object(solve, 'delay', side_effect=OperationalError):
            response = self.client.post(
                '/solver/tasks/', data=json.dumps(json_input))
        assert response.status_code == 503

    @pytest.mark.usefixtures('init_app')
    def test_solve_link_without_node(self, json_input):
        json_input['links'].append(
            {'length': 10.0, 'source': [10.0, 10.0], 'target': [20.0, 20.0]})
        response = self.client.post(
            '/solver/tasks/', data=json.dumps(json_input))
        assert response.status_code == 422
        assert '_schema' in response.json['errors']

    @pytest.mark.usefixtures('init_app')
    def test_status_unknown_task(self):
        with mock.patch.object(
                solve.backend, 'get_state', return_value='PENDING'
        ):
            response = self.client.get(
                '/solver/tasks/{}/status'.format(DUMMY_TASK_ID))
        assert response.status_code == 404
        assert 'Unknown task ID: {}.'.format(DUMMY_TASK_ID) in response.json[
            'message']

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
                '/solver/tasks/{}/result'.format(DUMMY_TASK_ID))
        assert response.status_code == 404
        assert '/tasks/{}/status'.format(DUMMY_TASK_ID) in response.json[
            'message']

    @pytest.mark.skipif(
        not celery_running(), reason="This test requires Celery")
    @pytest.mark.skipif(
        not redis_running(), reason="This test requires Redis")
    @pytest.mark.usefixtures('init_app')
    def test_result_query_multiple_times(self, json_input):
        """Test result can be queried several times

        When using RabbitMQ as result backend (RPC backend), results are meant
        to be consumed only once: https://github.com/celery/celery/issues/5414.
        In practice, the result may be lost if queried several times.
        A reproducible case is when another task ID is queried. Then querying
        for original task ID will fail on a second attempt.
        """
        # Post task
        response = self.client.post(
            '/solver/tasks/', data=json.dumps(json_input))
        task_id = response.json['task_id']
        # Wait until task is completed
        while self.client.get(
                '/solver/tasks/{}/status'.format(task_id)
        ).json['status'] in ('waiting', 'ongoing'):
            time.sleep(0.1)
        # Query result for another task ID
        response = self.client.get(
            '/solver/tasks/{}/result'.format(DUMMY_TASK_ID))
        assert response.status_code == 404
        # Query task result
        response = self.client.get('/solver/tasks/{}/result'.format(task_id))
        assert response.status_code == 200
        result = response.json
        assert result['status'] == 'ok'
        assert 'solution' in result
        # Query task result again
        response = self.client.get('/solver/tasks/{}/result'.format(task_id))
        assert response.status_code == 200
        assert response.json == result
