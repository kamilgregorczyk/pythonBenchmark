FROM python:3.7-alpine

ENV PYTHONUNBUFFERED=1
WORKDIR scripts

RUN apk add build-base linux-headers bash

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . .
ENTRYPOINT bash -c "python main.py && cat results.csv"