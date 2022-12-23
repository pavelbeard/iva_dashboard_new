#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username= "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER admin
        CREATE DATABASE iva_dashboard_db
        GRANT ALL PRIVILEGES ON DATABASE iva_dashboard_db TO admin
        ALTER USER admin WITH PASSWORD "$POSTGRES_DB_PASSWORD";
EOSQL