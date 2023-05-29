FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get upgrade -y && apt-get install -y libsqlite3-dev libpq-dev python-dev python3-dev libxml2-dev libxslt1-dev zlib1g-dev libsasl2-dev libldap2-dev build-essential libssl-dev libffi-dev libmysqlclient-dev libjpeg-dev libjpeg8-dev liblcms2-dev libblas-dev libatlas-base-dev
RUN pip install -U pip setuptools

COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt

ADD . /code/
EXPOSE 8000
