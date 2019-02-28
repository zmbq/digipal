FROM alpine:3.9

# Get the sources
RUN apk add git
WORKDIR /
RUN git clone https://github.com/ruven/iipsrv.git

# Get the build tools ready
RUN apk add automake
RUN apk add autoconf

WORKDIR /iipsrv
# Deployed in /tmp/iipsrv/src/iipsrv.fcgi
RUN ./autogen.sh && ./configure && make

ENV VERBOSITY 1
ENV MAX_IMAGE_CACHE_SIZE 20
ENV JPEG_QUALITY 75
ENV MAX_CVT 800
ENV FILESYSTEM_PREVIX /image
ENV LOGFILE /logs/iipsrv.log

CMD ["/iipsrc/src/iipsrv.fcgi", "--bind", "127.0.0.1:9000", "--backlog", "1024"]


