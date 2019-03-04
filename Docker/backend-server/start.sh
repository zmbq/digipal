#! /bin/sh

until PGPASSWORD="dppsqlpass" psql -h archetype-db -U app_digipal --db digipal -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 10
done

echo Postgres is ready.

cd /digipal
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn --workers 5 --bind 0.0.0.0:8090 build.wsgi:application --log-file /logs/guncorn.log
