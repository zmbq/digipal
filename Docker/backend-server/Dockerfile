FROM python:2.7-alpine

# Install necessary packages
RUN apk update && apk add \
    git \
    nodejs npm \
    postgresql-dev \
    gcc  \
    musl-dev \
    libxml2-dev \
    libxslt-dev \
    uwsgi uwsgi-python

# Clone the sources
RUN git clone -b develop https://github.com/kcl-ddh/digipal.git /digipal

# Install Python requirements
RUN pip install -r /digipal/build/requirements.txt

# Install node requirements
RUN npm install -g less typescript@2.1.5

# Copy parameter files
COPY settings_docker.py /digipal/digipal_project/local_settings.py
COPY wsgi.ini /digipal/wsgi.ini
COPY start.sh /digipal/build/start.sh

CMD ["/bin/sh", "/digipal/build/start.sh"]
