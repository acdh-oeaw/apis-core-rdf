Installation
============
APIS-core is a library that allows you to easily build tools to manage prosopographical data. It is not a ready-made software solution
that you just deploy and start working. The typical workflow for starting an APIS project is as follows: set up the project, create an 
:term:`ontology` customize the functionalities and views, and finally add your data. This section will guide you through the first step. 

Prerequisites
-------------

APIS webapp needs Python 3.11+. Depending on your setup you might also want to use virtualenvs 
and a dependency manager such as `poetry <https://python-poetry.org/>`_.

Simple installation on a linux box
-----------------------------------

.. include:: ../../README.md
   :start-after: <!-- Installation -->
   :parser: myst_parser.sphinx_

Installation with Docker
------------------------

This is the recommended way to install APIS on local machines as well as on server infrastructure.
For experimenting with APIS you can use the `Dockerfile <https://github.com/acdh-oeaw/apis-core-rdf/blob/main/Dockerfile>`_ provided in the
APIS core library. It allows you to spin up an APIS instance using the sample-project shipped with the APIS core library.
To start it fire up a terminal and run

- ``cd path/to/apis-core-rdf`` to change to the directory where the Dockerfile is located.
- ``docker build -t apis .`` to build the APIS image.
- ``docker run -p 5000:5000 apis`` to start the container. 

The APIS instance should now be accessible under http://localhost:5000.

To use the image for local development you can mount your local APIS instance directory to the container.
To do so you can use the following command:

``docker run -p 5000:5000 -v /path/to/your/apis_instance:/app apis``

Please note that you might need to install the further dependencies for the APIS instance in your local docker container.

This container uses the django development server and is not suitable for production use. Please see the next section for deploying APIS in production.

Docker Image
^^^^^^^^^^^^
For building and deploying a production APIS instances we use a `base image repo <https://github.com/acdh-oeaw/apis-base-container>`_ that contains a 
`Dockerfile <https://github.com/acdh-oeaw/apis-base-container/blob/main/Dockerfile>`_. 
For deploying APIS instances in the `ACDH-CH <https://www.oeaw.ac.at/acdh/>`_ cluster there is a 
`GitHub action <https://github.com/acdh-oeaw/prosnet-workflows/blob/main/.github/workflows/deploy-apis-instance.yml>`_ 
that can be used as a basis for similar deployments in Kubernetes clusters via GitHub.

The `Dockerfile <https://github.com/acdh-oeaw/apis-base-container/blob/main/Dockerfile>`_  expects some folders to be present in your local directories:

- ``apis_instance``: This is the directory of your application. It needs to be a valid Django project. As a starting point for developing your own APIS 
  instance you can use the `sample project <https://github.com/acdh-oeaw/apis-core-rdf/tree/main/sample_project>`_ shipped with the APIS core library.
- ``startup``: This directory contains shell scripts that are executed on container startup. The scripts are executed in alphabetical order. 
  The `startup scripts base image <https://github.com/acdh-oeaw/apis-base-container/tree/main/startup>`_ contains some scripts that are needed for 
  setting up an APIS instance. You can add your own scripts to this directory to customize the container startup process.
- ``apis``: A shell script that is the entrypoint of the container. The `apis <https://github.com/acdh-oeaw/apis-base-container/blob/main/apis>`_ script
  contained in our baseimage repo just calls the startup scripts in order.

After you have set up the needed directories you can build the image with:

``docker build -t apis .``

To start the container you can use:

``docker run -p 5000:5000 apis``


Docker Compose
^^^^^^^^^^^^^^

In production APIS should be used together with an SQL database. The simplest way to set that up is by using `Docker Compose <https://docs.docker.com/compose/>`_.
Below is an example of a ``docker-compose.yml`` file that sets up an APIS instance with a PostgreSQL database.

.. code-block:: yaml

  version: '3.8'

  services:
    app:
      build:
        context: .
        dockerfile: Dockerfile
      depends_on:
        db:
          condition: service_healthy
          restart: true

      environment: # some settings can be overwritten with env variables
        - DJANGO_SETTINGS_MODULE=apis.settings
        - DJANGO_SECRET_KEY=your_secret_key
        - DJANGO_DEBUG=True
        - DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
      volumes:
        - ${PWD}/local_apis_instance:/app #mount your local APIS instance to the container if needed
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

