"""Test utils"""
import redis
import celery
import celery.bin.base
import celery.bin.control
import celery.platforms

from pyodhean_server.celery import app as celery_app


def redis_running():
    """Test Redis server is available"""
    redis_client = redis.Redis(socket_connect_timeout=1)
    try:
        redis_client.ping()
    except redis.exceptions.ConnectionError:
        return False
    return True


def celery_running():
    """Test Celery server is available

    Inspired by https://stackoverflow.com/a/33545849
    """
    status = celery.bin.control.status(celery_app)
    try:
        status.run()
        return True
    except celery.bin.base.Error as exc:
        if exc.status == celery.platforms.EX_UNAVAILABLE:
            return False
        raise
