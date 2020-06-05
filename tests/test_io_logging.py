"""IO logging tests"""
import time
import json

import pytest

from pyodhean_server.app import create_app

from .common import TestingConfig
from .utils import redis_running


class TestIOLogging:

    @pytest.mark.skipif(not redis_running(), reason="This test requires Redis")
    def test_request_response_logging(
        self, json_input, tmp_path, celery_worker
    ):

        # Pass io files directory to Flask app config
        class IOLoggerTestingConfig(TestingConfig):
            IO_FILES_DIR = str(tmp_path)

        app = create_app(IOLoggerTestingConfig)
        client = app.test_client()

        # Pass io files directory to Celery app config
        celery_worker.app.conf['io_files_dir'] = str(tmp_path)

        # Post task
        response = client.post('/solver/tasks/', json=json_input)
        task_id = response.json['task_id']

        # Check request is logged
        log_files = list(tmp_path.iterdir())
        assert len(log_files) == 1
        request_file = log_files[0]
        assert request_file.name == f"{task_id}-request.json"
        assert json.load(request_file.open()) == json_input

        # Wait until task is completed
        while client.get(
                '/solver/tasks/{}/status'.format(task_id)
        ).json['status'] in ('waiting', 'ongoing'):
            time.sleep(0.1)

        # Query task result
        response = client.get('/solver/tasks/{}/result'.format(task_id))
        assert response.status_code == 200
        result = response.json
        assert result['status'] == 'ok'
        assert 'solution' in result

        # Check response is logged
        log_files = list(tmp_path.iterdir())
        assert len(log_files) == 2
        response_file = next(
            f for f in log_files if f.name == f"{task_id}-response.json"
        )
        # We can't test that response_file == response.json because the
        # response is modified by API schemas.
        assert 'solution' in json.load(response_file.open())
