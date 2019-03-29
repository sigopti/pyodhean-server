"""PyODHeaN solver task"""
from pyodhean.interface import JSONInterface
from pyodhean_server.celery import app


# options [cf https://www.coin-or.org/Ipopt/documentation/node42.html]
OPTIONS = {
    'tol': 1e-3,           # defaut: 1e-8
}


@app.task
def solve(json_input):
    """Solve PyODHeaN model"""
    solver = JSONInterface(OPTIONS)
    json_output = solver.solve(json_input, tee=False, keepfiles=False)
    return json_output
