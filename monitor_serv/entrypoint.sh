#!/bin/bash

if [ "$POSTGRES_DB_NAME" = "iva_dashboard_db" ]
then
  echo "Waiting for postgres..."
  
  while ! nc -z "$POSTGRES_DB_HOST" "$POSTGRES_DB_PORT" ; do
      sleep 0.1
  done

  echo "postgres started!"

fi

python3.11 manage.py migrate --noinput
python3.11 manage.py collectstatic --noinput --clear

exec "$@"