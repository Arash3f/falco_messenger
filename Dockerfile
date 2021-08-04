FROM python:3.8.3-alpine

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add gcc python3-dev musl-dev openssl-dev libffi-dev  jpeg-dev zlib-dev 

# install dependencies
RUN pip install --upgrade pip 
COPY ./project/requirements-docker.txt /usr/src/app
RUN pip install -r requirements-docker.txt

# copy project file
COPY ./project /usr/src/app

RUN python manage.py flush --no-input
RUN python manage.py makemigrations messenger
RUN python manage.py migrate
RUN python manage.py collectstatic
RUN export DJANGO_SETTINGS_MODULE=falco.settings
