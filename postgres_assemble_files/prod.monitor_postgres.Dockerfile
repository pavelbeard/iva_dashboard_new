FROM postgres:alpine

COPY docker-entrypoint-initdb.d/prod.init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh

ENTRYPOINT ["/docker-entrypoint-initdb.d/init-user-db.sh"]