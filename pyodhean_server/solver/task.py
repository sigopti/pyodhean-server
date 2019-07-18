"""PyODHeaN solver task"""
from pyodhean.interface import JSONInterface
from pyodhean_server.celery import app


# options [cf https://www.coin-or.org/Ipopt/documentation/node42.html]
OPTIONS = {
    'tol': 1e-3,           # defaut: 1e-8
}


CELERY_STATUSES_MAPPING = {
    'SENT': 'waiting',
    'RETRY': 'waiting',
    'STARTED': 'ongoing',
    'FAILURE': 'server_error',
    'SUCCESS': 'success',
    'PENDING': 'unknown',
}


SOLVER_STATUSES_MAPPING = {
    'ok': 'ok',
    'warning': 'no_solution_found',
    'error': 'solver_error',
    'aborted': 'solver_error',
    'unknown': 'solver_error'
}


@app.task
def solve(json_input):
    """Solve PyODHeaN model"""
    solver = JSONInterface(OPTIONS)
    json_output = solver.solve(json_input, tee=False, keepfiles=False)
    json_output['status'] = SOLVER_STATUSES_MAPPING[json_output['status']]
    return json_output
