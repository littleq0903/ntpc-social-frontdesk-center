FROM littleq0903/ntpc-frontdesk-env
MAINTAINER Colin Su

RUN mkdir src
ADD . src

WORKDIR src

EXPOSE 8000
