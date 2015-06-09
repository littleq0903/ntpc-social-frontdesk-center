FROM ubuntu:14.04
MAINTAINER Colin Su <littleq0903@gmail.com>

# for django-bower
RUN apt-get update
RUN apt-get install -y npm
RUN npm install -g bower

# for python dependencies
ADD requirements.txt .
RUN pip install -r ./requirements.txt
