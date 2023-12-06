#!/bin/sh

until cd /backend
do
    echo "Waiting ..."
done


python -m celery -A shop worker -l info