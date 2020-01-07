"""PyODHeaN server application"""

from flask import Flask
from flask_smorest import Api

from pyodhean_server.solver.resources import blp as solver_blp
from pyodhean_server import logger, auth
from pyodhean_server.settings import DefaultConfig


def create_app(config_class=None):
    """Create application

    :param class config_class: Configuration class. This parameter is typically
        used for tests. In production, parameters are passed using the file in
        FLASK_SETTINGS_FILE environment variable.
    """
    app = Flask('PyODHeaN server')

    app.config.from_object(config_class or DefaultConfig)
    # Override config with optional settings file
    app.config.from_envvar('FLASK_SETTINGS_FILE', silent=True)
    logger.init_app(app)
    auth.init_app(app)

    api = Api(app)
    api.register_blueprint(solver_blp)

    app.logger.info("Pyodhean server started. Ready to rock.")

    return app
