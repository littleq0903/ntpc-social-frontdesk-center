FROM littleq0903/ntpc-frontdesk-env
MAINTAINER Colin Su

RUN mkdir src
ADD . src

WORKDIR src

RUN python manage.py bower install

EXPOSE 8000
