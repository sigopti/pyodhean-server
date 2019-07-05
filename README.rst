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

Install redis
-------------

It should be available from the package manager in most Linux distributions.

Install ipopt
-------------

Get ipopt tarball from https://github.com/JuliaOpt/IpoptBuilder/releases

Extract it ::

    tar -xvzf IpoptBuilder.xxx.tar.gz

Add it to the PATH ::

    export PATH=$PATH:/path/to/ipopt/bin/
    export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/ipopt/lib/

Launch solver server
--------------------

::

    celery -A pyodhean_server.celery worker

Configure and launch web API server
-----------------------------------

::

    # Set FLASK_ENV variable
    export FLASK_ENV=development

    # Alternatively, use a .env file
    echo "FLASK_ENV=development" > .env

    # Run application
    flask run


Run server for production
=========================

Install redis
-------------

It should be available from the package manager in most Linux distributions.

Install ipopt
-------------

Get ipopt tarball from https://github.com/JuliaOpt/IpoptBuilder/releases

Extract it ::

    tar -xvzf IpoptBuilder.xxx.tar.gz

Configure and launch solver service
-----------------------------------

Copy systemd and logrotate.d directories from docs/deployment/etc into /etc.

Customize pyodhean-celery.conf

Start the service and enable it for automatic start on system startup ::

    systemctrl start pyodhean-celery
    systemctrl enable pyodhean-celery

Configure and launch web API server
-----------------------------------

The following lines explain hwo to run pyodhean server with apache. They do not
cover creating and using an SSL certificate.

Copy apache2 directory from docs/deployment/etc into /etc.

Create a pyodhean directory to hold the application files.

Create a Pyhton 3 virtual environment in the pyodhean directory::

    virtualenv -p /usr/bin/python3 venv-pyodhean

Pull code from pyodhean and pyodhean-server repositories and install them in
the virtual environment ::

    source venv-pyodhean/bin/activate
    pip install ./pyodhean
    pip install ./pyodhean-server

Copy files from docs/deployment/pyodhean into the pyodhean directory.

Customize them if needed. At least the path to the virtual environment must be
specified.

Make sure settings.conf can be read by apache user and is not world readable::

    chown root:www-data application/settings.conf
    chmod 640 application/settings.conf

The pyodhean directory should look like this:::

    pyodhean/
        application/
            application.wsgi
            settings.conf
        venv-pyodhean
        pyodhean
        pyodhean-server

Note: The pyodhean and pyodhean-server repositories can be stored anywhere.
They do not have to be in the pyodhean repository.

Edit /etc/apache2/sites-available/pyodhean.conf.

Reload apache2.

The API should be available as https://domain.tld/api/v0/.
