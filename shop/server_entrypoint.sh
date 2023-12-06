#!/bin/sh

until cd /backend
do
    echo "Waiting for server volume..."
done

until python manage.py makemigrations
do
    echo "Waiting for db to be ready..."
    sleep 2
done


until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done


#python manage.py collectstatic --noinput
#python manage.py createsuperuser --username=admin --email=admin@example.com --noinput
# python manage.py createsuperuser --noinput

# for debug
python manage.py runserver 0.0.0.0:8000