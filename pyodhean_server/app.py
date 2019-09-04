"""PyODHeaN server application"""

from flask import Flask
from flask_rest_api import Api

from pyodhean_server.solver.resources import blp as solver_blp
from pyodhean_server import logger
from pyodhean_server.settings import DefaultConfig


def create_app():
    """Create application"""
    app = Flask('PyODHeaN server')

    app.config.from_object(DefaultConfig)
    # Override config with optional settings file
    app.config.from_envvar('FLASK_SETTINGS_FILE', silent=True)
    logger.init_app(app)

    api = Api(app)
    api.register_blueprint(solver_blp)

    app.logger.info("Pyodhean server started. Ready to rock.")

    return app
