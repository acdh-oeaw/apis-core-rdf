Installation with Docker
========================

This is the recommended way to install APIS on local machines as well as on server infrastructure.

Docker Image
------------
For building and deploying APIS instances we use a `base image <https://github.com/acdh-oeaw/apis-base-container>`_. For deploying APIS instances in the `ACDH-CH <https://www.oeaw.ac.at/acdh/>`_ cluster there is a `GitHub action <https://github.com/acdh-oeaw/prosnet-workflows/blob/main/.github/workflows/deploy-apis-instance.yml>`_ that can be used as a basis for similar deployments in Kubernetes clusters via GitHub.

Docker Compose
--------------

For local development and or deployment on a single node/server there is a `APIS compose repo <https://github.com/acdh-oeaw/apis-core-rdf-compose>`_. It is setup with `OEBL ontology <https://github.com/acdh-oeaw/apis-instance-oebl-pnp/tree/abcfb7ee4708eded7428bc1a8e243233cf28e8b6>`_ as a basis, but the submodule can be exchanged for other APIS ontologies.
The `docker-compose <https://github.com/acdh-oeaw/apis-core-rdf-compose/blob/main/docker-compose.yml>`_ file included can be used as a starting point for a deployment via docker-compose. What is missing in this setup is some kind of reverse proxy solution (such as Traefik or an Nginx container).

.. code-block:: yaml

  version: '3.8'

  services:
    app:
      build:
        context: .
        dockerfile: apis-base-container/Dockerfile
      depends_on:
        db:
          condition: service_healthy
          restart: true

      env_file:
        - apis_settings.env
      volumes:
        - ${PWD}/apis_local_settings.py:/app/apis_local_settings.py
        - ${PWD}/local_startup_scripts/060-createsuperuser:/startup/060-createsuperuser
      ports:
        - 5000:5000

    db:
      image: postgres:latest
      restart: unless-stopped
      volumes:
        - postgres-data:/var/lib/postgresql/data
      environment:
        POSTGRES_USER: postgres
        POSTGRES_DB: postgres #use other passwords in production
        POSTGRES_PASSWORD: postgres
        POSTGRES_EXTENSIONS: pg_trgm
      healthcheck:
        test: ["CMD-SHELL", "pg_isready -d $${POSTGRES_DB} -U $${POSTGRES_USER}"]
        interval: 10s
        timeout: 3s
        retries: 3

  volumes:
    postgres-data:


After ``docker-compose up`` you should now have a default APIS installation accessible under http://0.0.0.0:5000.


Installation without Docker
===========================

Prerequisites
-------------

APIS webapp needs Python 3.11+ and `poetry <https://python-poetry.org/>`_ as a dependency manager.

Installation on a linux box
----------------------------

Change to the directory you have downloaded APIS to. Please note that a fully working APIS installation needs an ontology, a setting files and some other files alongside `apis-core-rdf <https://github.com/acdh-oeaw/apis-core-rdf>`_ library. Existing APIS instances such as `OEBL <>`_, `SiCProd <>`_, `Frischmuth <>`_ and `Tibschol <>`_ can serve as a starting point for developing your own instance. Clone one of these repos and install the dependencies:

.. code-block:: console
    poetry install

Next you need to change the settings file of the instance you cloned. For most of them its in ``apis_ontology/server.py``.
Especially you need to set the database connection to your needs. Alternatively you can set the environment variable ``DATABASE_URL`` to an appropriate string. See the documentation of `dj-database-url <https://github.com/jazzband/dj-database-url>`_ for details on how to do that.

Dont forget to set ``DEBUG = False`` once you are in production.

Once the database connection is set run:

.. code-block:: console

    poetry run manage.py migrate --settings=apis_ontology.server

For convenience we suggest you alter ``manage.py`` to::

    if __name__ == "__main__":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apis_ontology.server")

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)

Once that is done you dont have to include ``--settings=apis_ontology.server`` in your commands anymore.

Next we migrate the APIS internal tables:

.. code-block:: console

    poetry run manage.py migrate

and create a superuser:

.. code-block:: console

    poetry run manage.py createsuperuser

answer the questions and hit enter.
Now you can already proceed running the development server:

.. code-block:: console

    poetry run manage.py runserver

