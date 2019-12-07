#!/bin/sh
set -e
python manage.py makemigrations
python manage.py migrate
/usr/local/bin/gunicorn -c /usr/src/app/configs/gunicorn_config.py UTest_device_manage.wsgi