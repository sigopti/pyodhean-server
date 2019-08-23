"""Test fixtures"""
import pytest

from pyodhean_server.app import create_app

from .utils import JSONResponse


@pytest.fixture
def init_app(request):
    """Initialize test application"""
    request.cls.app = create_app()
    request.cls.app.config['TESTING'] = True
    request.cls.app.response_class = JSONResponse
    request.cls.client = request.cls.app.test_client()


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
                        },
                    },
                },
            ],
            'consumption': [
                # C1
                {
                    'id': [2.0, 5.0],
                    'kW': 80, 't_in': 80, 't_out': 60,
                },
                # C2
                {
                    'id': [30.0, 50.0],
                    'kW': 80, 't_in': 80, 't_out': 60,
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
            'diameter_int_min': 0.10,
            'speed_max': 2,
        },
    }
