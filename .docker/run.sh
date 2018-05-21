#!/usr/bin/env sh

export DEBUG=1
export SECRET_KEY="SECRET_KEY"$SECRET_KEY
export ALLOWED_HOSTS="*"

python /usr/src/app/norns/manage.py runserver
