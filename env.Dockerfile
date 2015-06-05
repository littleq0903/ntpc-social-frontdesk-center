FROM python:2.7
MAINTAINER Colin Su

ADD requirements.txt .
RUN pip install -r ./requirements.txt
