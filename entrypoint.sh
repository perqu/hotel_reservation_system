#!/bin/bash

python manage.py migrate

scripts/create_superuser.sh

python manage.py runserver 0.0.0.0:8000

