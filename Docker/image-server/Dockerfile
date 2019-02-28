FROM ubuntu:18.04

# Install packages
RUN echo Updating && apt-get update
RUN apt-get install -y git
RUN apt-get install -y autoconf
RUN apt-get install -y pkg-config
RUN apt-get install -y libtool
RUN apt-get install -y libjpeg-dev
RUN apt-get install -y libtiff-dev
RUN apt-get install -y imagemagick
RUN apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# Get the sources
WORKDIR /
RUN git clone https://github.com/ruven/iipsrv.git

# Build
WORKDIR /iipsrv
# Deployed in /tmp/iipsrv/src/iipsrv.fcgi
RUN ./autogen.sh && ./configure && make

ENV VERBOSITY 1
ENV MAX_IMAGE_CACHE_SIZE 20
ENV JPEG_QUALITY 75
ENV MAX_CVT 800
ENV FILESYSTEM_PREVIX /image
ENV LOGFILE /logs/iipsrv.log

CMD ["/iipsrv/src/iipsrv.fcgi", "--bind", "127.0.0.1:9000", "--backlog", "1024"]


