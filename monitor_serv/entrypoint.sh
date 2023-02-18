#!/usr/bin/env bash

if [ "$POSTGRES_DB_NAME" = "iva_dashboard" ]
then
  echo "Waiting for postgres..."
  
  while ! nc -z "$POSTGRES_DB_HOST" "$POSTGRES_DB_PORT" ; do
      sleep 0.1
  done

  echo "postgres started!"

fi

IVA_DASHBOARD_CHECK=$(python3.11 manage.py checkdb --iva_dashboard)
IVCS_CHECK=$(python3.11 manage.py checkdb --ivcs)

if [ $(python3.11 -c "print($IVA_DASHBOARD_CHECK + $IVCS_CHECK)") -eq 0 ];
then
  python3.11 manage.py migrate --database iva_dashboard --noinput
  python3.11 manage.py collectstatic --noinput --clear
  python3.11 manage.py createsuperuser --database iva_dashboard --noinput
  python3.11 manage.py setupdashboard
else
  echo "Приложение заве"
fi


#export ENCRYPTION_KEY=$(python3.11 manage.py genencryptionkey)

exec "$@"