FROM ubuntu:16.04

ENV APPDIR /app
WORKDIR $APPDIR
RUN mkdir -p $APPDIR/phpipam_pyclient
RUN mkdir -p $APPDIR/tests

RUN apt-get update && apt-get install python python-pip -y
RUN apt-get update && apt-get install python3 python3-pip -y

COPY requirements.txt $APPDIR/
COPY requirements_dev.txt $APPDIR/
COPY phpipam_pyclient/config.json $APPDIR/

RUN pip3 install --no-cache-dir -r requirements.txt -U
RUN pip3 install --no-cache-dir -r requirements_dev.txt -U

ADD phpipam_pyclient $APPDIR/phpipam_pyclient
ADD tests $APPDIR/tests
