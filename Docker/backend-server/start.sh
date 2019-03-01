#! /bin/sh

cd /digipal
python manage.py migrate --noinput
python manage.py collectstatic --noinput

/usr/sbin/uwsgi --ini /digipal/wsgi.ini