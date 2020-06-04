"""Test fixtures"""
import pyutilib.subprocess.GlobalData

import pytest

from pyodhean_server.app import create_app

from .common import TestingConfig

# https://github.com/PyUtilib/pyutilib/issues/31
# Disable signal handling
# Needed when using celery fixtures as task is launched in child thread
pyutilib.subprocess.GlobalData.DEFINE_SIGNAL_HANDLERS_DEFAULT = False


@pytest.fixture(params=[TestingConfig])
def init_app(request):
    """Initialize test application"""
    request.cls.app = create_app(request.param)
    request.cls.client = request.cls.app.test_client()


@pytest.fixture(scope='session')
def celery_config():
    return {
        'broker_url': 'redis://',
        'result_backend': 'redis://',
        # Use a dedicated queue to avoid clashing with a running worker
        'task_default_queue': 'testing',
    }


@pytest.fixture
def json_input():
    return {
        'nodes': {
            'production': [
                # P1
                {
                    'id': [0.0, 0.0],
                    'technologies': {
                        'k1': {
                            'efficiency': 0.9,
                            't_out_max': 100,
                            't_in_min': 30,
                            'production_unitary_cost': 800,
                            'energy_unitary_cost': 0.08,
                            'energy_cost_inflation_rate': 0.04,
                            'coverage_rate': 0.80,
                        },
                        'k2': {
                            'efficiency': 0.9,
                            't_out_max': 100,
                            't_in_min': 30,
                            'production_unitary_cost': 1000,
                            'energy_unitary_cost': 0.08,
                            'energy_cost_inflation_rate': 0.04,
                        },
                    },
                },
            ],
            'consumption': [
                # C1
                {
                    'id': [2.0, 5.0],
                    'kW': 80, 't_in': 60, 't_out': 80,
                },
                # C2
                {
                    'id': [30.0, 50.0],
                    'kW': 80, 't_in': 60, 't_out': 80,
                },
            ],
        },
        'links': [
            # P1 -> C1
            {'length': 10.0, 'source': [0.0, 0.0], 'target': [2.0, 5.0]},
            # C1 -> C2
            {'length': 100.0, 'source': [2.0, 5.0], 'target': [30.0, 50.0]},
        ],
        'parameters': {
            'diameter_int_max': 0.20,
            'speed_max': 2.5,
            'simultaneity_ratio': 0.70,
            'heat_loss_rate': 0.10,
        },
    }
