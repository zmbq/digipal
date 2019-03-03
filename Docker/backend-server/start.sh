#! /bin/sh

cd /digipal
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn --workers 5 --bind 0.0.0.0:8090 build.wsgi:application --log-file /logs/guncorn.log
