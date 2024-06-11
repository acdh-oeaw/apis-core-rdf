#!/bin/sh

/app/manage.py migrate
/app/manage.py setup || true
/app/manage.py loaddata sample_project --settings=sample_project.settings_loaddata
/app/manage.py runserver 0.0.0.0:5000
