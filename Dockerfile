FROM ubuntu:20.04

RUN rm -rf /var/lib/docker
RUN apt update
RUN apt -y upgrade
RUN apt install -y python3-pip
RUN apt install -y sqlite3
RUN apt install -y build-essential libssl-dev libffi-dev python3-dev
RUN apt install python-is-python3

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app
