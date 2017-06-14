FROM python:3.6
MAINTAINER X

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y \
    locales \
    && rm -rf /var/lib/apt/lists/*

RUN useradd uid1000 -d /home/uid1000
RUN mkdir -p /home/uid1000 && chown uid1000: /home/uid1000
VOLUME /home/uid1000

USER root

COPY requirements.txt /opt/code/requirements.txt
WORKDIR /opt/code
RUN pip install -Ur requirements.txt
COPY . /opt/code

RUN chown -R uid1000: /opt

WORKDIR /opt/code/shackbot

USER uid1000

CMD ["python3", "main.py"]
