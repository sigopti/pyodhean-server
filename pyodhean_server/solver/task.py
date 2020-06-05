"""PyODHeaN solver task"""
import pathlib
import json

from celery import shared_task
from celery.utils.log import get_task_logger

from pyodhean.interface import JSONInterface


logger = get_task_logger(__name__)


# See "Options available via the AMPL Interface" in IPOPT documentation.
# https://www.coin-or.org/Ipopt/documentation/node63.html
OPTIONS = {
    'tol': 1e-3,
}


# Celery app sets status to SENT when a task is published.
# A PENDING status means the task is unknown (wrong ID or deleted task)
# We don't need PENDING in the mapping because the view returns 404 on PENDING
CELERY_STATUSES_MAPPING = {
    'SENT': 'waiting',
    'RETRY': 'waiting',
    'STARTED': 'ongoing',
    'FAILURE': 'server_error',
    'REVOKED': 'server_error',
    'SUCCESS': 'success',
}


SOLVER_STATUSES_MAPPING = {
    'ok': 'ok',
    'warning': 'no_solution_found',
    'error': 'solver_error',
    'aborted': 'solver_error',
    'unknown': 'solver_error'
}


@shared_task(bind=True)
def solve(self, json_input):
    """Solve PyODHeaN model"""
    solver = JSONInterface(OPTIONS)
    logger.info('Starting solver')
    json_output = solver.solve(json_input, tee=False, keepfiles=False)
    status = json_output['status']
    if status in ('error', 'aborted', 'unknown'):
        logger.error(
            'Solver failed with status %(status)s', {'status': status})
    else:
        logger.info(
            'Solver succeeded with status %(status)s', {'status': status})
    json_output['status'] = SOLVER_STATUSES_MAPPING[status]
    # Log response to file
    io_files_dir = self.app.conf.get('io_files_dir')
    if io_files_dir is not None:
        with (
            pathlib.Path(io_files_dir) / f"{self.request.id}-response.json"
        ).open("w") as json_file:
            json_file.write(json.dumps(json_output, indent=2))
    return json_output
