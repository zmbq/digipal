#! /bin/sh
echo Restoring database contents
pg_restore /docker-entrypoint-initdb.d/initial.bak --dbname digipal --username app_digipal
