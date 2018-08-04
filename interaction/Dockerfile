FROM python:2.7-alpine

ENV TERM linux

RUN apk update && apk add --no-cache git netcat-openbsd openssl-dev libffi-dev g++ linux-headers make bash
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY check.py /check.py
COPY platforms /platforms
