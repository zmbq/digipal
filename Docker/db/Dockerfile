FROM postgres:9.6-alpine

ENV POSTGRES_DB digipal
ENV POSTGRES_USER app_digipal
ENV POSTGRESS_PASSWORD dppsqlpass

ADD initdb.sh /docker-entrypoint-initdb.d/
ADD initial.bak /docker-entrypoint-initdb.d/

