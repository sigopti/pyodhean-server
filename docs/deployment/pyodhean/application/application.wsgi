#!/usr/bin/env python3
"""Sample wsgi file

Customize path to virtual environment and you're done
"""

import os
import sys

# Working with Virtual Environment
# http://flask.pocoo.org/docs/1.0/deploying/mod_wsgi/#working-with-virtual-environments
activate_this = '/path/to/pyodhean/venv-pyodhean/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))


# Add application to Python path
# Check before adding so as not to add it multiple times
# when reloading the file:
# https://code.google.com/p/modwsgi/wiki/ReloadingSourceCode
PATH = os.path.dirname(__file__)
if PATH not in sys.path:
    sys.path.append(PATH)

# Provide path to custom settings file
os.environ['FLASK_SETTINGS_FILE'] = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 'settings.cfg')

# Unleash the beast
from pyodhean_server.app import create_app
application = create_app()
