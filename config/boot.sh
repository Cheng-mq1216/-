#!/usr/bin/env bash

# use inside web app container

source .env

export SECRET_KEY
export MYSQL_ROOT_PASSWORD
export MYSQL_USER
export MYSQL_PASSWORD
export MYSQL_DATABASE

python manage.py collectstatic --noinput &&
python manage.py migrate &&
gunicorn app.wsgi:application -w 2 -b 0.0.0.0:8000
