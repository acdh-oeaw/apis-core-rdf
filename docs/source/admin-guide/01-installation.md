---
title: Installation
---

APIS Core is a library that allows you to easily build tools to manage
prosopographical data. It is not a ready-made software solution that you can
just deploy and start working. The typical workflow for starting an APIS
project is as follows: set up the project, create an
`ontology`, customize functionalities
and views, and finally add your data. This section will guide you
through the first step.

# Prerequisites

APIS needs Python 3.11+.

# Installation

{!../README.md!lines=55-132}

# Installation with Docker

This is the recommended way to install APIS on local machines as well as
on server infrastructure. For experimenting with APIS you can use the
[Docker file](https://github.com/acdh-oeaw/apis-core-rdf/blob/main/Dockerfile)
provided in the APIS core library. It allows you to spin up an APIS
instance using the sample project shipped with the APIS core library. To
start it, start a terminal and run:

-   `cd path/to/apis-core-rdf` to change to the directory where the
    Docker file is located,
-   `docker build -t apis .` to build the APIS image,
-   `docker run -p 5000:5000 apis` to start the container.

The APIS instance should now be accessible under
<http://localhost:5000>.

Alternatively you can also use the Docker image built for our
demo project. To do so run:

-   `docker run -p 5000:5000 ghcr.io/acdh-oeaw/apis-core-rdf/discworld/main:latest`
    to start the container.

To use the image for local development you can mount your local APIS
instance directory into the container using the following command:

`docker run -p 5000:5000 -v /path/to/your/apis_instance:/app apis`

Please note that you might need to install custom dependencies for the
APIS instance in your local Docker container.

This container uses the Django development server and is not suitable
for production use. Please see the next section for deploying APIS in
production.

## Docker Compose

In production, APIS should be used together with an SQL database. The
simplest way to set that up is by using [Docker
Compose](https://docs.docker.com/compose/). Below is an example of a
`docker-compose.yml` file that sets up an APIS instance with a
PostgreSQL database.

``` yaml
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
```

After `docker-compose up` you should now have a default APIS
installation accessible under <http://127.0.0.1:5000>.
