===============
PyODHeaN Server
===============

Optimization of District Heating Networks

This package provides the solver server.


Installation
============

Install redis
-------------

It should be available from the package manager in most Linux distributions.

::

   aptitude install redis

Install ipopt
-------------

Install dependencies::

   aptitude install make g++ gfortran pkgconf liblapack-dev

Use coinbrew to fetch and compile Ipopt and dependencies::

    # Run as unprivileged user
    git clone --depth=1 https://github.com/coin-or/coinbrew
    cd coinbrew
    ./coinbrew Ipopt:releases/3.13.2 fetch
    ./coinbrew build Ipopt

Copy files to project directory::

    cp -r ./coinbrew/dist /path/to/project/ipopt

Install pyodhean
----------------

Use pip::

    pip install pyodhean-server

pyodhean-server supports Python >= 3.6.


Development configuration
=========================

Launch solver server
--------------------

Add path to ipopt to the PATH (should be added to .bashrc)::

    export PATH=$PATH:/path/to/project/ipopt/bin/

Check ipopt is correctly installed::

    ldd `which ipopt`
    ipopt -v

Launch worker::

    celery -A pyodhean_server worker

Configure and launch web API server
-----------------------------------

::

    # Set FLASK_ENV variable
    export FLASK_ENV=development

    # Alternatively, use a .env file
    echo "FLASK_ENV=development" > .env

    # Run application
    flask run


Production configuration
========================

Configure and launch web API server
-----------------------------------

The following lines explain hwo to run pyodhean server with apache. They do not
cover creating and using an SSL certificate.

Copy apache2 directory from docs/deployment/etc into /etc.

Create a pyodhean directory to hold the application files.

Create a Pyhton 3 virtual environment in the pyodhean directory::

    virtualenv -p /usr/bin/python3 venv-pyodhean

Pull code from pyodhean and pyodhean-server repositories and install them in
the virtual environment::

    source venv-pyodhean/bin/activate
    pip install ./pyodhean
    pip install ./pyodhean-server

Copy files from docs/deployment/pyodhean into the pyodhean directory.

Customize them if needed. At least the path to the virtual environment must be
specified.

Make sure settings.conf can be read by apache user::

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
They do not have to be in the pyodhean directory.

Edit /etc/apache2/sites-available/pyodhean.conf.

Reload apache2.

The API should be available as https://domain.tld/api/v0/.

Create directories to store log files::

    mkdir /var/log/pyodhean
    chmod pyodhean:pyodhean /var/log/pyodhean

Configure and launch solver service
-----------------------------------

Create pyodhean user::

   adduser --system --no-create-home --group pyodhean

Create log directory::

    mkdir -m 755 /var/log/pyodhean-celery
    chown pyodhean:pyodhean /var/log/pyodhean-celery

Copy systemd directory from docs/deployment/etc into /etc.

Edit pyodhean-celery configuration file to specify the paths.

   /etc/systemd/system/pyodhean-celery.service.d/pyodhean-celery.conf

Start the service and enable it for automatic start on system startup::

    systemctrl enable pyodhean-celery
    systemctrl start pyodhean-celery

Configure log files rotation
----------------------------

Copy logrotate.d directory from docs/deployment/etc into /etc.

Configure authentication
------------------------

Create a users DB file the apache user can read::

   touch /path/to/project/users.db
   chown root:www-data /path/to/project/users.db
   chmod 640 /path/to/project/users.db

Add users to the DB file::

    source venv-pyodhean/bin/activate
    flask add-user /path/to/project/users.db user password
    
Edit application configuration to enable authorization and pass users BD file::

   AUTH_ENABLED=True
   AUTH_USERS=/path/to/project/users.db
