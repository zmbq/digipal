FROM python:2.7-alpine

# Install necessary packages
RUN apk update && apk add \
    git \
    nodejs npm \
    postgresql-dev \
    gcc  \
    musl-dev \
    libxml2-dev \
    libxslt-dev

# Clone just the build directory
RUN mkdir /digipal
COPY build /digipal/build

# RUN git clone -b develop https://github.com/kcl-ddh/digipal.git /digipal

# Install Python requirements
RUN pip install -r /digipal/build/requirements.txt
RUN pip install gunicorn
# Install node requirements
RUN npm install -g less typescript@2.1.5

# Copy the rest of the sources (so if one source file changes, the image is built from here)
COPY digipal /digipal/digipal
COPY digipal_project /digipal/digipal_project
COPY digipal_text /digipal/digipal_text
COPY manage.py /digipal/manage.py

# Copy parameter files
COPY Docker/backend-server/settings_docker.py /digipal/digipal_project/local_settings.py
# COPY Docker/backend-server/wsgi.ini /digipal/wsgi.ini
COPY Docker/backend-server/start.sh /digipal/build/start.sh

ENV DJANGO_SETTINGS_MODULE digipal_project.settings
CMD ["/bin/sh", "/digipal/build/start.sh"]
