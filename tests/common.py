from pyodhean_server.settings import DefaultConfig


class TestingConfig(DefaultConfig):
    """Default donfiguration for tests"""
    TESTING = True
