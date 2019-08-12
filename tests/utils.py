"""Test utils"""
import json

from werkzeug.utils import cached_property
from flask import Response
import redis


class JSONResponse(Response):
    # pylint: disable=too-many-ancestors
    """
    A Response class with extra useful helpers, i.e. ``.json`` property.

    Taken from https://github.com/frol/flask-restplus-server-example/
    """
    @cached_property
    def json(self):
        return json.loads(self.get_data(as_text=True))


def redis_running():
    """Test Redis server is available"""
    redis_client = redis.Redis(socket_connect_timeout=1)
    try:
        redis_client.ping()
    except redis.exceptions.ConnectionError:
        return False
    return True
