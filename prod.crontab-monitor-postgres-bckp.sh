#!/bin/bash

TIMESTAMP=$(date +%d-%m-%Y_%H_%M_%S)
DB_FILE_LOCATION=/home/info-admin/iva_dashboard/prod
MONITOR_POSTGRES=monitor-postgres

if [ -f "$DB_FILE_LOCATION/dump-monitor-postgres.sql" ]; then
  rm -f "$DB_FILE_LOCATION/dump-monitor-postgres.sql"
  docker exec -t $MONITOR_POSTGRES pg_dumpall -c -U admin > "$DB_FILE_LOCATION/dump-monitor-postgres.sql"
else
  docker exec -t $MONITOR_POSTGRES pg_dumpall -c -U admin > "$DB_FILE_LOCATION/dump-monitor-postgres.sql"
  echo "database saved $TIMESTAMP" >> "$DB_FILE_LOCATION/dump-monitor-postgres.log"
fi