#!/bin/sh

/app/manage.py migrate
/app/manage.py setup || true
/app/manage.py loaddata sample_project
/app/manage.py runserver 0.0.0.0:8000
