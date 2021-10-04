FROM python:3.9-slim-buster

WORKDIR /tmp

RUN pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r requirements.txt

WORKDIR /root
