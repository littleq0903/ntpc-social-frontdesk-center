FROM ubuntu:14.04
MAINTAINER Colin Su <littleq0903@gmail.com>

# for bower
RUN apt-get update
RUN apt-get install -y nodejs npm python-setuptools libpq-dev python-dev libncurses5 libncurses5-dev git-core
RUN npm install -g bower

RUN ln -s /usr/bin/nodejs /usr/bin/node

# for python dependencies
RUN easy_install pip
ADD requirements.txt .
RUN pip install -r ./requirements.txt