should bring up a development server window with your new apis instance.


Installation on Windows
-----------------------

Change to the directory you have downloaded APIS to and install the needed Python packages
In the command prompt that pops up after the activation of the virtualenv, change directory to where you have downloaded apis (eg. to apis-core) and install the modules in requirements.txt

.. code-block:: console

    poetry install

If you encounter problems while installing the packages in the requirements.txt file, remove the ones that cause the problem (from the requirements.txt file), and download the .whl file of the problematic module from the following site: http://www.lfd.uci.edu/~gohlke/pythonlibs/ (choosing the correct version: your python version must be equal to the number after cp in the name of the .whl file, and your operating system 32-bit/64-bit with the end of the file name.)

Install the missing module by running the following command in the prompt from where your .whl file resides:

.. code-block:: console

    pip install name_of_the_whl_file

Install numpy+mkl, download the wheel file from the link above and install with the command:

.. code-block:: console

    pip install name_of_the_whl_file

Download and install SQLite (www.sqlite.org).

Next copy the dummpysettings.py file and rename it to server.py with the following command:
copy apisapp\apis\settings\dummysettings.py apisapp\apis\settings\server.py
Now edit ``server.py`` to your needs.

If you installed sqlite, it should look like below::

    import os
    from .base import *

    SECRET_KEY = 'd3j@zlckxkw73c3*ud2-11$)d6i)^my(60*o1psh*&-u35#ayi'
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': os.path.join('path\\to\\your\\sqlite\\installation', 'db.sqlite3'),
       }
    }

If you intend to use Mysql it should look something like::

    import os
    from .base import *

    SECRET_KEY = 'asdaaserffsdfi'
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'databsename',
        'USER': 'dtabaseuser',
        'PASSWORD': 'databasepassword',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
        }
    }

Dont forget to set ``DEBUG = False`` once you are in production.

Once the database connection is set, run:

.. code-block:: console

    python manage.py migrate --settings=apis.settings.server

For convenience we suggest you alter ``manage.py`` to::

    if __name__ == "__main__":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apis.settings.server")

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)

Once that is done you dont have to include ``--settings=apis.settings.server`` in your commands anymore.

Next we migrate the APIS internal tables:

.. code-block:: console

    python manage.py makemigrations metainfo entities relations vocabularies highlighter labels webpage
    python manage.py migrate

and create a superuser:

.. code-block:: console

    python manage.py createsuperuser

answer the questions and change to the static directory to download javascript libraries:

If you havent installed NPM and bower yet, install NodeJS, and bower with npm. Bower depends on Node.js and NPM, download the installation package from the Node.js site and click through it. You can now install Bower with npm. You might need to restart Windows to get all the path variables setup.
Open the Git Bash or Command Prompt and install bower with the following command.

.. code-block:: console

    npm install -g bower

If you have already installed bower you can proceed with installing the javascript libraries directly. In the command line or git bash go to the directory apis-webpage\static\webpage\libraries and run:

.. code-block:: console

    bower install

Finally the below command brings up a development server window with your new apis instance.

.. code-block:: console

    python manage.py runserver


Serving APIS via Apache WSGI
----------------------------

If you plan to use APIS in production you should deploy it via a proper webserver. We use Apache_ and ``mod_wsgi`` to
do so. Our apche virtualhost config looks something like:

.. code-block:: aconf

   <VirtualHost *:80>
      ServerName server_name
      ServerAlias server_alias #alias names if needed
      DocumentRoot /var/www/html #document root of your installation
      WSGIDaemonProcess YOUR_URL user=#1025 group=#1025 python-path=/var/www/html/
      WSGIProcessGroup YOUR_URL user=#1025 group=#1025 python-path=/var/www/html/
      WSGIScriptAlias / /var/www/html/apis-core/apis/wsgi.py
      <Directory /var/www/html>
        Require all granted
        AllowOverride All
        Options All granted
      </Directory>
      Alias /static /var/www/html/apis-core/static_dir #static directories to server via Apache
      Alias /downloads /var/www/html/apis-core/downloads
   </VirtualHost>

If the database is connected and the virtualhost is configured you are good to go:

.. code-block:: bash

    service apache2 reload


.. _Apache: https://httpd.apache.org/
