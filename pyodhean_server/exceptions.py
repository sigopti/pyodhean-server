"""Exceptions"""


class PyodheanServerError(Exception):
    """Generic PyODHeaN exception"""


class PyodheanServerConfigError(PyodheanServerError):
    """Configuration error"""
