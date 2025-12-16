#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r scpi/requirements.txt

cd scpi
python manage.py collectstatic --no-input
python manage.py migrate
python create_users_direct.py