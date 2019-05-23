===============
PyODHeaN Server
===============

Optimization of District Heating Networks

This package provides the solver server.


Install
=======

::

    pip install pyodhean-server

pyodhean-server supports Python >= 3.5.


Run server for development
==========================

Solver server ::

    celery -A pyodhean_server.celery worker

Web API server ::

    # Set FLASK_ENV variable
    export FLASK_ENV=development

    # Alternatively, use a .env file
    echo "FLASK_ENV=development" > .env

    # Run application
    flask run
