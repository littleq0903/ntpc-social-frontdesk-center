FROM ntpc-frontdesk-env:1.0
MAINTAINER Colin Su

RUN mkdir src
ADD . src

WORKDIR src

EXPOSE 8000
