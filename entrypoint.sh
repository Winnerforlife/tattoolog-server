#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

# Function for checking the availability of PostgreSQL
postgres_ready() {
python << END
import sys
import psycopg2

try:
    psycopg2.connect(
        dbname="${PG_DATABASE}",
        user="${PG_USER}",
        password="${PG_PASSWORD}",
        host="${DB_HOST}",
        port="${DB_PORT}"
    )
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}

# Waiting for PostgreSQL to become available
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done

>&2 echo 'PostgreSQL is available'

# Collecting static files and applying migrations
python manage.py collectstatic --noinput
python manage.py migrate

# Determining the number of worker processes
NUM_CORES=$(nproc)
NUM_WORKERS=$(( $NUM_CORES ))

# Determining the number of worker processes
if [ $DEBUG == "True" ]; then
    exec python3 manage.py runserver 0.0.0.0:${WEB_PORT}
else
    exec gunicorn config.wsgi:application --workers $NUM_WORKERS --bind 0.0.0.0:${WEB_PORT} --access-logfile=- --error-logfile=-
fi