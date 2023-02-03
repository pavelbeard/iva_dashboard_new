#!/bin/bash

if [ "$POSTGRES_DB_NAME" = "iva_dashboard" ]
then
  echo "Waiting for postgres..."
  
  while ! nc -z "$POSTGRES_DB_HOST" "$POSTGRES_DB_PORT" ; do
      sleep 0.1
  done

  echo "postgres started!"

fi

python3.11 manage.py migrate --noinput
python3.11 manage.py collectstatic --noinput --clear
python3.11 manage.py createsuperuser --noinput
python3.11 manage.py setupdashboard

export ENCRYPTION_KEY=$(python3.11 manage.py genencryptionkey)

exec "$@"