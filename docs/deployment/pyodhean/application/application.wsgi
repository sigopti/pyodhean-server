"""Sample wsgi file

Customize path to virtual environment and you're done
"""
# pylint: disable=invalid-name

import os
from pathlib import Path

from pyodhean_server.app import create_app

# Provide path to custom settings file
os.environ['FLASK_SETTINGS_FILE'] = str(
    Path(__file__).parent.resolve() / "settings.cfg")

# Unleash the beast
application = create_app()
