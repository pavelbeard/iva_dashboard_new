#!/bin/bash

set -e

psql -v ON_ERROR_STOP=1 --username= "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
        CREATE USER test_db
        CREATE DATABASE test_db
        GRANT ALL PRIVILEGES ON DATABASE test_db TO test_db;
EOSQL