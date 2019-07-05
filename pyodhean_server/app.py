"""PyODHeaN server application"""

from flask import Flask
from flask_rest_api import Api

from pyodhean_server.solver.resources import blp as solver_blp
from pyodhean_server.settings import DefaultConfig


app = Flask('PyODHeaN server')

app.config.from_object(DefaultConfig)
# Override config with optional settings file
app.config.from_envvar('FLASK_SETTINGS_FILE', silent=True)

api = Api(app)
api.register_blueprint(solver_blp)
