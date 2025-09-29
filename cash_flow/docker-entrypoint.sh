#!/bin/sh

echo "Apply database migrations"
python manage.py migrate

echo "Apply adding base data"
python manage.py migrate_data

echo "Running server"
gunicorn api_service.wsgi:application --bind 0.0.0.0:8000 --workers 1