#!/bin/sh
#

python /app/manage.py migrate
python /app/manage.py loaddata discworld
python /app/manage.py loaddata auth
exec python /app/manage.py runserver 0.0.0.0:8000
