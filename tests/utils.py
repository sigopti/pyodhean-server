"""Test utils"""
import redis


def redis_running():
    """Test Redis server is available"""
    redis_client = redis.Redis(socket_connect_timeout=1)
    try:
        redis_client.ping()
    except redis.exceptions.ConnectionError:
        return False
    return True
