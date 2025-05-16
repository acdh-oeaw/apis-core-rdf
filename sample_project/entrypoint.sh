#!/bin/sh

/app/manage.py migrate
/app/manage.py setup || true
/app/manage.py loaddata sample_project --settings=sample_project.settings_loaddata
/app/manage.py compilemessages
if [ -n "${DJANGO_SUPERUSER_PASSWORD+x}" ]; then
  echo "Creating adchadmin user with password $DJANGO_SUPERUSER_PASSWORD"
  /app/manage.py createsuperuser --email acdhadmin@discworld.acdh-ch-dev.oeaw.ac.at --user acdhadmin --noinput
fi
/app/manage.py runserver 0.0.0.0:5000
